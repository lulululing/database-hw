
import streamlit as st
import pandas as pd
from io import BytesIO
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("Please login first")
    st.switch_page("app.py")

# 检查权限
if 'export' not in st.session_state.get('permissions', []):
    st.error("You don't have permission to access this page")
    st.stop()

# 设置页面
st.set_page_config(
    page_title="报表生成",
    layout="wide"
)
st.title("报表生成")
def main():
    """报表生成页面"""
    st.markdown('<div class="main-header">Report Generation</div>', unsafe_allow_html=True)
    
    # 获取数据库管理器
    db = get_db_manager()
    
    st.markdown("### Select Report Type")
    
    report_type = st.selectbox(
        "Report Type",
        options=[
            "Comprehensive Report",
            "Historical Data Report",
            "Budget Data Report",
            "Budget vs Actual Comparison Report",
            "Country Summary Report",
            "Product Summary Report"
        ]
    )
    
    st.markdown("---")
    
    # 筛选条件
    st.markdown("### Filter Conditions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox(
            "Select Time Period",
            options=["All"] + time_periods,
            index=0
        )
    
    with col2:
        countries = db.get_all_countries()
        selected_country = st.selectbox(
            "Select Country",
            options=["All"] + countries,
            index=0
        )
    
    with col3:
        models = db.get_all_models()
        selected_model = st.selectbox(
            "Select Product",
            options=["All"] + models,
            index=0
        )
    
    st.markdown("---")
    
    # 生成报表按钮
    if st.button("Generate Report", type="primary", use_container_width=True):
        generate_report(db, report_type, selected_time, selected_country, selected_model)

def generate_report(db, report_type, time_period, country, model):
    """生成报表"""
    try:
        # 构建筛选条件
        filters = {}
        if time_period != "All":
            filters['time'] = time_period
        if country != "All":
            filters['country'] = country
        if model != "All":
            filters['model'] = model
        
        # 根据报表类型获取数据
        if report_type == "Comprehensive Report":
            df = generate_comprehensive_report(db, filters)
        elif report_type == "Historical Data Report":
            df = db.get_history_data(filters if filters else None)
        elif report_type == "Budget Data Report":
            df = db.get_budget_data(filters if filters else None)
        elif report_type == "Budget vs Actual Comparison Report":
            df = db.get_comparison_data(time_period if time_period != "All" else None)
        elif report_type == "Country Summary Report":
            df = db.get_country_summary(time_period if time_period != "All" else None)
        elif report_type == "Product Summary Report":
            df = db.get_model_summary(time_period if time_period != "All" else None)
        else:
            df = None
        
        if df is not None and not df.empty:
            st.success(f"Report generated successfully! Total {len(df)} records")
            
            # 显示报表预览
            st.markdown("---")
            st.markdown("### Report Preview")
            st.dataframe(df, use_container_width=True, height=400)
            
            # 显示统计信息
            st.markdown("---")
            st.markdown("### Report Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Records", f"{len(df):,}")
            
            with col2:
                if 'Sales' in df.columns:
                    st.metric("Total Sales", f"{df['Sales'].sum():,}")
                elif '总销量' in df.columns:
                    st.metric("Total Sales", f"{df['总销量'].sum():,}")
            
            with col3:
                if 'Revenues' in df.columns:
                    st.metric("Total Revenue", f"¥{df['Revenues'].sum():,.2f}")
                elif '总收入' in df.columns:
                    st.metric("Total Revenue", f"¥{df['总收入'].sum():,.2f}")
            
            # 导出选项
            st.markdown("---")
            st.markdown("### Export Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV导出
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Export as CSV",
                    data=csv,
                    file_name=f"{report_type.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Excel导出
                excel_data = to_excel(df)
                st.download_button(
                    label="Export as Excel",
                    data=excel_data,
                    file_name=f"{report_type.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        else:
            st.warning("No data found matching the criteria.")
    
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")

def generate_comprehensive_report(db, filters):
    """生成综合报表"""
    # 获取历史数据和预算数据
    history_df = db.get_history_data(filters if filters else None)
    budget_df = db.get_budget_data(filters if filters else None)
    
    if history_df is not None and budget_df is not None:
        # 添加数据来源标识
        history_df['Data_Source'] = 'Actual'
        budget_df['Data_Source'] = 'Budget'
        
        # 合并数据
        df = pd.concat([history_df, budget_df], ignore_index=True)
        return df
    elif history_df is not None:
        return history_df
    elif budget_df is not None:
        return budget_df
    else:
        return None

def to_excel(df):
    """将DataFrame转换为Excel文件"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report_Data')
    output.seek(0)
    return output.getvalue()

if __name__ == "__main__":
    main()