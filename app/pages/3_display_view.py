
import streamlit as st
import pandas as pd
import io
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限（任意视图权限）
view_perms = ['view_display', 'view_s_display', 'view_display_country']
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
def main():
    """综合视图页面"""
    st.markdown('<div class="main-header">Display View</div>', unsafe_allow_html=True)
    
    # 获取用户信息
    u = st.session_state.user_info
    db = get_db_manager()
    
    # 确定可用的视图
    permissions = st.session_state.permissions
    available_views = []
    
    if 'view_display' in permissions:
        available_views.append(("true_Revenues", "Revenue View"))
        available_views.append(("s_Display", "Summary Display"))
    
    if 'view_s_display' in permissions:
        available_views.append(("s_Display", "Summary Display"))
    
    if 'view_display_country' in permissions:
        available_views.append(("s_Display_Country", "Country Display"))
    
    if not available_views:
        st.error("No display views available for your role")
        return
    
    # 选择视图
    view_options = [name for _, name in available_views]
    selected_view_name = st.selectbox("Select View", view_options)
    
    # 获取对应的数据库视图名称
    selected_db_view = next(db_view for db_view, name in available_views if name == selected_view_name)
    
    # 筛选条件
    st.markdown("### Filter Options")
    
    # 根据用户角色限制筛选
    if u.get('country'):
        # 业务员只能看自己国家
        st.info(f"You can only view data for **{u['country']}**")
        selected_country = [u['country']]
        country_disabled = True
    else:
        # 经理/FBP可以选择多个国家
        countries = db.get_all_countries()
        selected_country = st.multiselect("Select Countries", countries, default=countries[:3])
        country_disabled = False
    
    # 时间筛选
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox("Select Time Period", ["All"] + time_periods)
    
# 查询按钮
    if st.button("Query Data", type="primary", use_container_width=True):
        with st.spinner("Querying data..."):
            try:
                # 构建查询
                if selected_db_view == "s_Display_Country":
                    # 国家视图需要国家参数
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
                else:
                    query = f"SELECT * FROM {selected_db_view}"
                    params = ()
                
                # 执行查询
                df = db.execute_query(query, params if params else None)
                
                if not df.empty:
                    # 应用时间筛选
                    if selected_time != "All":
                        df = df[df['Time'] == selected_time] if 'Time' in df.columns else df
                    
                    st.success(f"Found {len(df)} records")
                    
                    # 显示数据
                    st.markdown("### Data Preview")
                    st.dataframe(df, use_container_width=True, height=400)
                    
                    # 统计信息
                    st.markdown("### Summary Statistics")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Records", len(df))
                    
                    with col2:
                        if 'Sales' in df.columns:
                            st.metric("Total Sales", f"{df['Sales'].sum():,}")
                        elif 'Total_Sales' in df.columns:
                            st.metric("Total Sales", f"{df['Total_Sales'].sum():,}")
                    
                    with col3:
                        if 'Revenue' in df.columns:
                            st.metric("Total Revenue", f"¥{df['Revenue'].sum():,.2f}")
                        elif 'Revenues' in df.columns:
                            st.metric("Total Revenue", f"¥{df['Revenues'].sum():,.2f}")
                        elif 'Total_Revenue' in df.columns:
                            st.metric("Total Revenue", f"¥{df['Total_Revenue'].sum():,.2f}")
                    
                    # 导出功能
                    if 'export' in permissions:
                        st.markdown("---")
                        st.markdown("### Export Data")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            csv = df.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label="Export as CSV",
                                data=csv,
                                file_name=f"{selected_view_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col2:
                            # Excel导出 (修复版)
                            # 使用 BytesIO 在内存中操作，避免文件权限问题，并使用 with 语句自动保存
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='View_Data')
                            
                            excel_data = output.getvalue()
                            
                            st.download_button(
                                label="Export as Excel",
                                data=excel_data,
                                file_name=f"{selected_view_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                else:
                    st.warning("No data found")
                    
            except Exception as e:
                st.error(f"Query failed: {str(e)}")
    else:
        st.info("Select view options and click 'Query Data' button")

if __name__ == "__main__":
    main()