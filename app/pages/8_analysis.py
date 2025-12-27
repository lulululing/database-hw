import streamlit as st
import pandas as pd
from utils.database import get_db_manager
import plotly.express as px
import plotly.graph_objects as go

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限
if 'analyze' not in st.session_state.get('permissions', []):
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="报表分析",
    layout="wide"
)
st.title("预算与预测对比分析")

def main():
    """数据分析对比页面（改进：预算vs预测）"""
    st.markdown('<div class="main-header">Budget vs Forecast Analysis</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 选择分析类型
    st.markdown("### Select Analysis Type")
    
    analysis_type = st.radio(
        "Analysis Dimension",
        options=[
            "Budget vs Forecast Comparison", 
            "Time Period Breakdown",  # 新增
            "Country Summary", 
            "Product Summary"
        ],
        horizontal=True
    )
    
    st.markdown("---")
    
    try:
        if analysis_type == "Budget vs Forecast Comparison":
            show_comparison_analysis(db)
        elif analysis_type == "Time Period Breakdown":
            show_time_breakdown_analysis(db)  # 新增
        elif analysis_type == "Country Summary":
            show_country_summary(db)
        elif analysis_type == "Product Summary":
            show_product_summary(db)
    
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.info("Please check if the database connection configuration is correct.")

def show_comparison_analysis(db):
    """改进：预算vs预测对比分析（而不是预算vs历史）"""
    st.markdown("### Budget vs Forecast Comparison")
    st.info("📊 Compare **Budget** (planned) vs **Forecast** (predicted) data")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "Select Time Period",
        options=["All"] + time_periods,
        index=0
    )
    
    # 获取对比数据（已改为预算vs预测）
    df = db.get_comparison_data(selected_time if selected_time != "All" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### Comparison Data")
        
        # 计算差异列
        df['销量差异'] = df['预测销量'] - df['预算销量']
        df['收入差异'] = df['预测收入'] - df['预算收入']
        df['毛利差异'] = df['预测毛利'] - df['预算毛利']
        df['净利差异'] = df['预测净利'] - df['预算净利']
        
        # 数据格式化
        df_display = df.copy()
        numeric_cols = ['预测销量', '预算销量', '销量差异', '预测收入', '预算收入', '收入差异', 
                       '预测毛利', '预算毛利', '毛利差异', '预测净利', '预算净利', '净利差异']
        
        for col in numeric_cols:
            if col in df_display.columns:
                if '销量' in col or '差异' in col and '收入' not in col and '利' not in col:
                    df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
                else:
                    df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # 导出功能
        if 'export' in st.session_state.permissions:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Export Comparison Data",
                    data=csv,
                    file_name=f"Budget_Forecast_Comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        tab1, tab2, tab3 = st.tabs(["📈 Sales Comparison", "💰 Revenue Comparison", "📊 Profit Comparison"])
        
        with tab1:
            if '预测销量' in df.columns and '预算销量' in df.columns:
                sales_data = df[['h_Time', 'Country', 'Model', '预测销量', '预算销量']].dropna()
                if not sales_data.empty:
                    sales_summary = sales_data.groupby('h_Time')[['预测销量', '预算销量']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Forecast', x=sales_summary['h_Time'], y=sales_summary['预测销量']))
                    fig.add_trace(go.Bar(name='Budget', x=sales_summary['h_Time'], y=sales_summary['预算销量']))
                    fig.update_layout(barmode='group', title='Sales: Budget vs Forecast')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No sales comparison data")
        
        with tab2:
            if '预测收入' in df.columns and '预算收入' in df.columns:
                revenue_data = df[['h_Time', 'Country', 'Model', '预测收入', '预算收入']].dropna()
                if not revenue_data.empty:
                    revenue_summary = revenue_data.groupby('h_Time')[['预测收入', '预算收入']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(name='Forecast', x=revenue_summary['h_Time'], y=revenue_summary['预测收入'], mode='lines+markers'))
                    fig.add_trace(go.Scatter(name='Budget', x=revenue_summary['h_Time'], y=revenue_summary['预算收入'], mode='lines+markers'))
                    fig.update_layout(title='Revenue: Budget vs Forecast', yaxis_title='Revenue (¥)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No revenue comparison data")
        
        with tab3:
            if '预测净利' in df.columns and '预算净利' in df.columns:
                profit_data = df[['h_Time', 'Country', 'Model', '预测净利', '预算净利']].dropna()
                if not profit_data.empty:
                    profit_summary = profit_data.groupby('h_Time')[['预测净利', '预算净利']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(name='Forecast', x=profit_summary['h_Time'], y=profit_summary['预测净利'], 
                                           mode='lines+markers', fill='tozeroy'))
                    fig.add_trace(go.Scatter(name='Budget', x=profit_summary['h_Time'], y=profit_summary['预算净利'], 
                                           mode='lines+markers', fill='tozeroy'))
                    fig.update_layout(title='Net Income: Budget vs Forecast', yaxis_title='Net Income (¥)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No profit comparison data")
    
    else:
        st.warning("No comparison data found.")

def show_time_breakdown_analysis(db):
    """
    新增：国家总数据按时间段拆分对比
    显示各个时间段的国家汇总对比
    """
    st.markdown("### Time Period Breakdown by Country")
    st.info("📅 View country-level metrics broken down by time period")
    
    # 获取所有时间段
    time_periods = db.get_all_time_periods()
    
    if not time_periods:
        st.warning("No time period data available")
        return
    
    # 选择多个时间段进行对比
    selected_times = st.multiselect(
        "Select Time Periods to Compare",
        options=time_periods,
        default=time_periods[:min(3, len(time_periods))]  # 默认选择前3个
    )
    
    if not selected_times:
        st.info("Please select at least one time period")
        return
    
    # 获取各时间段的国家汇总数据
    all_data = []
    for time_period in selected_times:
        df_time = db.get_country_summary(time_period)
        if df_time is not None and not df_time.empty:
            df_time['Time Period'] = time_period
            all_data.append(df_time)
    
    if not all_data:
        st.warning("No data found for selected time periods")
        return
    
    # 合并数据
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # 数据展示
    st.markdown("#### Country Summary by Time Period")
    
    # 重新排列列顺序
    df_display = df_combined[['Time Period', 'Country', '总销量', '总收入', '总毛利', '总净收入']].copy()
    
    # 格式化显示
    df_display['总销量'] = df_display['总销量'].apply(lambda x: f"{x:,.0f}")
    df_display['总收入'] = df_display['总收入'].apply(lambda x: f"¥{x:,.2f}")
    df_display['总毛利'] = df_display['总毛利'].apply(lambda x: f"¥{x:,.2f}")
    df_display['总净收入'] = df_display['总净收入'].apply(lambda x: f"¥{x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # 可视化对比
    st.markdown("---")
    st.markdown("#### Visual Comparison")
    
    tab1, tab2, tab3 = st.tabs(["📊 Revenue Trends", "💵 Net Income Trends", "🌍 Country Heatmap"])
    
    with tab1:
        # 收入趋势对比
        fig = px.line(df_combined, x='Time Period', y='总收入', color='Country',
                     title='Revenue Trends by Country',
                     markers=True)
        fig.update_layout(yaxis_title='Revenue (¥)', xaxis_title='Time Period')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # 净收入趋势对比
        fig = px.bar(df_combined, x='Time Period', y='总净收入', color='Country',
                    title='Net Income by Country and Time',
                    barmode='group')
        fig.update_layout(yaxis_title='Net Income (¥)', xaxis_title='Time Period')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # 热力图：国家 x 时间段
        pivot_data = df_combined.pivot(index='Country', columns='Time Period', values='总收入')
        fig = px.imshow(pivot_data, 
                       labels=dict(x="Time Period", y="Country", color="Revenue (¥)"),
                       title="Revenue Heatmap: Country × Time",
                       aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    
    # 导出功能
    if 'export' in st.session_state.permissions:
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            csv = df_combined.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Export Time Breakdown",
                data=csv,
                file_name=f"Time_Breakdown_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

def show_country_summary(db):
    """按国家汇总分析（使用预测数据Display）"""
    st.markdown("### Country Summary Analysis (Forecast Data)")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "Select Time Period",
        options=["All"] + time_periods,
        index=0,
        key="country_time"
    )
    
    # 获取数据
    df = db.get_country_summary(selected_time if selected_time != "All" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### Country Summary Data")
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Countries", len(df))
        
        with col2:
            st.metric("Total Revenue", f"¥{df['总收入'].sum():,.2f}")
        
        with col3:
            st.metric("Total Net Income", f"¥{df['总净收入'].sum():,.2f}")
        
        st.markdown("---")
        
        # 数据表格
        df_display = df.copy()
        df_display['总销量'] = df_display['总销量'].apply(lambda x: f"{x:,.0f}")
        df_display['总收入'] = df_display['总收入'].apply(lambda x: f"¥{x:,.2f}")
        df_display['总毛利'] = df_display['总毛利'].apply(lambda x: f"¥{x:,.2f}")
        df_display['总净收入'] = df_display['总净收入'].apply(lambda x: f"¥{x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Revenue by Country")
            fig = px.bar(df, x='Country', y='总收入', title='Forecast Revenue by Country')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Net Income by Country")
            fig = px.bar(df, x='Country', y='总净收入', title='Forecast Net Income by Country', color='总净收入')
            st.plotly_chart(fig, use_container_width=True)
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Export Country Summary",
                    data=csv,
                    file_name=f"Country_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("No country summary data found.")

def show_product_summary(db):
    """按产品汇总分析（使用预测数据Display）"""
    st.markdown("### Product Summary Analysis (Forecast Data)")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "Select Time Period",
        options=["All"] + time_periods,
        index=0,
        key="model_time"
    )
    
    # 获取数据
    df = db.get_model_summary(selected_time if selected_time != "All" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### Product Summary Data")
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Product Models", len(df))
        
        with col2:
            st.metric("Total Sales", f"{df['总销量'].sum():,}")
        
        with col3:
            st.metric("Total Revenue", f"¥{df['总收入'].sum():,.2f}")
        
        st.markdown("---")
        
        # 数据表格
        df_display = df.copy()
        df_display['总销量'] = df_display['总销量'].apply(lambda x: f"{x:,.0f}")
        df_display['总收入'] = df_display['总收入'].apply(lambda x: f"¥{x:,.2f}")
        df_display['总毛利'] = df_display['总毛利'].apply(lambda x: f"¥{x:,.2f}")
        df_display['总净收入'] = df_display['总净收入'].apply(lambda x: f"¥{x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Sales by Product")
            fig = px.bar(df, x='Model', y='总销量', title='Forecast Sales by Product')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Revenue by Product")
            fig = px.pie(df, values='总收入', names='Model', title='Revenue Distribution by Product')
            st.plotly_chart(fig, use_container_width=True)
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Export Product Summary",
                    data=csv,
                    file_name=f"Product_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("No product summary data found.")

if __name__ == "__main__":
    main()