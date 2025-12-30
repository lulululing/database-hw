import streamlit as st
import pandas as pd
import io
from utils.helper import handle_save_success
from utils.database import get_db_manager
from utils.i18n import get_text
from utils.helper import apply_currency_conversion
from utils.i18n import show_sidebar_with_nav, get_text
# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_required'))
    st.switch_page("app.py")

# 检查权限（任意视图权限）
view_perms = ['view_display', 'view_s_display', 'view_display_country', 
              'view_history_country', 'view_budget_country', 'view_costs_country', 'view_sales_country']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in view_perms)

if not has_permission:
    st.error(get_text('no_permission'))
    st.stop()

# 设置页面
st.set_page_config(
    page_title=get_text('nav_display'),
    layout="wide"
)
show_sidebar_with_nav()
st.title(get_text('nav_display'))

def log_export_action(db, view_name, export_type, record_count):
    """记录导出操作的日志"""
    try:
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        details = f"导出{export_type}: {view_name}, 记录数: {record_count}"
        
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="EXPORT",  # 对应10_System_Log.py中的EXPORT操作类型
            message_prefix="数据导出",
            details=details,
            operation_type="导出"
        )
    except Exception as e:
        print(f"记录导出日志失败: {e}")
        return False

def log_view_action(db, view_name, country_filter=None, time_filter=None, currency_filter=None):
    """记录视图查看操作的日志"""
    try:
        # 构建日志详情
        filter_details = []
        if country_filter:
            filter_details.append(f"国家: {country_filter}")
        if time_filter and time_filter != "All":
            filter_details.append(f"时间: {time_filter}")
        if currency_filter:
            filter_details.append(f"货币: {currency_filter}")
        
        details = f"查看视图: {view_name}"
        if filter_details:
            details += f" | 筛选: {'; '.join(filter_details)}"
        
        # 获取用户信息
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        # 使用helper.py中的handle_save_success函数
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="VIEW",  # 对应10_System_Log.py中的VIEW操作类型
            message_prefix="视图查询",
            details=details,
            operation_type="查看"  # 虽然这不是保存操作，但函数可以复用
        )
    except Exception as e:
        st.warning(f"记录日志失败: {e}")
        return False

def main():
    """综合视图页面"""
    
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
        available_views.append(("Display", get_text('view_display_all')))
        available_views.append(("s_Display", get_text('view_s_display')))
        available_views.append(("s_Display_Model", get_text('view_s_model')))
        available_views.append(("s_Display_Country", get_text('view_s_country')))
        
        # 经理也可以看各国的Display视图
        available_views.append(("DisplayIndia", "🇮🇳 " + get_text('view_display_india')))
        available_views.append(("DisplayPakistan", "🇵🇰 " + get_text('view_display_pakistan')))
        available_views.append(("DisplayKenya", "🇰🇪 " + get_text('view_display_kenya')))
        available_views.append(("DisplaySouthAfrica", "🇿🇦 " + get_text('view_display_sa')))
    
    elif role == 'FBP':
        # 财务：Display视图（所有国家）
        available_views.append(("Display", get_text('view_display_all')))
        available_views.append(("History", get_text('view_history')))
        available_views.append(("Budget", get_text('view_budget')))
        available_views.append(("Costs", get_text('view_costs')))
        available_views.append(("Sales_Price", get_text('view_sales_price')))
    
    elif role.startswith('Salesperson_'):
        # 业务员：只看本国的视图
        country = u.get('country', '')
        
        if country == 'India':
            available_views.append(("DisplayIndia", "🇮🇳 " + get_text('view_display_india')))
            available_views.append(("Sales_Price_India", get_text('view_sales_price_india')))
        elif country == 'Pakistan':
            available_views.append(("DisplayPakistan", "🇵🇰 " + get_text('view_display_pakistan')))
            available_views.append(("Sales_Price_Pakistan", get_text('view_sales_price_pakistan')))
        elif country == 'Kenya':
            available_views.append(("DisplayKenya", "🇰🇪 " + get_text('view_display_kenya')))
            available_views.append(("Sales_Price_Kenya", get_text('view_sales_price_kenya')))
        elif country == 'South Africa':
            available_views.append(("DisplaySouthAfrica", "🇿🇦 " + get_text('view_display_sa')))
            available_views.append(("Sales_Price_South_Africa", get_text('view_sales_price_sa')))
        
        # 业务员也能查看本国的History, Budget, Costs
        available_views.append(("History_Country", get_text('view_history_country')))
        available_views.append(("Budget_Country", get_text('view_budget_country')))
        available_views.append(("Costs_Country", get_text('view_costs_country')))
    
    if not available_views:
        st.error(get_text('msg_no_views'))
        return
    
    # 选择视图
    view_options = [name for _, name in available_views]
    selected_view_name = st.selectbox(get_text('select_view'), view_options)
    
    # 获取对应的数据库视图名称
    selected_db_view = next(db_view for db_view, name in available_views if name == selected_view_name)
    
    # 筛选条件
    st.markdown(f"### {get_text('filter_title')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 根据用户角色限制筛选
        if u.get('country'):
            # 业务员只能看自己国家
            st.info(get_text('msg_current_region', region=u['country']))
            selected_country = [u['country']]
            country_disabled = True
        else:
            # 经理/FBP可以选择多个国家（但只显示实际存在的4个国家）
            selected_country = st.multiselect(get_text('select_country'), ACTUAL_COUNTRIES, default=ACTUAL_COUNTRIES[:2])
            country_disabled = False
    
    with col2:
        # 时间筛选
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox(get_text('select_time'), ["All"] + time_periods)
    
    with col3:
        # 货币选择（新增功能）
        default_idx = 0 if st.session_state.get('language') == 'zh' else 1
        currency_opt = st.selectbox(
            get_text('currency'), 
            ["CNY", "USD"], 
            index=default_idx, 
            key="curr_select"
        )
    
    # 查询按钮
    if st.button(get_text('btn_query'), type="primary", use_container_width=True):
        with st.spinner(get_text('status_querying')):
            try:
                log_view_action(
                    db=db,
                    view_name=selected_view_name,
                    country_filter=selected_country if not country_disabled else st.session_state.user_info.get('country', ''),
                    time_filter=selected_time,
                    currency_filter=currency_opt
                )
                # 构建查询（保持V1的简洁查询逻辑）
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
                    st.success(get_text('msg_found_records', count=len(df)))
                    
                    # 应用货币转换（新增功能）
                    df_converted, currency_symbol = apply_currency_conversion(df, db, currency_opt)
                    
                    # 显示数据
                    st.markdown(f"### {get_text('header_preview')}")
                    
                    # 创建显示用的副本（保持V1的简洁样式）
                    df_display = df_converted.copy()
                    
                    # 智能列检测和格式化（V2的改进）
                    # 自动识别货币相关列并添加符号
                    currency_related_keywords = ['Revenue', 'Profit', 'Income', 'Cost', 'Price', 'Sales']
                    for col in df_display.columns:
                        # 检查是否是货币相关列
                        is_currency_col = any(keyword in col for keyword in currency_related_keywords)
                        
                        if is_currency_col and col in df_display.columns and pd.api.types.is_numeric_dtype(df_display[col]):
                            # 为数值添加货币符号
                            df_display[col] = df_display[col].apply(
                                lambda x: f"{currency_symbol}{x:,.2f}" if pd.notna(x) else x
                            )
                    
                    st.dataframe(df_display, use_container_width=True, height=400)
                    
                    # 统计信息（使用智能列检测）
                    st.markdown(f"### {get_text('header_stats')}")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(get_text('metric_records'), len(df))
                    
                    with col2:
                        # 智能查找销售列
                        sales_col = None
                        sales_keywords = ['Sales', 'Quantity', 'Volume']
                        for col in df_converted.columns:
                            if any(keyword in col for keyword in sales_keywords):
                                sales_col = col
                                break
                        
                        if sales_col:
                            st.metric(get_text('metric_total_sales'), f"{df_converted[sales_col].sum():,.0f}")
                        else:
                            st.metric(get_text('metric_total_sales'), "N/A")
                    
                    with col3:
                        # 智能查找收入列（V2的改进）
                        revenue_col = None
                        revenue_keywords = ['Revenues', 'Revenue', 'Total_Revenue']
                        for col in df_converted.columns:
                            if any(keyword in col for keyword in revenue_keywords):
                                revenue_col = col
                                break
                        
                        if revenue_col:
                            st.metric(get_text('metric_total_revenue'), f"{currency_symbol}{df_converted[revenue_col].sum():,.2f}")
                        else:
                            st.metric(get_text('metric_total_revenue'), "N/A")
                    
                    with col4:
                        # 智能查找利润列（V2的改进）
                        profit_col = None
                        profit_keywords = ['Net_income', 'Net_Income', 'Profit', 'NetProfit']
                        for col in df_converted.columns:
                            if any(keyword in col for keyword in profit_keywords):
                                profit_col = col
                                break
                        
                        if profit_col:
                            st.metric(get_text('metric_total_profit'), f"{currency_symbol}{df_converted[profit_col].sum():,.2f}")
                        else:
                            st.metric(get_text('metric_total_profit'), "N/A")
                    
                    # 导出功能（保持V1样式）
                    if 'export' in permissions:
                        st.markdown("---")
                        st.markdown(f"### {get_text('header_export')}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            csv = df_converted.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label=get_text('btn_export_csv'),
                                data=csv,
                                file_name=f"{selected_db_view}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True,
                                # 添加on_click回调记录日志
                                on_click=lambda: log_export_action(db, selected_db_view, 'CSV', len(df_converted))
                            )
                                                
                        with col2:
                            # Excel导出
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df_converted.to_excel(writer, index=False, sheet_name='View_Data')
                            
                            excel_data = output.getvalue()
                            
                            st.download_button(
                                label=get_text('btn_export_excel'),
                                data=excel_data,
                                file_name=f"{selected_db_view}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True,
                                # 添加on_click回调记录日志
                                on_click=lambda: log_export_action(db, selected_db_view, 'Excel', len(df_converted))
                            )
                else:
                    st.warning(get_text('msg_no_data'))
                    
            except Exception as e:
                st.error(f"{get_text('error')} {str(e)}")
                st.info(get_text('tip_query_error'))
                # 显示调试信息（保持V1的调试方式）
                with st.expander(get_text('debug_info')):
                    st.code(f"Query: {query}")
                    st.code(f"Params: {params}")
                    st.code(f"Error: {str(e)}")
    else:
        st.info(get_text('tip_query'))

if __name__ == "__main__":
    main()