"""
报表生成页面
Report Generation Page
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from utils.database import get_db_manager


def show():
    """显示报表生成页面"""
    st.markdown('<div class="main-header">📑 报表生成</div>', unsafe_allow_html=True)
    
    if 'export' not in st.session_state.permissions:
        st.warning("⚠️ 您没有导出报表权限。")
        return
    
    # 获取数据库管理器
    db = get_db_manager()
    
    st.markdown("### 📊 选择报表类型")
    
    report_type = st.selectbox(
        "报表类型",
        options=[
            "综合报表",
            "历史数据报表",
            "预算数据报表",
            "预算实际对比报表",
            "国家汇总报表",
            "产品汇总报表"
        ]
    )
    
    st.markdown("---")
    
    # 筛选条件
    st.markdown("### 🔍 筛选条件")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_periods = db.get_all_time_periods()
        selected_time = st.selectbox(
            "选择时间",
            options=["全部"] + time_periods,
            index=0
        )
    
    with col2:
        countries = db.get_all_countries()
        selected_country = st.selectbox(
            "选择国家",
            options=["全部"] + countries,
            index=0
        )
    
    with col3:
        models = db.get_all_models()
        selected_model = st.selectbox(
            "选择产品",
            options=["全部"] + models,
            index=0
        )
    
    st.markdown("---")
    
    # 生成报表按钮
    if st.button("📊 生成报表", type="primary", use_container_width=True):
        generate_report(db, report_type, selected_time, selected_country, selected_model)


def generate_report(db, report_type, time_period, country, model):
    """生成报表"""
    try:
        # 构建筛选条件
        filters = {}
        if time_period != "全部":
            filters['time'] = time_period
        if country != "全部":
            filters['country'] = country
        if model != "全部":
            filters['model'] = model
        
        # 根据报表类型获取数据
        if report_type == "综合报表":
            df = generate_comprehensive_report(db, filters)
        elif report_type == "历史数据报表":
            df = db.get_history_data(filters if filters else None)
        elif report_type == "预算数据报表":
            df = db.get_budget_data(filters if filters else None)
        elif report_type == "预算实际对比报表":
            df = db.get_comparison_data(time_period if time_period != "全部" else None)
        elif report_type == "国家汇总报表":
            df = db.get_country_summary(time_period if time_period != "全部" else None)
        elif report_type == "产品汇总报表":
            df = db.get_model_summary(time_period if time_period != "全部" else None)
        else:
            df = None
        
        if df is not None and not df.empty:
            st.success(f"✅ 报表生成成功！共 {len(df)} 条记录")
            
            # 显示报表预览
            st.markdown("---")
            st.markdown("### 📋 报表预览")
            st.dataframe(df, use_container_width=True, height=400)
            
            # 显示统计信息
            st.markdown("---")
            st.markdown("### 📊 统计摘要")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📝 记录数", f"{len(df):,}")
            
            with col2:
                if '销量' in df.columns:
                    st.metric("📦 总销量", f"{df['销量'].sum():,}")
                elif '总销量' in df.columns:
                    st.metric("📦 总销量", f"{df['总销量'].sum():,}")
            
            with col3:
                if '收入' in df.columns:
                    st.metric("💰 总收入", f"¥{df['收入'].sum():,.2f}")
                elif '总收入' in df.columns:
                    st.metric("💰 总收入", f"¥{df['总收入'].sum():,.2f}")
            
            # 导出选项
            st.markdown("---")
            st.markdown("### 📥 导出报表")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV导出
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📄 导出为 CSV",
                    data=csv,
                    file_name=f"{report_type}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Excel导出
                excel_data = to_excel(df)
                st.download_button(
                    label="📊 导出为 Excel",
                    data=excel_data,
                    file_name=f"{report_type}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        else:
            st.warning("⚠️ 没有找到符合条件的数据。")
    
    except Exception as e:
        st.error(f"❌ 报表生成失败: {str(e)}")


def generate_comprehensive_report(db, filters):
    """生成综合报表"""
    # 获取历史数据和预算数据
    history_df = db.get_history_data(filters if filters else None)
    budget_df = db.get_budget_data(filters if filters else None)
    
    if history_df is not None and budget_df is not None:
        # 添加数据来源标识
        history_df['数据来源'] = '实际'
        budget_df['数据来源'] = '预算'
        
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
        df.to_excel(writer, index=False, sheet_name='报表数据')
    output.seek(0)
    return output.getvalue()
