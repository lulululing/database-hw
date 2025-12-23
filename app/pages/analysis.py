"""
数据分析对比页面
Data Analysis and Comparison Page
"""

import streamlit as st
import pandas as pd
from utils.database import get_db_manager


def show():
    """显示数据分析对比页面"""
    st.markdown('<div class="main-header">📈 数据分析对比</div>', unsafe_allow_html=True)
    
    if 'analyze' not in st.session_state.permissions:
        st.warning("⚠️ 您没有数据分析权限。")
        return
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 选择分析类型
    st.markdown("### 📊 选择分析类型")
    
    analysis_type = st.radio(
        "分析维度",
        options=["预算 vs 实际对比", "按国家汇总", "按产品汇总", "时间趋势分析"],
        horizontal=True
    )
    
    st.markdown("---")
    
    try:
        if analysis_type == "预算 vs 实际对比":
            show_comparison_analysis(db)
        elif analysis_type == "按国家汇总":
            show_country_summary(db)
        elif analysis_type == "按产品汇总":
            show_model_summary(db)
        elif analysis_type == "时间趋势分析":
            show_time_series_analysis(db)
    
    except Exception as e:
        st.error(f"❌ 分析失败: {str(e)}")
        st.info("💡 请检查数据库连接配置是否正确。")


def show_comparison_analysis(db):
    """预算vs实际对比分析"""
    st.markdown("### 📊 预算 vs 实际对比分析")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "选择时间期间",
        options=["全部"] + time_periods,
        index=0,
        key="comp_time"
    )
    
    # 获取对比数据
    df = db.get_comparison_data(selected_time if selected_time != "全部" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### 📋 对比数据")
        
        # 数据格式化
        df_display = df.copy()
        numeric_cols = ['实际销量', '预算销量', '实际收入', '预算收入', '实际净收入', '预算净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # 导出功能
        if 'export' in st.session_state.permissions:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 导出对比数据",
                    data=csv,
                    file_name=f"预算实际对比_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # 可视化
        st.markdown("---")
        st.markdown("#### 📊 可视化对比")
        
        tab1, tab2, tab3 = st.tabs(["销量对比", "收入对比", "净收入对比"])
        
        with tab1:
            if '实际销量' in df.columns and '预算销量' in df.columns:
                sales_data = df[['时间', '国家', '型号', '实际销量', '预算销量']].dropna()
                if not sales_data.empty:
                    sales_summary = sales_data.groupby('时间')[['实际销量', '预算销量']].sum()
                    st.bar_chart(sales_summary)
                else:
                    st.info("无销量对比数据")
        
        with tab2:
            if '实际收入' in df.columns and '预算收入' in df.columns:
                revenue_data = df[['时间', '国家', '型号', '实际收入', '预算收入']].dropna()
                if not revenue_data.empty:
                    revenue_summary = revenue_data.groupby('时间')[['实际收入', '预算收入']].sum()
                    st.line_chart(revenue_summary)
                else:
                    st.info("无收入对比数据")
        
        with tab3:
            if '实际净收入' in df.columns and '预算净收入' in df.columns:
                income_data = df[['时间', '国家', '型号', '实际净收入', '预算净收入']].dropna()
                if not income_data.empty:
                    income_summary = income_data.groupby('时间')[['实际净收入', '预算净收入']].sum()
                    st.area_chart(income_summary)
                else:
                    st.info("无净收入对比数据")
    
    else:
        st.warning("⚠️ 没有找到对比数据。")


def show_country_summary(db):
    """按国家汇总分析"""
    st.markdown("### 🌍 按国家汇总分析")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "选择时间期间",
        options=["全部"] + time_periods,
        index=0,
        key="country_time"
    )
    
    # 获取数据
    df = db.get_country_summary(selected_time if selected_time != "全部" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### 📋 国家汇总数据")
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🌍 国家数量",
                value=len(df)
            )
        
        with col2:
            st.metric(
                label="💰 总收入",
                value=f"¥{df['总收入'].sum():,.2f}"
            )
        
        with col3:
            st.metric(
                label="💵 总净收入",
                value=f"¥{df['总净收入'].sum():,.2f}"
            )
        
        st.markdown("---")
        
        # 数据表格
        df_display = df.copy()
        numeric_cols = ['总收入', '总毛利', '总净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}")
        
        for col in ['毛利率', '净利率']:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### 📊 可视化分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 各国总收入")
            st.bar_chart(df.set_index('国家')['总收入'])
        
        with col2:
            st.markdown("##### 各国净利率")
            st.bar_chart(df.set_index('国家')['净利率'])
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 导出国家汇总",
                    data=csv,
                    file_name=f"国家汇总_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("⚠️ 没有找到国家汇总数据。")


def show_model_summary(db):
    """按产品汇总分析"""
    st.markdown("### 📱 按产品汇总分析")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "选择时间期间",
        options=["全部"] + time_periods,
        index=0,
        key="model_time"
    )
    
    # 获取数据
    df = db.get_model_summary(selected_time if selected_time != "全部" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### 📋 产品汇总数据")
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📱 产品型号数",
                value=len(df)
            )
        
        with col2:
            st.metric(
                label="📦 总销量",
                value=f"{df['总销量'].sum():,}"
            )
        
        with col3:
            st.metric(
                label="💰 总收入",
                value=f"¥{df['总收入'].sum():,.2f}"
            )
        
        st.markdown("---")
        
        # 数据表格
        df_display = df.copy()
        numeric_cols = ['总收入', '总毛利', '总净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}")
        
        if '平均毛利率' in df_display.columns:
            df_display['平均毛利率'] = df_display['平均毛利率'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### 📊 可视化分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 各型号销量")
            st.bar_chart(df.set_index('型号')['总销量'])
        
        with col2:
            st.markdown("##### 各型号收入")
            st.bar_chart(df.set_index('型号')['总收入'])
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 导出产品汇总",
                    data=csv,
                    file_name=f"产品汇总_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("⚠️ 没有找到产品汇总数据。")


def show_time_series_analysis(db):
    """时间趋势分析"""
    st.markdown("### 📅 时间趋势分析")
    
    # 获取时间序列数据
    df = db.get_time_series_data()
    
    if df is not None and not df.empty:
        st.markdown("#### 📋 时间序列数据")
        
        # 数据表格
        df_display = df.copy()
        numeric_cols = ['总收入', '总毛利', '总净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### 📊 趋势图表")
        
        tab1, tab2, tab3 = st.tabs(["综合趋势", "销量趋势", "收入与利润趋势"])
        
        with tab1:
            st.line_chart(df.set_index('时间')[['总销量', '总收入', '总净收入']])
        
        with tab2:
            st.area_chart(df.set_index('时间')['总销量'])
        
        with tab3:
            st.line_chart(df.set_index('时间')[['总收入', '总毛利', '总净收入']])
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 导出时间序列",
                    data=csv,
                    file_name=f"时间序列_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("⚠️ 没有找到时间序列数据。")
