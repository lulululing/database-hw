import streamlit as st
import pandas as pd
import io
from utils.database import get_db_manager
from datetime import datetime

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 检查权限 - 有导出权限的都能生成报表
if 'export' not in st.session_state.get('permissions', []):
    st.error("您没有权限访问此页面")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="报表生成",
    layout="wide"
)

def main():
    st.title("报表生成与导出")
    
    # 获取用户信息
    u = st.session_state.user_info
    role = st.session_state.role
    db = get_db_manager()
    
    # 根据角色显示提示
    country_filter = u.get('country')
    if country_filter:
        st.info(f"当前区域: **{country_filter}** (报表将只包含您所在国家的数据)")
    else:
        st.info("您可以生成所有国家的报表")
    
    # 选择报表类型
    st.markdown("### 选择报表类型")
    
    report_type = st.selectbox(
        "报表类型",
        [
            "综合数据报表 (Display)",
            "历史数据报表 (History)",
            "预算数据报表 (Budget)",
            "成本数据报表 (Costs)",
            "销售价格报表 (Sales Price)",
            "预算预测对比报表 (Budget vs Forecast)",
            "国家汇总报表 (Country Summary)",
            "产品汇总报表 (Product Summary)"
        ]
    )
    
    # 筛选条件
    st.markdown("### 筛选条件")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox("时间周期", ["全部"] + time_periods)
    
    with col2:
        if country_filter:
            selected_country = st.text_input("国家", country_filter, disabled=True)
        else:
            countries = ["全部"] + db.get_all_countries()
            selected_country = st.selectbox("国家", countries)
    
    with col3:
        models = ["全部"] + db.get_all_models()
        selected_model = st.selectbox("产品型号", models)
    
    # 生成报表按钮
    if st.button("生成报表", type="primary", use_container_width=True):
        with st.spinner("正在生成报表..."):
            try:
                df = None
                report_name = ""
                
                # 根据报表类型获取数据
                if "综合数据报表" in report_type:
                    query = "SELECT * FROM Display WHERE 1=1"
                    params = []
                    
                    if country_filter:
                        query += " AND Country = %s"
                        params.append(country_filter)
                    elif selected_country != "全部":
                        query += " AND Country = %s"
                        params.append(selected_country)
                    
                    if selected_time != "全部":
                        query += " AND h_Time = %s"
                        params.append(selected_time)
                    
                    if selected_model != "全部":
                        query += " AND Model = %s"
                        params.append(selected_model)
                    
                    df = db.execute_query(query, tuple(params) if params else None)
                    report_name = "Display_Report"
                
                elif "历史数据报表" in report_type:
                    filters = {}
                    if country_filter:
                        filters['country'] = country_filter
                    elif selected_country != "全部":
                        filters['country'] = selected_country
                    
                    if selected_time != "全部":
                        filters['time'] = selected_time
                    
                    if selected_model != "全部":
                        filters['model'] = selected_model
                    
                    df = db.get_history_data(filters)
                    report_name = "History_Report"
                
                elif "预算数据报表" in report_type:
                    filters = {}
                    if country_filter:
                        filters['country'] = country_filter
                    elif selected_country != "全部":
                        filters['country'] = selected_country
                    
                    if selected_time != "全部":
                        filters['time'] = selected_time
                    
                    if selected_model != "全部":
                        filters['model'] = selected_model
                    
                    df = db.get_budget_data(filters)
                    report_name = "Budget_Report"
                
                elif "成本数据报表" in report_type:
                    if country_filter:
                        df = db.get_costs_data(country=country_filter)
                    elif selected_country != "全部":
                        df = db.get_costs_data(country=selected_country)
                    else:
                        df = db.get_costs_data()
                    report_name = "Costs_Report"
                
                elif "销售价格报表" in report_type:
                    if country_filter:
                        df = db.get_sales_price_data(country=country_filter)
                    elif selected_country != "全部":
                        df = db.get_sales_price_data(country=selected_country)
                    else:
                        df = db.get_sales_price_data()
                    report_name = "Sales_Price_Report"
                
                elif "预算预测对比报表" in report_type:
                    df = db.get_comparison_data(selected_time if selected_time != "全部" else None)
                    
                    if country_filter and not df.empty:
                        df = df[df['Country'] == country_filter]
                    elif selected_country != "全部" and not df.empty:
                        df = df[df['Country'] == selected_country]
                    
                    report_name = "Budget_Forecast_Comparison"
                
                elif "国家汇总报表" in report_type:
                    df = db.get_country_summary(selected_time if selected_time != "全部" else None)
                    
                    if country_filter and not df.empty:
                        df = df[df['Country'] == country_filter]
                    elif selected_country != "全部" and not df.empty:
                        df = df[df['Country'] == selected_country]
                    
                    report_name = "Country_Summary_Report"
                
                elif "产品汇总报表" in report_type:
                    if country_filter:
                        # 业务员只看本国产品
                        if selected_time != "全部":
                            df = db.execute_query("""
                                SELECT Model, SUM(Sales) as 总销量, SUM(Revenues) as 总收入,
                                       SUM(Gross_profits) as 总毛利, SUM(Net_income) as 总净收入
                                FROM Display WHERE Country = %s AND h_Time = %s
                                GROUP BY Model ORDER BY 总收入 DESC
                            """, (country_filter, selected_time))
                        else:
                            df = db.execute_query("""
                                SELECT Model, SUM(Sales) as 总销量, SUM(Revenues) as 总收入,
                                       SUM(Gross_profits) as 总毛利, SUM(Net_income) as 总净收入
                                FROM Display WHERE Country = %s
                                GROUP BY Model ORDER BY 总收入 DESC
                            """, (country_filter,))
                    else:
                        df = db.get_model_summary(selected_time if selected_time != "全部" else None)
                    
                    report_name = "Product_Summary_Report"
                
                # 显示报表
                if df is not None and not df.empty:
                    st.success(f"报表生成成功！共 {len(df)} 条记录")
                    
                    # 显示数据预览
                    st.markdown("### 报表预览")
                    st.dataframe(df, use_container_width=True, height=400)
                    
                    # 统计信息
                    st.markdown("### 报表统计")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("总记录数", len(df))
                    
                    with col2:
                        if 'Sales' in df.columns or '总销量' in df.columns:
                            sales_col = 'Sales' if 'Sales' in df.columns else '总销量'
                            st.metric("总销量", f"{df[sales_col].sum():,}")
                    
                    with col3:
                        revenue_cols = ['Revenues', '总收入', 'Revenue']
                        revenue_col = next((col for col in revenue_cols if col in df.columns), None)
                        if revenue_col:
                            st.metric("总收入", f"¥{df[revenue_col].sum():,.2f}")
                    
                    # 导出选项
                    st.markdown("---")
                    st.markdown("### 导出报表")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    # 生成文件名
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename_base = f"{report_name}_{timestamp}"
                    
                    with col1:
                        # CSV导出
                        csv = df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="导出为 CSV",
                            data=csv,
                            file_name=f"{filename_base}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Excel导出
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False, sheet_name='Report')
                        
                        excel_data = output.getvalue()
                        
                        st.download_button(
                            label="导出为 Excel",
                            data=excel_data,
                            file_name=f"{filename_base}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    with col3:
                        # HTML导出
                        html = df.to_html(index=False)
                        st.download_button(
                            label="导出为 HTML",
                            data=html,
                            file_name=f"{filename_base}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    
                    # 记录日志
                    db.log_event(u['id'], "EXPORT", f"Generated {report_name} with {len(df)} records")
                
                else:
                    st.warning("未找到符合条件的数据")
                    
            except Exception as e:
                st.error(f"生成报表失败: {str(e)}")
                with st.expander("查看错误详情"):
                    st.code(str(e))

if __name__ == "__main__":
    main()