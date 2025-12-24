# pages/8_📈_Data_Analysis.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager
import plotly.express as px

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
st.title("报表分析")
def main():
    """数据分析对比页面"""
    st.markdown('<div class="main-header">📈 Data Analysis & Comparison</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 选择分析类型
    st.markdown("### Select Analysis Type")
    
    analysis_type = st.radio(
        "Analysis Dimension",
        options=["Budget vs Actual Comparison", "Country Summary", "Product Summary", "Time Trend Analysis"],
        horizontal=True
    )
    
    st.markdown("---")
    
    try:
        if analysis_type == "Budget vs Actual Comparison":
            show_comparison_analysis(db)
        elif analysis_type == "Country Summary":
            show_country_summary(db)
        elif analysis_type == "Product Summary":
            show_product_summary(db)
        elif analysis_type == "Time Trend Analysis":
            show_time_trend_analysis(db)
    
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.info("Please check if the database connection configuration is correct.")

def show_comparison_analysis(db):
    """预算vs实际对比分析"""
    st.markdown("### Budget vs Actual Comparison")
    
    # 选择时间期间
    time_periods = db.get_all_time_periods()
    selected_time = st.selectbox(
        "Select Time Period",
        options=["All"] + time_periods,
        index=0
    )
    
    # 获取对比数据
    df = db.get_comparison_data(selected_time if selected_time != "All" else None)
    
    if df is not None and not df.empty:
        st.markdown("#### Comparison Data")
        
        # 数据格式化
        df_display = df.copy()
        numeric_cols = ['实际销量', '预算销量', '实际收入', '预算收入', '实际毛利', '预算毛利']
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
                    label="Export Comparison Data",
                    data=csv,
                    file_name=f"Budget_Actual_Comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        tab1, tab2, tab3 = st.tabs(["Sales Comparison", "Revenue Comparison", "Profit Comparison"])
        
        with tab1:
            if '实际销量' in df.columns and '预算销量' in df.columns:
                sales_data = df[['h_Time', 'Country', 'Model', '实际销量', '预算销量']].dropna()
                if not sales_data.empty:
                    sales_summary = sales_data.groupby('h_Time')[['实际销量', '预算销量']].sum()
                    st.bar_chart(sales_summary)
                else:
                    st.info("No sales comparison data")
        
        with tab2:
            if '实际收入' in df.columns and '预算收入' in df.columns:
                revenue_data = df[['h_Time', 'Country', 'Model', '实际收入', '预算收入']].dropna()
                if not revenue_data.empty:
                    revenue_summary = revenue_data.groupby('h_Time')[['实际收入', '预算收入']].sum()
                    st.line_chart(revenue_summary)
                else:
                    st.info("No revenue comparison data")
        
        with tab3:
            if '实际毛利' in df.columns and '预算毛利' in df.columns:
                profit_data = df[['h_Time', 'Country', 'Model', '实际毛利', '预算毛利']].dropna()
                if not profit_data.empty:
                    profit_summary = profit_data.groupby('h_Time')[['实际毛利', '预算毛利']].sum()
                    st.area_chart(profit_summary)
                else:
                    st.info("No profit comparison data")
    
    else:
        st.warning("No comparison data found.")

def show_country_summary(db):
    """按国家汇总分析"""
    st.markdown("### Country Summary Analysis")
    
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
        numeric_cols = ['总收入', '总毛利', '总净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Revenue by Country")
            st.bar_chart(df.set_index('Country')['总收入'])
        
        with col2:
            st.markdown("##### Net Income by Country")
            st.bar_chart(df.set_index('Country')['总净收入'])
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Export Country Summary",
                    data=csv,
                    file_name=f"Country_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("No country summary data found.")

def show_product_summary(db):
    """按产品汇总分析"""
    st.markdown("### Product Summary Analysis")
    
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
        numeric_cols = ['总收入', '总毛利', '总净收入']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"¥{x:,.2f}")
        
        if '平均毛利率' in df_display.columns:
            df_display['平均毛利率'] = df_display['平均毛利率'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df_display, use_container_width=True)
        
        # 可视化
        st.markdown("---")
        st.markdown("#### Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Sales by Product")
            st.bar_chart(df.set_index('Model')['总销量'])
        
        with col2:
            st.markdown("##### Revenue by Product")
            st.bar_chart(df.set_index('Model')['总收入'])
        
        # 导出
        if 'export' in st.session_state.permissions:
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Export Product Summary",
                    data=csv,
                    file_name=f"Product_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.warning("No product summary data found.")

def show_time_trend_analysis(db):
    """时间趋势分析"""
    st.markdown("### Time Trend Analysis")
    
    # 选择指标
    metrics = st.multiselect(
        "Select Metrics to Display",
        ["Sales", "Revenue", "Gross Profit", "Net Income"],
        default=["Revenue", "Net Income"]
    )
    
    # 获取基础数据
    df_history = db.get_history_data()
    
    if df_history is not None and not df_history.empty:
        # 按时间汇总
        time_summary = df_history.groupby('h_Time').agg({
            'Sales': 'sum',
            'Revenues': 'sum',
            'Gross_profits': 'sum',
            'Net_income': 'sum'
        }).reset_index()
        
        # 重命名列
        time_summary.columns = ['Time', 'Sales', 'Revenue', 'Gross Profit', 'Net Income']
        
        # 创建图表
        if metrics:
            # 使用Plotly创建交互式图表
            fig = px.line(time_summary, x='Time', y=metrics,
                         title='Financial Metrics Trend',
                         markers=True)
            
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="Time Period",
                yaxis_title="Value (¥)",
                legend_title="Metrics"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select at least one metric to display")
        
        # 显示数据表
        with st.expander("View Trend Data"):
            st.dataframe(time_summary, use_container_width=True)
            
            # 导出功能
            if 'export' in st.session_state.permissions:
                csv = time_summary.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Export Trend Data",
                    data=csv,
                    file_name=f"Time_Trend_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    else:
        st.warning("No time series data available.")

if __name__ == "__main__":
    main()