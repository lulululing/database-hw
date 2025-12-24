# pages/4_📜_History_Data.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限
if 'view_history' not in st.session_state.get('permissions', []):
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="历史记录",
    layout="wide"
)

st.title("历史记录")
def main():
    """历史数据查询页面"""
    st.markdown('<div class="main-header">📜 History Data Query</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 筛选条件
    st.markdown("### 🔍 Query Conditions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # 获取时间列表
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox(
            "Select Time Period",
            options=["All"] + time_periods,
            index=0
        )
    
    with col2:
        # 获取国家列表
        countries = db.get_all_countries()
        selected_country = st.selectbox(
            "Select Country",
            options=["All"] + countries,
            index=0
        )
    
    with col3:
        # 获取型号列表
        models = db.get_all_models()
        selected_model = st.selectbox(
            "Select Product Model",
            options=["All"] + models,
            index=0
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
    
    st.markdown("---")
    
    # 构建筛选条件
    filters = {}
    if selected_time != "All":
        filters['time'] = selected_time
    if selected_country != "All":
        filters['country'] = selected_country
    if selected_model != "All":
        filters['model'] = selected_model
    
    # 获取数据
    try:
        df = db.get_history_data(filters if filters else None)
        
        if df is not None and not df.empty:
            # 显示统计信息
            st.markdown("### 📈 Data Statistics")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    label="📝 Records",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="📦 Total Sales",
                    value=f"{df['Sales'].sum():,}"
                )
            
            with col3:
                st.metric(
                    label="💰 Total Revenue",
                    value=f"¥{df['Revenues'].sum():,.2f}"
                )
            
            with col4:
                st.metric(
                    label="💵 Total Gross Profit",
                    value=f"¥{df['Gross_profits'].sum():,.2f}"
                )
            
            with col5:
                st.metric(
                    label="💸 Total Net Income",
                    value=f"¥{df['Net_income'].sum():,.2f}"
                )
            
            st.markdown("---")
            
            # 显示数据表格
            st.markdown("### 📋 Detailed Data")
            
            # 添加数据格式化
            df_display = df.copy()
            df_display['Revenues'] = df_display['Revenues'].apply(lambda x: f"¥{x:,.2f}")
            df_display['Gross_profits'] = df_display['Gross_profits'].apply(lambda x: f"¥{x:,.2f}")
            df_display['Margin_profits'] = df_display['Margin_profits'].apply(lambda x: f"¥{x:,.2f}")
            df_display['Net_income'] = df_display['Net_income'].apply(lambda x: f"¥{x:,.2f}")
            
            st.dataframe(
                df_display,
                use_container_width=True,
                height=400
            )
            
            # 导出功能
            if 'export' in st.session_state.permissions:
                st.markdown("---")
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Export as CSV",
                        data=csv,
                        file_name=f"History_Data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        else:
            st.warning("⚠️ No data found matching the criteria.")
    
    except Exception as e:
        st.error(f"❌ Query failed: {str(e)}")
        st.info("💡 Please check if the database connection configuration is correct.")

if __name__ == "__main__":
    main()