# app/pages/1_Dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
from utils.helper import apply_currency_conversion
from utils.database import get_db_manager
from utils.i18n import get_text, show_sidebar_with_nav

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_warning'))
    st.switch_page("app.py")

show_sidebar_with_nav()

# 设置页面标题
st.set_page_config(
    page_title=get_text('dashboard_header'),
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
/* 全局卡片样式 */
.main-header {
    font-size: 1.8rem;
    font-weight: bold;
    color: #1f77b4;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #eee;
}

/* 强制修改 Primary 按钮为蓝色 (用于批量导出和退出) */
div.stButton > button[kind="primary"] {
    background-color: #1f77b4 !important;
    border-color: #1f77b4 !important;
    color: white !important;
    font-weight: bold !important;
    transition: all 0.3s;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #155a8a !important;
    border-color: #155a8a !important;
}

/* 快速访问卡片样式 */
.metric-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #eee;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
    cursor: pointer;
    margin-bottom: 1rem;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.metric-card h3 {
    color: #1f77b4;
    margin-top: 0 !important;
    margin-bottom: 10px !important;
    font-size: 1.3rem !important;
}

.metric-card p {
    color: #666;
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 0 !important;
}

/* 系统状态卡片 */
.status-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #eee;
}

/* 标题样式微调 */
h2 {
    font-size: 1.5rem !important;
    color: #333;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}
h3 {
    font-size: 1.2rem !important;
    color: #555;
    margin-top: 1rem !important;
}
.avatar-container {
    display: flex; 
    justify-content: center; 
    align-items: center; 
    width: 100%; 
    height: 120px; 
    background-color: white;          /* 白色背景 */
    border: 3px solid black;          /* 黑色边框 */
    border-radius: 10px;              /* 圆角 */
    font-size: 50px;
}
/* 批量导出按钮 - 蓝色 */
div.stButton > button[kind="primary"][key="generate_batch_main"],
button[kind="primary"][data-testid="baseButton-secondary"]:has-text("生成批量导出文件"),
button[kind="primary"]:has-text("Generate Batch Export") {
    background-color: #1f77b4 !important;
    border-color: #1f77b4 !important;
    color: white !important;
}

/* 快速导出按钮保持原有样式 */
div.stButton > button:not([kind="primary"]) {
    /* 快速导出按钮的样式 */
}

/* 退出按钮 - 红色 */
div.stButton > button[kind="primary"]:contains("退出"),
div.stButton > button[kind="primary"]:contains("Logout") {
    background-color: #FF4B4B !important;
    border-color: #FF4B4B !important;
}

.logout-btn-primary:hover {
    background-color: #FF3333 !important;
}
</style>
""", unsafe_allow_html=True)

def show_user_profile_section():
    """用户中心部分"""
    st.markdown(f"## {get_text('dashboard_tab_profile')}")
    user_perms = st.session_state.get('permissions', []) 
    # 用户信息卡片
    with st.container():
        col_u1, col_u2 = st.columns([1, 5])
        
        with col_u1:
            # 头像区域
            st.markdown(
                """
                <div style="
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    width: 100px; 
                    height: 150px; 
                    background-color: white; 
                    border: 1px solid black; 
                    border-radius: 2px; 
                    font-size: 50px;
                    margin: 0 auto;">
                </div>
                """, 
                unsafe_allow_html=True
            )
    
        with col_u2:
            user_name = st.session_state.get('name', get_text('unknown_user'))
            user_role = st.session_state.get('role', get_text('unknown_role'))
            username = st.session_state.get('username', 'N/A')
            
            # --- 修改开始：使用HTML精确控制排版 ---
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; height: 150px; justify-content: flex-start; padding-top: 0;">
                <h2 style="margin: 0; padding: 0; line-height: 1.2; font-size: 1.8rem; border: none;">{user_name}</h2>
                <div style="font-weight: bold; color: #555; margin-top: 5px;">{user_role}</div>
                <div style="color: #888; font-size: 0.9rem;">{get_text('user_id')}: {username}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 权限明细 (网格布局)
    st.markdown(f"### {get_text('permissions')}")

    # 使用简单的列布局
    cols = st.columns(4)  # 或改成3就是3x3
    for idx, perm in enumerate(user_perms):
        with cols[idx % 4]:
            readable_perm = get_text(f"perm_{perm}")
            # 如果找不到，尝试去掉下划线后的字母
            if readable_perm.startswith("perm_"):
                # 简单转换
                readable_perm = perm.replace('_', ' ').title()
            st.write(f"{readable_perm}")
    
    st.markdown("---")

def show_system_status_section():
    """系统状态监控部分"""
    st.markdown(f"## {get_text('system_status')}")
    
    try:
        db = get_db_manager()
        
        # 尝试连接数据库
        if db.connect():
            st.success(get_text('db_connected'))
            
            # 综合数据统计
            st.markdown(f"### {get_text('comprehensive_data')}")
            try:
                time_periods = db.get_all_time_periods()
                countries = db.get_all_countries()
                models = db.get_all_models()
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric(get_text('metric_time'), len(time_periods))
                with col_stat2:
                    st.metric(get_text('metric_country'), len(countries))
                with col_stat3:
                    st.metric(get_text('metric_model'), len(models))
            except Exception as e:
                st.warning(f"{get_text('stat_failed')}: {str(e)}")
        else:
            st.error(get_text('db_failed'))
            
    except Exception as e:
        st.warning(f"{get_text('db_check_failed')}: {str(e)}")
        st.info(get_text('db_check_suggestion'))
    
    # 系统信息
    with st.expander(get_text('system_info'), expanded=False):
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            # 登录时间
            login_time = st.session_state.get('login_time', datetime.now())
            if isinstance(login_time, str):
                try:
                    login_time = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
                except:
                    login_time = datetime.now()
            
            st.write(f"**{get_text('login_time')}:**")
            st.write(login_time.strftime('%Y-%m-%d %H:%M:%S'))
            user_perms = st.session_state.get('permissions', []) 
            # 权限数量
            st.write(f"**{get_text('permission_count')}:**")
            st.write(f"{len(user_perms)}")
        
        with col_info2:
            # 数据库角色
            db_role = st.session_state.get('user_info', {}).get('db_role', 'Default')
            st.write(f"**{get_text('database_role')}:**")
            st.write(db_role)
            
            # 当前语言
            current_lang = st.session_state.get('language', 'zh')
            lang_display = "中文" if current_lang == 'zh' else "English"
            st.write(f"**{get_text('current_language')}:**")
            st.write(lang_display)

    st.markdown("---")

def show_batch_export_section():
    """批量导出功能 - 完整实现"""
    st.markdown(f"## {get_text('batch_export_title')}")
    st.markdown(f"<p style='color: #666;'>{get_text('batch_export_desc')}</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 选择数据表
            table_options = [
                get_text('source_display'),
                get_text('source_history'),
                get_text('source_budget'),
                get_text('source_costs'),
                get_text('source_price'),
                get_text('source_exchange'),
                get_text('source_expenses')
            ]
            
            table_mapping = {
                get_text('source_display'): 'Display',
                get_text('source_history'): 'History',
                get_text('source_budget'): 'Budget',
                get_text('source_costs'): 'Costs',
                get_text('source_price'): 'Sales_Price',
                get_text('source_exchange'): 'Exchange',
                get_text('source_expenses'): 'Regional_Expenses'
            }
            
            selected_tables = st.multiselect(
                get_text('batch_select_tables'),
                options=table_options,
                default=[get_text('source_display'), get_text('source_history')],
                help=get_text('batch_select_hint')
            )
        
        with col2:
            # 导出格式选择
            export_format = st.radio(
                get_text('export_format'),
                options=["Excel", "CSV"],
                horizontal=True,
                index=0
            )
        
        # 时间范围筛选
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            use_date_filter = st.checkbox(get_text('enable_date_filter'), value=False)
        
        with col_date2:
            if use_date_filter:
                date_col1, date_col2 = st.columns(2)
                with date_col1:
                    start_date = st.date_input(
                        get_text('start_date'),
                        value=datetime.now() - timedelta(days=30),
                        key="batch_start_date"
                    )
                with date_col2:
                    end_date = st.date_input(
                        get_text('end_date'),
                        value=datetime.now(),
                        key="batch_end_date"
                    )
            else:
                start_date = None
                end_date = None
        
        # 货币选择
        col_curr1, col_curr2 = st.columns(2)
        with col_curr1:
            convert_currency = st.checkbox(get_text('convert_currency'), value=True)
        with col_curr2:
            if convert_currency:
                target_currency = st.selectbox(get_text('target_currency'), ["CNY", "USD"])
            else:
                target_currency = None
        
        generate_btn = st.button(
            get_text('generate_batch_export'), 
            type="secondary",  # 改为secondary类型，这样不会默认红色
            key="generate_batch_main",
            use_container_width=True
        )

        # 然后通过CSS将secondary按钮也设为蓝色
        st.markdown("""
        <style>
        /* 将secondary类型的批量导出按钮设为蓝色 */
        div.stButton > button[kind="secondary"][key="generate_batch_main"] {
            background-color: #1f77b4 !important;
            border-color: #1f77b4 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if generate_btn:
            if not selected_tables:
                st.warning(get_text('batch_select_hint'))
                return
            
            with st.spinner(get_text('batch_processing')):
                try:
                    db = get_db_manager()
                    
                    # === 新增：获取当前用户的国家限制 ===
                    user_country = st.session_state.user_info.get('country')
                    # =================================
                    
                    # 收集所有数据
                    data_dict = {}
                    export_stats = {}
                    
                    for table_display in selected_tables:
                        table_name = table_mapping.get(table_display, table_display)
                        
                        # === 修改：构建带安全检查的 SQL 查询 ===
                        query = f"SELECT * FROM {table_name}"
                        params = []
                        conditions = [] # 用来存放 WHERE 条件
                        
                        # 1. 安全过滤：如果是业务员，强制加上国家筛选
                        # (注意：Exchange汇率表没有Country字段，所以排除掉)
                        if user_country and table_name != 'Exchange':
                            conditions.append("Country = %s")
                            params.append(user_country)
                        
                        # 2. 时间过滤 (原有的逻辑)
                        if use_date_filter and start_date and end_date:
                            # 根据表名确定时间列
                            time_col = 'h_Time' # 默认
                            if table_name == 'Costs': time_col = 'Costs_time'
                            elif table_name == 'Exchange': time_col = 'Exchange_time'
                            elif table_name == 'Regional_Expenses': time_col = 'Expenses_time'
                            
                            conditions.append(f"{time_col} >= %s AND {time_col} <= %s")
                            params.extend([start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')])
                        
                        # 3. 组装最终 SQL
                        if conditions:
                            query += " WHERE " + " AND ".join(conditions)
                        df = pd.read_sql_query(query, db.conn, params=params if params else None)
                        
                        if not df.empty:
                            # 应用货币转换
                            if convert_currency and target_currency and table_name not in ['Exchange']:
                                # 确定时间列
                                time_col = None
                                if 'h_Time' in df.columns:
                                    time_col = 'h_Time'
                                elif 'Costs_time' in df.columns:
                                    time_col = 'Costs_time'
                                elif 'Exchange_time' in df.columns:
                                    time_col = 'Exchange_time'
                                elif 'Expenses_time' in df.columns:
                                    time_col = 'Expenses_time'
                                
                                df_converted, currency_symbol = apply_currency_conversion(
                                    df, db, target_currency, time_col
                                )
                                data_dict[table_display] = df_converted
                            else:
                                data_dict[table_display] = df
                            
                            export_stats[table_display] = len(df)
                    
                    if not data_dict:
                        st.warning(get_text('no_data_found'))
                        return
                    
                    # 创建导出文件
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if export_format == "Excel":
                        # 导出为单个Excel文件，多个sheet
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            for table_display, df in data_dict.items():
                                sheet_name = table_display[:31]  # Excel sheet name max 31 chars
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        data = output.getvalue()
                        file_name = f"batch_export_{timestamp}.xlsx"
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        
                        # 显示统计信息
                        st.success(f"{get_text('batch_complete')} {len(data_dict)} {get_text('data_tables')}")
                        for table, count in export_stats.items():
                            st.info(f"  • {table}: {count} {get_text('records')}")
                        
                    else:  # CSV格式，打包为ZIP
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for table_display, df in data_dict.items():
                                csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                                file_name_in_zip = f"{table_mapping.get(table_display, table_display)}_{timestamp}.csv"
                                zip_file.writestr(file_name_in_zip, csv_data)
                        
                        data = zip_buffer.getvalue()
                        file_name = f"batch_export_{timestamp}.zip"
                        mime_type = "application/zip"
                        
                        # 显示统计信息
                        st.success(f"{get_text('batch_complete')} {len(data_dict)} {get_text('data_tables')}")
                        for table, count in export_stats.items():
                            st.info(f"  • {table}: {count} {get_text('records')}")
                    
                    # 提供下载按钮
                    st.download_button(
                        label=get_text('batch_download_zip'),
                        data=data,
                        file_name=file_name,
                        mime=mime_type,
                        use_container_width=True,
                        key=f"download_{timestamp}"
                    )
                    
                    # 记录日志
                    username = st.session_state.get('username', '')
                    role = st.session_state.get('role', '')
                    db.insert_system_log(
                        action_type="EXPORT",
                        details=f"批量导出操作 - 导出{len(selected_tables)}个表，格式: {export_format}, 总记录数: {sum(export_stats.values())}",
                        username=username,
                        role=role
                    )
                except Exception as e:
                    st.error(f"{get_text('export_error')}: {str(e)}")
                    st.info(get_text('db_check_connection'))
    # 快速导出选项
    st.markdown(f"### {get_text('quick_export_options')}")
    
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        if st.button(f"{get_text('export_current_month')}", use_container_width=True):
            with st.spinner(get_text('preparing_month_data')):
                try:
                    current_month = datetime.now().strftime("%Y-%m")
                    db = get_db_manager()
                    
                    # === 新增：获取用户国家限制 ===
                    user_country = st.session_state.user_info.get('country')
                    
                    # 1. 构建统计查询 (Stats Query)
                    if user_country:
                        # 业务员：只能查自己国家的数据
                        query = """
                            SELECT 'Display' as source, COUNT(*) as records FROM Display WHERE h_Time = %s AND Country = %s
                            UNION ALL
                            SELECT 'History', COUNT(*) FROM History WHERE h_Time = %s AND Country = %s
                            UNION ALL
                            SELECT 'Budget', COUNT(*) FROM Budget WHERE h_Time = %s AND Country = %s
                            UNION ALL
                            SELECT 'Costs', COUNT(*) FROM Costs WHERE Costs_time = %s AND Country = %s
                        """
                        # 参数需要翻倍：(时间, 国家, 时间, 国家...)
                        params = (current_month, user_country) * 4
                    else:
                        # 经理/财务：查所有
                        query = """
                            SELECT 'Display' as source, COUNT(*) as records FROM Display WHERE h_Time = %s
                            UNION ALL
                            SELECT 'History', COUNT(*) FROM History WHERE h_Time = %s
                            UNION ALL
                            SELECT 'Budget', COUNT(*) FROM Budget WHERE h_Time = %s
                            UNION ALL
                            SELECT 'Costs', COUNT(*) FROM Costs WHERE Costs_time = %s
                        """
                        params = (current_month, current_month, current_month, current_month)
                    
                    stats = db.execute_query(query, params)
                    
                    if not stats.empty:
                        total_records = stats['records'].sum()
                        st.success(f"{get_text('month_data_stats')} {total_records} {get_text('records')}")
                        for _, row in stats.iterrows():
                            st.info(f"  • {row['source']}: {row['records']} {get_text('records')}")
                                                # 提供导出按钮
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            for table in ['Display', 'History', 'Budget', 'Costs']:
                                time_col = 'Costs_time' if table == 'Costs' else 'h_Time'
                                
                                # === 修改：加入国家筛选 ===
                                if user_country:
                                    sql = f"SELECT * FROM {table} WHERE {time_col} = %s AND Country = %s"
                                    p = (current_month, user_country)
                                else:
                                    sql = f"SELECT * FROM {table} WHERE {time_col} = %s"
                                    p = (current_month,)
                                
                                df = db.execute_query(sql, p)
                                if not df.empty:
                                    df.to_excel(writer, sheet_name=table, index=False)
                        
                        st.download_button(
                            label=get_text('download_month_excel'),
                            data=output.getvalue(),
                            file_name = get_text('download_month_data').format(current_month=current_month),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    else:
                        st.warning(f"{get_text('no_month_data')} ({current_month})")
                
                    db.insert_system_log(
                        action_type="EXPORT",
                        details=f"快速导出本月数据 - 月份: {current_month}, 导出表格: Display, History, Budget, Costs",
                        username=st.session_state.get('username', ''),
                        role=st.session_state.get('role', '')
                    )        
                except Exception as e:
                    st.error(f"{get_text('export_month_failed')}: {str(e)}")
    
    with col_q2:
        if st.button(f"{get_text('export_last_quarter')}", use_container_width=True):
            with st.spinner(get_text('preparing_quarter_data')):
                try:
                    # ... (计算 start_date, end_date 的代码保持不变) ...
                    # 复制你原来的计算日期代码放在这里
                    now = datetime.now()
                    quarter_start_month = ((now.month - 1) // 3) * 3 - 2
                    if quarter_start_month <= 0:
                        quarter_start_month += 12
                        year = now.year - 1
                    else:
                        year = now.year
                    start_date = f"{year}-{quarter_start_month:02d}"
                    end_date = f"{year}-{quarter_start_month+2:02d}"

                    db = get_db_manager()
                    user_country = st.session_state.user_info.get('country')
                    
                    # 1. 统计查询
                    if user_country:
                        query = """
                            SELECT 'Display' as source, COUNT(*) as records FROM Display WHERE (h_Time BETWEEN %s AND %s) AND Country = %s
                            UNION ALL
                            SELECT 'History', COUNT(*) FROM History WHERE (h_Time BETWEEN %s AND %s) AND Country = %s
                            UNION ALL
                            SELECT 'Budget', COUNT(*) FROM Budget WHERE (h_Time BETWEEN %s AND %s) AND Country = %s
                        """
                        params = (start_date, end_date, user_country) * 3
                    else:
                        query = """
                            SELECT 'Display' as source, COUNT(*) as records FROM Display WHERE h_Time BETWEEN %s AND %s
                            UNION ALL
                            SELECT 'History', COUNT(*) FROM History WHERE h_Time BETWEEN %s AND %s
                            UNION ALL
                            SELECT 'Budget', COUNT(*) FROM Budget WHERE h_Time BETWEEN %s AND %s
                        """
                        params = (start_date, end_date) * 3

                    stats = db.execute_query(query, params)
                    
                    if not stats.empty:
                        total_records = stats['records'].sum()
                        st.success(f"{get_text('quarter_data_stats')} ({start_date}~{end_date}): {total_records} {get_text('records')}")
                        
                        # 提供导出按钮
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            for table in ['Display', 'History', 'Budget']:
                                if user_country:
                                    sql = f"SELECT * FROM {table} WHERE (h_Time BETWEEN %s AND %s) AND Country = %s"
                                    p = (start_date, end_date, user_country)
                                else:
                                    sql = f"SELECT * FROM {table} WHERE h_Time BETWEEN %s AND %s"
                                    p = (start_date, end_date)
                                
                                df = db.execute_query(sql, p)
                                if not df.empty:
                                    df.to_excel(writer, sheet_name=table, index=False)
                        
                        st.download_button(
                            label=f"{get_text('download_quarter_data')} ({start_date}~{end_date})",
                            data=output.getvalue(),
                            file_name = get_text('download_quarter_data_file').format(start_date=start_date, end_date=end_date),

                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    else:
                        st.warning(f"{get_text('no_quarter_data')} ({start_date}~{end_date})")
                    db.insert_system_log(
                        action_type="EXPORT",
                        details=f"快速导出季度数据 - 季度: {start_date}~{end_date}, 导出表格: Display, History, Budget",
                        username=st.session_state.get('username', ''),
                        role=st.session_state.get('role', '')
                    )    
                except Exception as e:
                    st.error(f"{get_text('export_quarter_failed')}: {str(e)}")
    
    with col_q3:
        user_country = st.session_state.user_info.get('country')
        if not user_country: 
            if st.button(f"{get_text('export_all_data')}", use_container_width=True):
                with st.spinner(get_text('preparing_all_data')):
                    try:
                        db = get_db_manager()
                        
                        # 统计所有表的数据量
                        tables = ['Display', 'History', 'Budget', 'Costs', 'Sales_Price', 'Exchange', 'Regional_Expenses']
                        stats = {}
                        
                        for table in tables:
                            query = f"SELECT COUNT(*) as count FROM {table}"
                            df = db.execute_query(query)
                            if not df.empty:
                                stats[table] = df.iloc[0]['count']
                        
                        if sum(stats.values()) > 0:
                            st.success(get_text('all_data_stats'))
                            for table, count in stats.items():
                                if count > 0:
                                    st.info(f"  • {table}: {count} 条记录")
                            
                            # 由于数据量可能很大，提示用户
                            st.warning(get_text('all_data_warning'))
                            
                        else:
                            st.warning(get_text('no_data_in_db'))
                        db.insert_system_log(
                            action_type="VIEW",  # 这是查看统计，不是实际导出
                            details=f"查看所有数据统计 - 共计{sum(stats.values())}条记录",
                            username=st.session_state.get('username', ''),
                            role=st.session_state.get('role', '')
                        )    
                    except Exception as e:
                        st.error(f"{get_text('get_stats_failed')}: {str(e)}")
        else:
            # 业务员看到的占位符，或者什么都不显示
            st.button(f"{get_text('export_all_data')}", disabled=True, help="权限受限：仅管理员可导出全库备份", use_container_width=True)

def main():
    """主函数 - 整合的仪表盘"""
    # 标题
    st.markdown(f'<div class="main-header">{get_text("dashboard_header")}</div>', unsafe_allow_html=True)
    
    # 欢迎消息
    user_name = st.session_state.get('name', get_text('unknown_user'))
    st.markdown(f"### {get_text('welcome')} {user_name}!")
    
    # 用户中心部分
    show_user_profile_section()
    
    # 系统状态监控
    show_system_status_section()
    
    # --- 快速访问 ---
    st.markdown(f"## {get_text('function_reconmmend')}")

    col1, col2 = st.columns(2)

    # 卡片 1：数据填报
    with col1:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location='pages/2_data_entry.py'">
            <h3>{get_text('card_entry_title')}</h3>
            <p>{get_text('card_entry_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

    # 卡片 2：对比分析  
    with col2:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location='pages/8_analysis.py'">
            <h3>{get_text('card_analysis_title')}</h3>
            <p>{get_text('card_analysis_desc')}</p>
        </div>
        """, unsafe_allow_html=True)   
    st.markdown("---")
    
    # 批量导出功能
    show_batch_export_section()
    
    st.markdown("---")
    
    # 退出按钮
    st.markdown("""
        <style>
        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #FF4B4B !important;
            border-color: #FF4B4B !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #FF3333 !important;
            border-color: #FF3333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    logout_btn = st.button(get_text('logout'), type="primary", use_container_width=True)
    if logout_btn:
        # 记录登出日志
        try:
            db = get_db_manager()
            username = st.session_state.get('username', '')
            role = st.session_state.get('role', '')
            db.insert_system_log(
                action_type="LOGOUT",
                details=f"用户登出系统 - 用户名: {username}, 角色: {role}",
                username=username,
                role=role
            )
        except:
            pass
        
        # 清除会话状态
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.switch_page("app.py")

if __name__ == "__main__":
    main()