import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 检查权限 - 所有人都能查看价格
view_perms = ['view_price', 'edit_price']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in view_perms)

if not has_permission:
    st.error("您没有权限访问此页面")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="销售价格",
    layout="wide"
)

def main():
    st.title("销售价格查询")
    
    # 获取用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    permissions = st.session_state.permissions
    db = get_db_manager()
    
    # 根据角色显示提示
    if u.get('country'):
        st.info(f"当前区域: **{u['country']}** (您只能查看本国数据)")
        country_filter = u['country']
    else:
        st.info("您可以查看所有国家的销售价格数据")
        country_filter = None
    
    # 查询数据
    if country_filter:
        df = db.get_sales_price_data(country=country_filter)
    else:
        df = db.get_sales_price_data()
    
    if not df.empty:
        st.success(f"找到 {len(df)} 条记录")
        
        # 筛选功能
        with st.expander("高级筛选"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not country_filter:
                    countries = ["全部"] + df['Country'].unique().tolist()
                    selected_country = st.selectbox("国家", countries)
                    if selected_country != "全部":
                        df = df[df['Country'] == selected_country]
            
            with col2:
                models = ["全部"] + df['Model'].unique().tolist()
                selected_model = st.selectbox("产品型号", models)
                if selected_model != "全部":
                    df = df[df['Model'] == selected_model]
            
            with col3:
                if 'h_Time' in df.columns:
                    times = ["全部"] + sorted(df['h_Time'].unique().tolist(), reverse=True)
                    selected_time = st.selectbox("时间周期", times)
                    if selected_time != "全部":
                        df = df[df['h_Time'] == selected_time]
        
        # 显示数据
        st.markdown("### 数据预览")
        st.dataframe(df, use_container_width=True, height=400)
        
        # 统计信息
        st.markdown("### 统计摘要")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("记录数", len(df))
        
        with col2:
            if 'Sales' in df.columns:
                st.metric("总销量", f"{df['Sales'].sum():,}")
        
        with col3:
            if 'Price' in df.columns:
                st.metric("平均价格", f"¥{df['Price'].mean():,.2f}")
        
        with col4:
            if 'Currency' in df.columns:
                currencies = df['Currency'].value_counts()
                st.metric("主要币种", currencies.index[0] if len(currencies) > 0 else "N/A")
        
        # 导出功能（如果有权限）
        if 'export' in permissions:
            st.markdown("---")
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="导出为CSV",
                data=csv,
                file_name=f"sales_price_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.warning("未找到销售价格数据")

if __name__ == "__main__":
    main()