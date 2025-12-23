"""
成本数据页面
Costs Data Page
"""

import streamlit as st
import pandas as pd
from utils.database import get_db_manager


def show():
    """显示成本数据页面"""
    st.markdown('<div class="main-header">💸 成本数据</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    try:
        df = db.get_costs_data()
        
        if df is not None and not df.empty:
            # 显示统计信息
            st.markdown("### 📈 成本统计")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📝 记录数",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="💰 平均成本",
                    value=f"¥{df['成本'].mean():.2f}"
                )
            
            with col3:
                st.metric(
                    label="📉 最低成本",
                    value=f"¥{df['成本'].min():.2f}"
                )
            
            with col4:
                st.metric(
                    label="📈 最高成本",
                    value=f"¥{df['成本'].max():.2f}"
                )
            
            st.markdown("---")
            
            # 显示数据表格
            st.markdown("### 📋 详细数据")
            
            # 数据格式化
            df_display = df.copy()
            df_display['成本'] = df_display['成本'].apply(lambda x: f"¥{x:.2f}")
            
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
                        label="📥 导出为 CSV",
                        data=csv,
                        file_name=f"成本数据_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # 图表展示
            if 'analyze' in st.session_state.permissions:
                st.markdown("---")
                st.markdown("### 📊 成本分析")
                
                tab1, tab2 = st.tabs(["按国家", "按产品型号"])
                
                with tab1:
                    country_summary = df.groupby('国家')['成本'].mean().reset_index()
                    st.bar_chart(country_summary.set_index('国家'))
                
                with tab2:
                    model_summary = df.groupby('型号')['成本'].mean().reset_index()
                    st.bar_chart(model_summary.set_index('型号'))
        
        else:
            st.warning("⚠️ 没有找到成本数据。")
    
    except Exception as e:
        st.error(f"❌ 查询失败: {str(e)}")
        st.info("💡 请检查数据库连接配置是否正确。")
