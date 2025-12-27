import streamlit as st
import pandas as pd
import io
from utils.database import get_db_manager
from config import ROLES, CURRENCY_COLUMNS

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限（任意视图权限）
view_perms = ['view_display', 'view_s_display', 'view_display_country', 
              'view_history_country', 'view_budget_country', 'view_costs_country', 'view_sales_country']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in view_perms)

if not has_permission:
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="查看视图",
    layout="wide"
)
st.title("查看视图")

def format_currency_columns(df):
    """为货币相关的列添加货币符号"""
    df_display = df.copy()
    
    for col in df_display.columns:
        # 检查是否是货币相关列
        is_currency_col = any(currency_col in col for currency_col in CURRENCY_COLUMNS)
        
        if is_currency_col and col in df_display.columns:
            # 为数值添加货币符号
            df_display[col] = df_display[col].apply(
                lambda x: f"¥{x:,.2f}" if pd.notna(x) and isinstance(x, (int, float)) else x
            )
    
    return df_display

def main():
    """综合视图页面"""
    st.markdown('<div class="main-header">Display View</div>', unsafe_allow_html=True)
    
    # 获取用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    db = get_db_manager()
    
    # 确定可用的视图
    permissions = st.session_state.permissions
    available_views = []
    
    # 定义实际存在的国家（只有这4个）
    ACTUAL_COUNTRIES = ['India', 'Pakistan', 'Kenya', 'South Africa']
    
    # 根据权限配置可用视图
    if role == 'Manager':
        # 经理：所有Display视图 + 所有s_Display视图
        available_views.append(("Display", "📊 Comprehensive Display (All Countries)"))
        available_views.append(("s_Display", "📈 Summary Display (History+Forecast+Budget)"))
        available_views.append(("s_Display_Model", "📱 Model Summary Display"))
        available_views.append(("s_Display_Country", "🌍 Country Summary Display"))
        
        # 经理也可以看各国的Display视图
        available_views.append(("DisplayIndia", "🇮🇳 Display - India"))
        available_views.append(("DisplayPakistan", "🇵🇰 Display - Pakistan"))
        available_views.append(("DisplayKenya", "🇰🇪 Display - Kenya"))
        available_views.append(("DisplaySouthAfrica", "🇿🇦 Display - South Africa"))
    
    elif role == 'FBP':
        # 财务：Display视图（所有国家）
        available_views.append(("Display", "📊 Comprehensive Display (All Countries)"))
        available_views.append(("History", "📋 Historical Data"))
        available_views.append(("Budget", "📈 Budget Data"))
        available_views.append(("Costs", "💰 Cost Data"))
        available_views.append(("Sales_Price", "💵 Sales Price Data"))
    
    elif role.startswith('Salesperson_'):
        # 业务员：只看本国的视图
        country = u.get('country', '')
        
        if country == 'India':
            available_views.append(("DisplayIndia", "🇮🇳 Display - India"))
            available_views.append(("Sales_Price_India", "💵 Sales Price - India"))
        elif country == 'Pakistan':
            available_views.append(("DisplayPakistan", "🇵🇰 Display - Pakistan"))
            available_views.append(("Sales_Price_Pakistan", "💵 Sales Price - Pakistan"))
        elif country == 'Kenya':
            available_views.append(("DisplayKenya", "🇰🇪 Display - Kenya"))
            available_views.append(("Sales_Price_Kenya", "💵 Sales Price - Kenya"))
        elif country == 'South Africa':
            available_views.append(("DisplaySouthAfrica", "🇿🇦 Display - South Africa"))
            available_views.append(("Sales_Price_South_Africa", "💵 Sales Price - South Africa"))
        
        # 业务员也能查看本国的History, Budget, Costs
        available_views.append(("History_Country", f"📋 Historical Data - {country}"))
        available_views.append(("Budget_Country", f"📈 Budget Data - {country}"))
        available_views.append(("Costs_Country", f"💰 Cost Data - {country}"))
    
    if not available_views:
        st.error("No display views available for your role")
        return
    
    # 选择视图
    view_options = [name for _, name in available_views]
    selected_view_name = st.selectbox("📊 Select View", view_options)
    
    # 获取对应的数据库视图名称
    selected_db_view = next(db_view for db_view, name in available_views if name == selected_view_name)
    
    # 筛选条件
    st.markdown("### 🔍 Filter Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 根据用户角色限制筛选
        if u.get('country'):
            # 业务员只能看自己国家
            st.info(f"🌍 You can only view data for **{u['country']}**")
            selected_country = [u['country']]
            country_disabled = True
        else:
            # 经理/FBP可以选择多个国家（但只显示实际存在的4个国家）
            selected_country = st.multiselect("🌍 Select Countries", ACTUAL_COUNTRIES, default=ACTUAL_COUNTRIES[:2])
            country_disabled = False
    
    with col2:
        # 时间筛选
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox("📅 Select Time Period", ["All"] + time_periods)
    
    # 查询按钮
    if st.button("🔎 Query Data", type="primary", use_container_width=True):
        with st.spinner("Querying data..."):
            try:
                # 构建查询
                query = ""
                params = ()
                
                # 根据视图类型构建不同的查询
                if selected_db_view.endswith('_Country'):
                    # 特殊处理：业务员查看本国的基础表数据
                    base_table = selected_db_view.replace('_Country', '')
                    query = f"SELECT * FROM {base_table} WHERE Country = %s"
                    params = (u['country'],)
                    
                    if selected_time != "All":
                        if base_table == "History":
                            query += " AND h_Time = %s"
                            params = (u['country'], selected_time)
                        elif base_table == "Budget":
                            query += " AND h_Time = %s"
                            params = (u['country'], selected_time)
                        elif base_table == "Costs":
                            query += " AND Costs_time = %s"
                            params = (u['country'], selected_time)
                
                elif selected_db_view in ['DisplayIndia', 'DisplayPakistan', 'DisplayKenya', 'DisplaySouthAfrica',
                                         'Sales_Price_India', 'Sales_Price_Pakistan', 'Sales_Price_Kenya', 'Sales_Price_South_Africa']:
                    # 业务员的国家视图
                    query = f"SELECT * FROM {selected_db_view}"
                    if selected_time != "All":
                        query += " WHERE h_Time = %s"
                        params = (selected_time,)
                    else:
                        params = ()
                
                elif selected_db_view == "s_Display_Country":
                    # 国家汇总视图
                    if u.get('country'):
                        query = "SELECT * FROM s_Display_Country WHERE Country = %s"
                        params = (u['country'],)
                    else:
                        if selected_country:
                            placeholders = ', '.join(['%s'] * len(selected_country))
                            query = f"SELECT * FROM s_Display_Country WHERE Country IN ({placeholders})"
                            params = tuple(selected_country)
                        else:
                            query = "SELECT * FROM s_Display_Country"
                            params = ()
                    
                    if selected_time != "All":
                        query += " AND h_Time = %s" if "WHERE" in query else " WHERE h_Time = %s"
                        params = params + (selected_time,) if params else (selected_time,)
                
                else:
                    # 其他视图（Display, s_Display等）
                    query = f"SELECT * FROM {selected_db_view}"
                    
                    where_clauses = []
                    query_params = []
                    
                    # 国家筛选（只对有Country字段的视图有效）
                    if selected_country and not country_disabled and selected_db_view not in ['s_Display_Model']:
                        placeholders = ', '.join(['%s'] * len(selected_country))
                        where_clauses.append(f"Country IN ({placeholders})")
                        query_params.extend(selected_country)
                    
                    # 时间筛选
                    if selected_time != "All":
                        where_clauses.append("h_Time = %s")
                        query_params.append(selected_time)
                    
                    if where_clauses:
                        query += " WHERE " + " AND ".join(where_clauses)
                    
                    params = tuple(query_params)
                
                # 执行查询
                df = db.execute_query(query, params if params else None)
                
                if not df.empty:
                    st.success(f"✅ Found {len(df)} records")
                    
                    # 格式化货币列
                    df_formatted = format_currency_columns(df)
                    
                    # 显示数据
                    st.markdown("### 📋 Data Preview")
                    st.dataframe(df_formatted, use_container_width=True, height=400)
                    
                    # 统计信息
                    st.markdown("### 📊 Summary Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📝 Total Records", len(df))
                    
                    with col2:
                        if 'Sales' in df.columns:
                            st.metric("📦 Total Sales", f"{df['Sales'].sum():,}")
                    
                    with col3:
                        revenue_col = None
                        for col in ['Revenues', 'Revenue', 'Revenues_history', 'Revenues_forecasting']:
                            if col in df.columns:
                                revenue_col = col
                                break
                        
                        if revenue_col:
                            st.metric("💰 Total Revenue", f"¥{df[revenue_col].sum():,.2f}")
                    
                    with col4:
                        profit_col = None
                        for col in ['Net_income', 'Net_Income', 'Net_income_history', 'Net_income_forecasting']:
                            if col in df.columns:
                                profit_col = col
                                break
                        
                        if profit_col:
                            st.metric("📈 Total Net Income", f"¥{df[profit_col].sum():,.2f}")
                    
                    # 导出功能
                    if 'export' in permissions:
                        st.markdown("---")
                        st.markdown("### 📥 Export Data")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            csv = df.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label="💾 Export as CSV",
                                data=csv,
                                file_name=f"{selected_view_name.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col2:
                            # Excel导出
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='View_Data')
                            
                            excel_data = output.getvalue()
                            
                            st.download_button(
                                label="📊 Export as Excel",
                                data=excel_data,
                                file_name=f"{selected_view_name.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                else:
                    st.warning("⚠️ No data found")
                    
            except Exception as e:
                st.error(f"❌ Query failed: {str(e)}")
                st.info("💡 Tip: Check if the view exists in database and you have proper permissions")
                # 显示调试信息
                with st.expander("🔍 Debug Info"):
                    st.code(f"Query: {query}")
                    st.code(f"Params: {params}")
                    st.code(f"Error: {str(e)}")
    else:
        st.info("👆 Select view options and click 'Query Data' button")

if __name__ == "__main__":
    main()