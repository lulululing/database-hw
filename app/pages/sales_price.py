"""
销售价格数据页面
Sales Price Data Page
"""

import streamlit as st
import pandas as pd
from utils.database import get_db_manager


def show():
    """显示销售价格数据页面"""
    st.markdown('<div class="main-header">💵 销售价格数据</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    try:
        df = db.get_sales_price_data()
        
        if df is not None and not df.empty:
            # 显示统计信息
            st.markdown("### 📈 数据统计")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📝 记录数",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="📦 总销量",
                    value=f"{df['销量'].sum():,}"
                )
            
            with col3:
                st.metric(
                    label="💰 平均价格 (USD)",
                    value=f"${df['价格'].mean():.2f}"
                )
            
            with col4:
                st.metric(
                    label="💵 价格区间",
                    value=f"${df['价格'].min():.2f} - ${df['价格'].max():.2f}"
                )
            
            st.markdown("---")
            
            # 显示数据表格
            st.markdown("### 📋 详细数据")
            
            # 数据格式化
            df_display = df.copy()
            df_display['价格'] = df_display['价格'].apply(lambda x: f"${x:.2f}")
            
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
                        file_name=f"销售价格_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        else:
            st.warning("⚠️ 没有找到销售价格数据。")
    
    except Exception as e:
        st.error(f"❌ 查询失败: {str(e)}")
        st.info("💡 请检查数据库连接配置是否正确。")
