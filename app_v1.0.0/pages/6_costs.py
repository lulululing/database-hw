# pages/6_💸_Cost_Details.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限
if 'view_costs' not in st.session_state.get('permissions', []):
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="查看成本",
    layout="wide"
)
st.title("查看成本")
def main():
    """成本数据页面"""
    st.markdown('<div class="main-header">💸 Cost Details</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    try:
        df = db.get_costs_data()
        
        if df is not None and not df.empty:
            # 显示统计信息
            st.markdown("### 📈 Cost Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📝 Records",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="💰 Average Cost",
                    value=f"¥{df['Costs'].mean():.2f}"
                )
            
            with col3:
                st.metric(
                    label="📉 Min Cost",
                    value=f"¥{df['Costs'].min():.2f}"
                )
            
            with col4:
                st.metric(
                    label="📈 Max Cost",
                    value=f"¥{df['Costs'].max():.2f}"
                )
            
            st.markdown("---")
            
            # 显示数据表格
            st.markdown("### 📋 Detailed Data")
            
            # 数据格式化
            df_display = df.copy()
            df_display['Costs'] = df_display['Costs'].apply(lambda x: f"¥{x:.2f}")
            
            st.dataframe(
                df_display,
                use_container_width=True,
                height=500
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
                        file_name=f"Cost_Data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # 图表展示
            if 'analyze' in st.session_state.permissions:
                st.markdown("---")
                st.markdown("### 📊 Cost Analysis")
                
                tab1, tab2 = st.tabs(["By Country", "By Product Model"])
                
                with tab1:
                    country_summary = df.groupby('Country')['Costs'].mean().reset_index()
                    st.bar_chart(country_summary.set_index('Country'))
                
                with tab2:
                    model_summary = df.groupby('Model')['Costs'].mean().reset_index()
                    st.bar_chart(model_summary.set_index('Model'))
        
        else:
            st.warning("⚠️ No cost data found.")
    
    except Exception as e:
        st.error(f"❌ Query failed: {str(e)}")
        st.info("💡 Please check if the database connection configuration is correct.")

if __name__ == "__main__":
    main()