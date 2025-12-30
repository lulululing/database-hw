import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 检查权限 - 扩展：业务员也能查看
view_perms = ['view_history', 'view_history_country']
has_permission = any(perm in st.session_state.get('permissions', []) for perm in view_perms)

if not has_permission:
    st.error("您没有权限访问此页面")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="历史数据",
    layout="wide"
)

def main():
    st.title("历史数据查询")
    
    # 获取用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    permissions = st.session_state.permissions
    db = get_db_manager()
    
    # 根据角色显示提示
    if u.get('country'):
        st.info(f"当前区域: **{u['country']}** (您只能查看本国数据)")
        country_filter = u['country']
        country_disabled = True
    else:
        st.info("您可以查看所有国家的历史数据")
        country_filter = None
        country_disabled = False
    
    # 筛选条件
    st.markdown("### 筛选条件")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox("时间周期", ["全部"] + time_periods)
    
    with col2:
        if country_disabled:
            selected_country = st.text_input("国家", country_filter, disabled=True)
        else:
            countries = ["全部"] + db.get_all_countries()
            selected_country = st.selectbox("国家", countries)
    
    with col3:
        models = ["全部"] + db.get_all_models()
        selected_model = st.selectbox("产品型号", models)
    
    # 查询按钮
    if st.button("查询数据", type="primary", use_container_width=True):
        with st.spinner("查询中..."):
            try:
                # 构建筛选条件
                filters = {}
                
                if selected_time != "全部":
                    filters['time'] = selected_time
                
                if country_disabled:
                    filters['country'] = country_filter
                elif selected_country != "全部":
                    filters['country'] = selected_country
                
                if selected_model != "全部":
                    filters['model'] = selected_model
                
                # 查询数据
                df = db.get_history_data(filters)
                
                if not df.empty:
                    st.success(f"找到 {len(df)} 条记录")
                    
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
                        if 'Revenues' in df.columns:
                            st.metric("总收入", f"¥{df['Revenues'].sum():,.2f}")
                    
                    with col4:
                        if 'Net_income' in df.columns:
                            st.metric("总净利润", f"¥{df['Net_income'].sum():,.2f}")
                    
                    # 导出功能（如果有权限）
                    if 'export' in permissions:
                        st.markdown("---")
                        csv = df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="导出为CSV",
                            data=csv,
                            file_name=f"history_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("未找到符合条件的数据")
                    
            except Exception as e:
                st.error(f"查询失败: {str(e)}")

if __name__ == "__main__":
    main()