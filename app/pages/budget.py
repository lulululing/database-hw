"""
预算数据查询页面
Budget Data Query Page
"""

import streamlit as st
import pandas as pd
from utils.database import get_db_manager


def show():
    """显示预算数据查询页面"""
    st.markdown('<div class="main-header">💰 预算数据查询</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 筛选条件
    st.markdown("### 🔍 查询条件")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox(
            "选择时间",
            options=["全部"] + time_periods,
            index=0,
            key="budget_time"
        )
    
    with col2:
        countries = db.get_all_countries()
        selected_country = st.selectbox(
            "选择国家",
            options=["全部"] + countries,
            index=0,
            key="budget_country"
        )
    
    with col3:
        models = db.get_all_models()
        selected_model = st.selectbox(
            "选择产品型号",
            options=["全部"] + models,
            index=0,
            key="budget_model"
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 查询", use_container_width=True, type="primary", key="budget_search")
    
    st.markdown("---")
    
    # 构建筛选条件
    filters = {}
    if selected_time != "全部":
        filters['time'] = selected_time
    if selected_country != "全部":
        filters['country'] = selected_country
    if selected_model != "全部":
        filters['model'] = selected_model
    
    # 获取数据
    try:
        df = db.get_budget_data(filters if filters else None)
        
        if df is not None and not df.empty:
            # 显示统计信息
            st.markdown("### 📈 预算统计")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    label="📝 记录数",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="📦 预算销量",
                    value=f"{df['销量'].sum():,}"
                )
            
            with col3:
                st.metric(
                    label="💰 预算收入",
                    value=f"¥{df['收入'].sum():,.2f}"
                )
            
            with col4:
                st.metric(
                    label="💵 预算毛利",
                    value=f"¥{df['毛利'].sum():,.2f}"
                )
            
            with col5:
                st.metric(
                    label="💸 预算净收入",
                    value=f"¥{df['净收入'].sum():,.2f}"
                )
            
            st.markdown("---")
            
            # 显示数据表格
            st.markdown("### 📋 详细数据")
            
            # 添加数据格式化
            df_display = df.copy()
            df_display['收入'] = df_display['收入'].apply(lambda x: f"¥{x:,.2f}")
            df_display['毛利'] = df_display['毛利'].apply(lambda x: f"¥{x:,.2f}")
            df_display['边际利润'] = df_display['边际利润'].apply(lambda x: f"¥{x:,.2f}")
            df_display['净收入'] = df_display['净收入'].apply(lambda x: f"¥{x:,.2f}")
            
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
                        label="📥 导出为 CSV",
                        data=csv,
                        file_name=f"预算数据_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # 图表展示
            if 'analyze' in st.session_state.permissions:
                st.markdown("---")
                st.markdown("### 📊 预算可视化")
                
                tab1, tab2, tab3 = st.tabs(["按时间", "按国家", "按产品"])
                
                with tab1:
                    time_summary = df.groupby('时间').agg({
                        '销量': 'sum',
                        '收入': 'sum',
                        '净收入': 'sum'
                    }).reset_index()
                    st.line_chart(time_summary.set_index('时间'))
                
                with tab2:
                    country_summary = df.groupby('国家').agg({
                        '销量': 'sum',
                        '收入': 'sum',
                        '净收入': 'sum'
                    }).reset_index()
                    st.bar_chart(country_summary.set_index('国家'))
                
                with tab3:
                    model_summary = df.groupby('型号').agg({
                        '销量': 'sum',
                        '收入': 'sum',
                        '净收入': 'sum'
                    }).reset_index()
                    st.bar_chart(model_summary.set_index('型号'))
        
        else:
            st.warning("⚠️ 没有找到符合条件的预算数据。")
    
    except Exception as e:
        st.error(f"❌ 查询失败: {str(e)}")
        st.info("💡 请检查数据库连接配置是否正确。")
