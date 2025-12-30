import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from utils.database import get_db_manager
from utils.helper import apply_currency_conversion
from utils.i18n import show_sidebar_with_nav, get_text

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_warning'))  # 修改：login_required → login_warning
    st.switch_page("app.py")

# 检查权限
if 'analyze' not in st.session_state.get('permissions', []):
    st.error(get_text('no_permission'))
    st.stop()

# 设置页面
st.set_page_config(
    page_title=get_text('nav_analysis'),
    layout="wide"
)

# 显示侧边栏导航 - 这是关键修复！
show_sidebar_with_nav()
st.title(get_text('nav_analysis'))

def log_view_action(db, page_name, analysis_type, filter_details=""):
    """记录查看操作的日志"""
    try:
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        details = f"查看{page_name}页面 - {analysis_type}分析"
        if filter_details:
            details += f" | 筛选条件: {filter_details}"
        
        from utils.helper import handle_save_success
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="VIEW",
            message_prefix="数据分析",
            details=details,
            operation_type="查看"
        )
    except Exception as e:
        st.warning(f"记录日志失败: {e}")
        return False

def log_export_action(db, page_name, analysis_type, export_type, record_count):
    """记录导出操作的日志"""
    try:
        user_info = {
            'id': st.session_state.get('user_id', ''),
            'username': st.session_state.get('username', ''),
            'role': st.session_state.get('role', 'User')
        }
        
        details = f"导出{page_name}页面 - {analysis_type}分析数据({export_type}), 记录数: {record_count}"
        
        from utils.helper import handle_save_success
        return handle_save_success(
            db=db,
            user_info=user_info,
            action_type="EXPORT",
            message_prefix="数据导出",
            details=details,
            operation_type="导出"
        )
    except Exception as e:
        print(f"记录导出日志失败: {e}")
        return False

def main():
    """数据分析对比页面（改进：预算vs预测）"""
    
    # 获取数据库管理器
    db = get_db_manager()
    
    # 创建Tab标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text('analysis_opt_comparison'),
        get_text('analysis_opt_time'),
        get_text('analysis_opt_country'),
        get_text('analysis_opt_product')
    ])
    
    with tab1:
        show_comparison_analysis(db)
    
    with tab2:
        show_time_breakdown_analysis(db)
    
    with tab3:
        show_country_summary(db)
    
    with tab4:
        show_product_summary(db)

def show_comparison_analysis(db):
    """改进：预算vs预测对比分析（而不是预算vs历史）"""
    
    # ========== 筛选条件区域 ==========
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_periods = db.get_all_time_periods()
        if not time_periods:
            st.warning(get_text('msg_no_time_data'))  # 修改：硬编码中文 → get_text
            return
        
        selected_time = st.selectbox(
            get_text('select_time'),
            options=[get_text('view_all_option')] + time_periods,
            index=0
        )
    
    with col2:
        # 货币选择
        default_idx = 0 if st.session_state.get('language') == 'zh' else 1
        currency_opt = st.selectbox(
            get_text('currency'),
            ["CNY", "USD"],
            index=default_idx,
            key="comp_curr"
        )
    
    # 记录查看日志
    filter_details = []
    if selected_time != get_text('view_all_option'):
        filter_details.append(f"时间: {selected_time}")
    filter_details.append(f"货币: {currency_opt}")
    
    log_view_action(
        db=db,
        page_name=get_text('nav_analysis'),
        analysis_type="预算vs预测对比",
        filter_details="; ".join(filter_details)
    )
    
    # 获取对比数据（已改为预算vs预测）
    time_param = selected_time if selected_time != get_text('view_all_option') else None
    df = db.get_comparison_data(time_param)
    
    if df is not None and not df.empty:
        # 应用货币转换
        df_converted, currency_symbol = apply_currency_conversion(df, db, currency_opt)
        
        # 显示数据统计信息 - 使用i18n
        st.info(get_text('msg_found_records').format(count=len(df_converted)))
        
        # 计算差异列（使用转换后的数据）
        df_display = df_converted.copy()
        
        # 为差异列使用i18n键值（需要在i18n.py中添加）
        df_display[get_text('col_sales_diff')] = df_display['预测销量'] - df_display['预算销量']
        df_display[get_text('col_revenue_diff')] = df_display['预测收入'] - df_display['预算收入']
        df_display[get_text('col_gross_profit_diff')] = df_display['预测毛利'] - df_display['预算毛利']
        df_display[get_text('col_net_profit_diff')] = df_display['预测净利'] - df_display['预算净利']
        
        # 创建显示用的格式化副本
        df_formatted = df_display.copy()
        numeric_cols = ['预测销量', '预算销量', get_text('col_sales_diff'), 
                       '预测收入', '预算收入', get_text('col_revenue_diff'), 
                       '预测毛利', '预算毛利', get_text('col_gross_profit_diff'),
                       '预测净利', '预算净利', get_text('col_net_profit_diff')]
        
        for col in numeric_cols:
            if col in df_formatted.columns:
                if '销量' in col or 'Sales' in col:
                    df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
                else:
                    df_formatted[col] = df_formatted[col].apply(lambda x: f"{currency_symbol}{x:,.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(df_formatted, use_container_width=True, height=400)
        
        # 双格式导出功能
        if 'export' in st.session_state.get('permissions', []):
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df_display.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=get_text('btn_export_csv'),
                    data=csv_data,
                    file_name=f"Budget_Forecast_Comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="预算vs预测对比",
                        export_type="CSV", 
                        record_count=len(df_display)
                    )
                )
            
            with col2:
                # Excel导出
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_display.to_excel(writer, index=False, sheet_name='Comparison_Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label=get_text('btn_export_excel'),
                    data=excel_data,
                    file_name=f"Budget_Forecast_Comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="预算vs预测对比",
                        export_type="Excel", 
                        record_count=len(df_display)
                    )
                )
        
        # 可视化
        viz_tab1, viz_tab2, viz_tab3 = st.tabs([
            f"{get_text('tab_sales')}",
            f"{get_text('tab_revenue')} ({currency_symbol})",
            f"{get_text('tab_net_income')} ({currency_symbol})"
        ])
        
        with viz_tab1:
            if '预测销量' in df_display.columns and '预算销量' in df_display.columns:
                sales_data = df_display[['h_Time', 'Country', 'Model', '预测销量', '预算销量']].dropna()
                if not sales_data.empty:
                    sales_summary = sales_data.groupby('h_Time')[['预测销量', '预算销量']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name=get_text('legend_forecast'), x=sales_summary['h_Time'], y=sales_summary['预测销量']))
                    fig.add_trace(go.Bar(name=get_text('legend_budget'), x=sales_summary['h_Time'], y=sales_summary['预算销量']))
                    fig.update_layout(barmode='group', title=get_text('chart_sales_comparison'))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(get_text('msg_no_sales_data'))
        
        with viz_tab2:
            if '预测收入' in df_display.columns and '预算收入' in df_display.columns:
                revenue_data = df_display[['h_Time', 'Country', 'Model', '预测收入', '预算收入']].dropna()
                if not revenue_data.empty:
                    revenue_summary = revenue_data.groupby('h_Time')[['预测收入', '预算收入']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(name=get_text('legend_forecast'), x=revenue_summary['h_Time'], 
                                            y=revenue_summary['预测收入'], mode='lines+markers'))
                    fig.add_trace(go.Scatter(name=get_text('legend_budget'), x=revenue_summary['h_Time'], 
                                            y=revenue_summary['预算收入'], mode='lines+markers'))
                    fig.update_layout(
                        title=f"{get_text('chart_revenue_comparison')} ({currency_symbol})",
                        yaxis_title=f"{get_text('unit_revenue')} ({currency_symbol})"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(get_text('msg_no_revenue_data'))
        
        with viz_tab3:
            if '预测净利' in df_display.columns and '预算净利' in df_display.columns:
                profit_data = df_display[['h_Time', 'Country', 'Model', '预测净利', '预算净利']].dropna()
                if not profit_data.empty:
                    profit_summary = profit_data.groupby('h_Time')[['预测净利', '预算净利']].sum().reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(name=get_text('legend_forecast'), x=profit_summary['h_Time'], y=profit_summary['预测净利'], 
                                           mode='lines+markers', fill='tozeroy'))
                    fig.add_trace(go.Scatter(name=get_text('legend_budget'), x=profit_summary['h_Time'], y=profit_summary['预算净利'], 
                                           mode='lines+markers', fill='tozeroy'))
                    fig.update_layout(
                        title=f"{get_text('chart_profit_comparison')} ({currency_symbol})",
                        yaxis_title=f"{get_text('unit_profit')} ({currency_symbol})"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(get_text('msg_no_profit_data'))
    
    else:
        st.warning(get_text('msg_no_comparison_data'))

def show_time_breakdown_analysis(db):
    """新增：国家总数据按时间段拆分对比"""
    
    # ========== 筛选条件区域 ==========
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_periods = db.get_all_time_periods()
        if not time_periods:
            st.warning(get_text('msg_no_time_data'))
            return
        
        selected_times = st.multiselect(
            get_text('select_time_periods'),  # 需要添加到i18n.py
            options=time_periods,
            default=time_periods[:min(3, len(time_periods))]
        )
    
    with col2:
        default_idx = 0 if st.session_state.get('language') == 'zh' else 1
        currency_opt = st.selectbox(
            get_text('currency'),
            ["CNY", "USD"],
            index=default_idx,
            key="time_curr"
        )
    
    if not selected_times:
        st.info(get_text('msg_select_time_period'))  # 需要添加到i18n.py
        return
    
    # 记录查看日志
    filter_details = []
    if selected_times:
        filter_details.append(f"时间段: {', '.join(selected_times)}")
    filter_details.append(f"货币: {currency_opt}")
    
    log_view_action(
        db=db,
        page_name=get_text('nav_analysis'),
        analysis_type="时间段分解分析",
        filter_details="; ".join(filter_details)
    )
    
    # 获取各时间段的国家汇总数据
    all_data = []
    for time_period in selected_times:
        df_time = db.get_country_summary(time_period)
        if df_time is not None and not df_time.empty:
            df_time['Time Period'] = time_period
            all_data.append(df_time)
    
    if not all_data:
        st.warning(get_text('msg_no_data_for_time'))  # 需要添加到i18n.py
        return
    
    # 合并数据并应用货币转换
    df_combined = pd.concat(all_data, ignore_index=True)
    df_converted, currency_symbol = apply_currency_conversion(df_combined, db, currency_opt)
    
    # 显示数据统计信息 - 使用i18n
    st.info(get_text('msg_time_breakdown_stats').format(
        records=len(df_converted), 
        countries=df_converted['Country'].nunique()
    ))
    
    # 创建格式化显示副本
    df_display = df_converted[['Time Period', 'Country', '总销量', '总收入', '总毛利', '总净收入']].copy()
    df_formatted = df_display.copy()
    
    df_formatted['总销量'] = df_formatted['总销量'].apply(lambda x: f"{x:,.0f}")
    df_formatted['总收入'] = df_formatted['总收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
    df_formatted['总毛利'] = df_formatted['总毛利'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
    df_formatted['总净收入'] = df_formatted['总净收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
    
    st.dataframe(df_formatted, use_container_width=True, height=400)
    
    # 可视化对比
    viz_tab1, viz_tab2, viz_tab3 = st.tabs([
        get_text('tab_revenue_trends'),  # 需要添加到i18n.py
        get_text('tab_net_income_trends'),  # 需要添加到i18n.py
        get_text('tab_country_heatmap')  # 需要添加到i18n.py
    ])
    
    with viz_tab1:
        # 收入趋势对比
        fig = px.line(df_converted, x='Time Period', y='总收入', color='Country',
                     title=f"{get_text('chart_revenue_trends')} ({currency_symbol})",  # 需要添加到i18n.py
                     markers=True)
        fig.update_layout(
            yaxis_title=f"{get_text('unit_revenue')} ({currency_symbol})",
            xaxis_title=get_text('label_time_period')  # 需要添加到i18n.py
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_tab2:
        # 净收入趋势对比
        fig = px.bar(df_converted, x='Time Period', y='总净收入', color='Country',
                    title=f"{get_text('chart_net_income_by_time')} ({currency_symbol})",  # 需要添加到i18n.py
                    barmode='group')
        fig.update_layout(
            yaxis_title=f"{get_text('unit_profit')} ({currency_symbol})",
            xaxis_title=get_text('label_time_period')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_tab3:
        # 热力图：国家 x 时间段
        pivot_data = df_converted.pivot(index='Country', columns='Time Period', values='总收入')
        fig = px.imshow(pivot_data, 
                       labels=dict(x=get_text('label_time_period'), y=get_text('select_country'), 
                                 color=f"{get_text('unit_revenue')} ({currency_symbol})"),
                       title=f"{get_text('chart_revenue_heatmap')} ({currency_symbol})",  # 需要添加到i18n.py
                       aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    
    # 双格式导出功能
    if 'export' in st.session_state.get('permissions', []):
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = df_converted.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=get_text('btn_export_csv'),
                data=csv_data,
                file_name=f"Time_Breakdown_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                on_click=lambda: log_export_action(
                    db=db, 
                    page_name=get_text('nav_analysis'),
                    analysis_type="时间段分解分析",
                    export_type="CSV", 
                    record_count=len(df_converted)
                )
            )
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_converted.to_excel(writer, index=False, sheet_name='Time_Breakdown_Data')
            excel_data = output.getvalue()
            
            st.download_button(
                label=get_text('btn_export_excel'),
                data=excel_data,
                file_name=f"Time_Breakdown_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                on_click=lambda: log_export_action(
                    db=db, 
                    page_name=get_text('nav_analysis'),
                    analysis_type="时间段分解分析",
                    export_type="Excel", 
                    record_count=len(df_converted)
                )
            )

def show_country_summary(db):
    """按国家汇总分析（使用预测数据Display）"""
    
    # 获取用户信息
    u = st.session_state.get('user_info', {})
    country_filter = u.get('country')
    
    # ========== 筛选条件区域 ==========
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_periods = db.get_all_time_periods()
        if not time_periods:
            st.warning(get_text('msg_no_time_data'))  # 修改：硬编码中文 → get_text
            return
            
        selected_time = st.selectbox(
            get_text('select_time'),
            options=[get_text('view_all_option')] + time_periods,
            index=0,
            key="country_time"
        )
    
    with col2:
        default_idx = 0 if st.session_state.get('language') == 'zh' else 1
        currency_opt = st.selectbox(
            get_text('currency'),
            ["CNY", "USD"],
            index=default_idx,
            key="ctry_curr"
        )
    
    # 记录查看日志
    filter_details = []
    if selected_time != get_text('view_all_option'):
        filter_details.append(f"时间: {selected_time}")
    if country_filter:
        filter_details.append(f"国家: {country_filter}")
    filter_details.append(f"货币: {currency_opt}")
    
    log_view_action(
        db=db,
        page_name=get_text('nav_analysis'),
        analysis_type="国家汇总分析",
        filter_details="; ".join(filter_details)
    )
    
    # 获取数据
    time_param = selected_time if selected_time != get_text('view_all_option') else None
    df = db.get_country_summary(time_param)
    
    # 如果是业务员，筛选本国数据
    if country_filter and df is not None and not df.empty:
        df = df[df['Country'] == country_filter]
    
    if df is not None and not df.empty:
        # 应用货币转换
        df_converted, currency_symbol = apply_currency_conversion(df, db, currency_opt)
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            country_count = len(df_converted)
            st.metric(get_text('metric_country'), country_count)  # 修改：metric_countries → metric_country
        
        with col2:
            if '总收入' in df_converted.columns:
                total_revenue = df_converted['总收入'].sum()
                st.metric(get_text('metric_total_revenue'), f"{currency_symbol}{total_revenue:,.2f}")
        
        with col3:
            if '总净收入' in df_converted.columns:
                total_net_income = df_converted['总净收入'].sum()
                st.metric(get_text('metric_total_profit'), f"{currency_symbol}{total_net_income:,.2f}")  # 修改：metric_total_net_income → metric_total_profit
        
        # 显示数据统计信息 - 使用i18n
        if country_filter:
            st.info(get_text('msg_current_region').format(region=country_filter))
        else:
            st.info(get_text('msg_found_records').format(count=country_count))
        
        # 数据表格
        df_display = df_converted.copy()
        df_formatted = df_display.copy()
        
        df_formatted['总销量'] = df_formatted['总销量'].apply(lambda x: f"{x:,.0f}")
        df_formatted['总收入'] = df_formatted['总收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        df_formatted['总毛利'] = df_formatted['总毛利'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        df_formatted['总净收入'] = df_formatted['总净收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        
        st.dataframe(df_formatted, use_container_width=True)
        
        # 可视化
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"##### {get_text('chart_revenue_by_country')} ({currency_symbol})")
            fig = px.bar(df_converted, x='Country', y='总收入', 
                        title=f"{get_text('chart_revenue_by_country')} ({currency_symbol})")
            fig.update_layout(yaxis_title=f"{get_text('unit_revenue')} ({currency_symbol})")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"##### {get_text('chart_net_income_by_country')} ({currency_symbol})")
            fig = px.bar(df_converted, x='Country', y='总净收入', 
                        title=f"{get_text('chart_net_income_by_country')} ({currency_symbol})", 
                        color='总净收入')
            fig.update_layout(yaxis_title=f"{get_text('unit_profit')} ({currency_symbol})")
            st.plotly_chart(fig, use_container_width=True)
        
        # 双格式导出功能
        if 'export' in st.session_state.get('permissions', []):
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df_converted.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=get_text('btn_export_csv'),
                    data=csv_data,
                    file_name=f"Country_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="国家汇总分析",
                        export_type="CSV", 
                        record_count=len(df_converted)
                    )
                )
            
            with col2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_converted.to_excel(writer, index=False, sheet_name='Country_Summary_Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label=get_text('btn_export_excel'),
                    data=excel_data,
                    file_name=f"Country_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="国家汇总分析",
                        export_type="Excel", 
                        record_count=len(df_converted)
                    )
                )
    
    else:
        st.warning(get_text('msg_no_data'))

def show_product_summary(db):
    """按产品汇总分析（使用预测数据Display）"""
    
    # 获取用户信息
    u = st.session_state.get('user_info', {})
    country_filter = u.get('country')
    
    # ========== 筛选条件区域 ==========
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_periods = db.get_all_time_periods()
        if not time_periods:
            st.warning(get_text('msg_no_time_data'))  # 修改：硬编码中文 → get_text
            return
            
        selected_time = st.selectbox(
            get_text('select_time'),
            options=[get_text('view_all_option')] + time_periods,
            index=0,
            key="model_time"
        )
    
    with col2:
        default_idx = 0 if st.session_state.get('language') == 'zh' else 1
        currency_opt = st.selectbox(
            get_text('currency'),
            ["CNY", "USD"],
            index=default_idx,
            key="prod_curr"
        )
    
    # 记录查看日志
    filter_details = []
    if selected_time != get_text('view_all_option'):
        filter_details.append(f"时间: {selected_time}")
    if country_filter:
        filter_details.append(f"国家: {country_filter}")
    filter_details.append(f"货币: {currency_opt}")
    
    log_view_action(
        db=db,
        page_name=get_text('nav_analysis'),
        analysis_type="产品汇总分析",
        filter_details="; ".join(filter_details)
    )
    
    # 获取数据
    time_param = selected_time if selected_time != get_text('view_all_option') else None
    df = db.get_model_summary(time_param)
    
    # 如果是业务员，需要从Display表筛选本国产品数据
    if country_filter and df is not None and not df.empty:
        if selected_time != get_text('view_all_option'):
            query = """
                SELECT Model, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                WHERE h_Time = %s AND Country = %s
                GROUP BY Model
                ORDER BY 总收入 DESC
            """
            params = (selected_time, country_filter)
        else:
            query = """
                SELECT Model, 
                       SUM(Sales) as 总销量,
                       SUM(Revenues) as 总收入,
                       SUM(Gross_profits) as 总毛利,
                       SUM(Net_income) as 总净收入
                FROM Display
                WHERE Country = %s
                GROUP BY Model
                ORDER BY 总收入 DESC
            """
            params = (country_filter,)
        
        df = db.execute_query(query, params)
    
    if df is not None and not df.empty:
        # 应用货币转换
        df_converted, currency_symbol = apply_currency_conversion(df, db, currency_opt)
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product_count = len(df_converted)
            st.metric(get_text('metric_model'), product_count)  # 修改：metric_product_models → metric_model
        
        with col2:
            if '总销量' in df_converted.columns:
                total_sales = df_converted['总销量'].sum()
                st.metric(get_text('metric_total_sales'), f"{total_sales:,.0f}")
        
        with col3:
            if '总收入' in df_converted.columns:
                total_revenue = df_converted['总收入'].sum()
                st.metric(get_text('metric_total_revenue'), f"{currency_symbol}{total_revenue:,.2f}")
        
        # 显示数据统计信息 - 使用i18n
        if country_filter:
            st.info(get_text('msg_current_region').format(region=country_filter))
        else:
            st.info(get_text('msg_found_records').format(count=product_count))
        
        # 数据表格
        df_display = df_converted.copy()
        df_formatted = df_display.copy()
        
        df_formatted['总销量'] = df_formatted['总销量'].apply(lambda x: f"{x:,.0f}")
        df_formatted['总收入'] = df_formatted['总收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        df_formatted['总毛利'] = df_formatted['总毛利'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        df_formatted['总净收入'] = df_formatted['总净收入'].apply(lambda x: f"{currency_symbol}{x:,.2f}")
        
        st.dataframe(df_formatted, use_container_width=True)
        
        # 可视化
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"##### {get_text('chart_sales_by_product')}")
            fig = px.bar(df_converted, x='Model', y='总销量', 
                        title=get_text('chart_sales_by_product'))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"##### {get_text('chart_revenue_distribution')} ({currency_symbol})")
            fig = px.pie(df_converted, values='总收入', names='Model', 
                        title=f"{get_text('chart_revenue_distribution')} ({currency_symbol})")
            st.plotly_chart(fig, use_container_width=True)
        
        # 双格式导出功能
        if 'export' in st.session_state.get('permissions', []):
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df_converted.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=get_text('btn_export_csv'),
                    data=csv_data,
                    file_name=f"Product_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="产品汇总分析",
                        export_type="CSV", 
                        record_count=len(df_converted)
                    )
                )
            
            with col2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_converted.to_excel(writer, index=False, sheet_name='Product_Summary_Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label=get_text('btn_export_excel'),
                    data=excel_data,
                    file_name=f"Product_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    on_click=lambda: log_export_action(
                        db=db, 
                        page_name=get_text('nav_analysis'),
                        analysis_type="产品汇总分析",
                        export_type="Excel", 
                        record_count=len(df_converted)
                    )
                )
    
    else:
        st.warning(get_text('msg_no_data'))

if __name__ == "__main__":
    main()