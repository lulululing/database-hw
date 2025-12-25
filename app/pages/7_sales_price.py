
import streamlit as st
import pandas as pd
from utils.database import get_db_manager
from config import ROLES

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限
has_price_permission = any(perm in st.session_state.get('permissions', []) 
                          for perm in ['edit_price', 'view_price'])
if not has_price_permission:
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="销售统计",
    layout="wide"
)
st.title("销售统计")
def main():
    """价格体系页面"""
    # 获取当前用户信息
    u = st.session_state.user_info
    role = u['role']
    country = u.get('country', None)
    
    # 判断是否有编辑权限
    from config import ROLES
    is_editable = 'edit_price' in ROLES[role]['permissions']
    
    # 标题
    if is_editable:
        if country:
            title = f"Price Management ({country})"
            st.info(f"**{country}** Price Management Mode (Editable)")
        else:
            title = "Price Management (Global)"
            st.info("Global Price Management Mode (Editable)")
    else:
        title = "Price Query (Read-Only)"
        st.info("Price Query Mode (Read-Only)")
    
    st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
    
    db = get_db_manager()
    
    # 1. 获取数据
    if country:
        # 业务员只能查看/编辑自己国家的数据
        sql = "SELECT * FROM Sales_Price WHERE Country = %s"
        df = db.execute_query(sql, (country,))
    else:
        # 经理/FBP可以查看所有数据
        sql = "SELECT * FROM Sales_Price"
        df = db.execute_query(sql)
    
    if df.empty:
        st.warning("No price data available")
        return

    # 2. 展示/编辑逻辑
    if is_editable:
        st.markdown("### Price Editor")
        st.markdown("> Edit prices directly in the table, then click Save")
        
        # 配置列编辑器
        edited_df = st.data_editor(
            df,
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "Model": st.column_config.TextColumn("Model", disabled=True),
                "Country": st.column_config.TextColumn("Country", disabled=True),
                "h_Time": st.column_config.TextColumn("Time Period", disabled=True),
                "Currency": st.column_config.TextColumn("Currency", disabled=True),
                "Price": st.column_config.NumberColumn("Price", required=True, format="%.2f"),
                "Sales": st.column_config.NumberColumn("Sales Forecast", required=True)
            },
            num_rows="dynamic",
            key="price_editor"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Save Changes", type="primary", use_container_width=True):
                if db.save_sales_price(edited_df):
                    st.success("Price table updated successfully")
                    db.log_event(u['id'], "UPDATE_PRICE", f"Updated price table for {country or 'global'}")
                    st.rerun()
                else:
                    st.error("Save failed")
    else:
        # 只读模式
        st.markdown("### Price Query")
        
        # 添加筛选选项
        col1, col2, col3 = st.columns(3)
        
        with col1:
            unique_models = df['Model'].unique().tolist()
            selected_models = st.multiselect("Filter by Model", unique_models, default=unique_models[:3])
        
        with col2:
            unique_times = df['h_Time'].unique().tolist()
            selected_time = st.selectbox("Filter by Time", ["All"] + unique_times)
        
        with col3:
            if not country:
                unique_countries = df['Country'].unique().tolist()
                selected_countries = st.multiselect("Filter by Country", unique_countries, default=unique_countries[:3])
            else:
                selected_countries = [country]
                st.text_input("Country", country, disabled=True)
        
        # 应用筛选
        filtered_df = df.copy()
        if selected_models:
            filtered_df = filtered_df[filtered_df['Model'].isin(selected_models)]
        if selected_time != "All":
            filtered_df = filtered_df[filtered_df['h_Time'] == selected_time]
        if not country and selected_countries:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )
        
        # 显示统计信息
        if not filtered_df.empty:
            st.markdown("### Price Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Models", len(filtered_df['Model'].unique()))
            with col2:
                st.metric("Avg Price", f"¥{filtered_df['Price'].mean():.2f}")
            with col3:
                st.metric("Total Forecast", f"{filtered_df['Sales'].sum():,}")
            with col4:
                st.metric("Records", len(filtered_df))

if __name__ == "__main__":
    main()