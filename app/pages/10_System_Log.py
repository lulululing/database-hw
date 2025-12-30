# app/pages/10_System_Log.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
from utils.database import get_db_manager
from utils.i18n import show_sidebar_with_nav, get_text

# ==================== 登录检查 ====================
if not st.session_state.get('logged_in', False):
    st.warning(get_text('login_warning'))
    st.switch_page("app.py")

# ==================== 显示侧边栏导航 ====================
show_sidebar_with_nav()

# ==================== 权限检查 ====================
if 'view_system_log' not in st.session_state.get('permissions', []):
    st.error(get_text('no_permission'))
    st.stop()

# ==================== 页面配置 ====================
st.set_page_config(page_title=get_text('nav_log'), layout="wide")
st.title(get_text('nav_log'))

def main():
    """系统日志查看页面"""
    
    # ========== 获取当前用户信息 ==========
    current_role = st.session_state.get('role', '')
    current_username = st.session_state.get('username', '')
    is_manager = current_role == 'Manager'
    
    # ========== 筛选条件区域 ==========
    # 创建4列布局用于筛选条件
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # 用户名筛选
        db = get_db_manager()
        if is_manager:
            # 经理可以查看所有用户
            all_users_query = "SELECT DISTINCT Username FROM System_Log ORDER BY Username"
            try:
                users_df = db.execute_query(all_users_query)
                all_users_list = [get_text('log_all_users')] + users_df['Username'].tolist()
                selected_user = st.selectbox(
                    get_text('log_filter_user'),
                    all_users_list,
                    index=0
                )
            except:
                selected_user = st.selectbox(
                    get_text('log_filter_user'),
                    [get_text('log_all_users')],
                    index=0
                )
        else:
            # 普通用户只能查看自己
            selected_user = st.selectbox(
                get_text('log_filter_user'),
                [current_username],
                index=0,
                disabled=True
            )
    
    with col2:
        # 角色筛选
        if is_manager:
            role_query = "SELECT DISTINCT Role FROM System_Log ORDER BY Role"
            try:
                roles_df = db.execute_query(role_query)
                all_roles_list = [get_text('log_all_roles')] + roles_df['Role'].tolist()
                selected_role = st.selectbox(
                    get_text('log_filter_role'),
                    all_roles_list,
                    index=0
                )
            except:
                all_roles_list = [get_text('log_all_roles'), "Manager", "User"]
                selected_role = st.selectbox(
                    get_text('log_filter_role'),
                    all_roles_list,
                    index=0
                )
        else:
            # 普通用户角色固定
            selected_role = st.selectbox(
                get_text('log_filter_role'),
                [current_role],
                index=0,
                disabled=True
            )
    
    with col3:
        # 开始时间筛选
        start_date = st.date_input(
            get_text('log_start_date'),
            value=datetime.now() - timedelta(days=30),
            key="log_start_date"
        )
    
    with col4:
        # 结束时间筛选
        end_date = st.date_input(
            get_text('log_end_date'),
            value=datetime.now(),
            key="log_end_date"
        )
    
    # 第二行筛选条件 - 删除搜索框，只保留操作类型和刷新按钮
    col5, col6 = st.columns([3, 1])
    
    with col5:
        # 操作类型筛选
        # 使用i18n.py中的映射
        action_type_mapping = {
            "LOGIN": get_text('log_action_login'),
            "LOGOUT": get_text('log_action_logout'), 
            "DATA_ENTRY": get_text('log_action_data_entry'),
            "COSTS_ENTRY": get_text('log_action_costs_entry'),
            "EXCHANGE_ENTRY": get_text('log_action_exchange_entry'),
            "EXPENSES_ENTRY": get_text('log_action_expenses_entry'),
            "SALES_ENTRY": get_text('log_action_sales_entry'),
            "DELETE": get_text('log_action_delete'),
            "EXPORT": get_text('log_action_export'),
            "UPDATE": get_text('log_action_update'),
            "VIEW": get_text('log_action_view'),
            "TEST": get_text('log_action_test')
        }
        
        # 获取可选的行动类型（英文值）
        action_options = list(action_type_mapping.keys())
        # 多选时显示翻译后的标签，但保存英文值
        selected_actions = st.multiselect(
            get_text('log_filter_action'),
            options=action_options,
            format_func=lambda x: action_type_mapping.get(x, x),
            default=[]
        )
    
    with col6:
        # 刷新按钮 - 只保留这一个
        if st.button(get_text('log_refresh'), use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # ========== 获取日志数据 ==========
    db = get_db_manager()
    
    # 构建基础查询
    base_query = "SELECT Log_ID, Log_Time, Username, Role, Action_Type, Details FROM System_Log"
    
    # 构建WHERE条件
    conditions = []
    params = []
    
    # 用户名筛选
    if selected_user != get_text('log_all_users'):
        conditions.append("Username = %s")
        params.append(selected_user)
    
    # 角色筛选
    if selected_role != get_text('log_all_roles'):
        conditions.append("Role = %s")
        params.append(selected_role)
    
    # 时间筛选
    if start_date:
        conditions.append("DATE(Log_Time) >= %s")
        params.append(start_date.strftime('%Y-%m-%d'))
    
    if end_date:
        conditions.append("DATE(Log_Time) <= %s")
        params.append(end_date.strftime('%Y-%m-%d'))
    
    # 操作类型筛选（数据库查询）
    if selected_actions:
        placeholders = ', '.join(['%s'] * len(selected_actions))
        conditions.append(f"Action_Type IN ({placeholders})")
        params.extend(selected_actions)
    
    # 构建完整查询
    if conditions:
        query = base_query + " WHERE " + " AND ".join(conditions) + " ORDER BY Log_Time DESC"
    else:
        query = base_query + " ORDER BY Log_Time DESC"
    
    # 执行查询
    try:
        df_logs = db.execute_query(query, params if params else None)
    except Exception as e:
        st.error(get_text('error') + str(e))
        df_logs = pd.DataFrame()
    
    # ========== 数据展示逻辑 ==========
    if not df_logs.empty and len(df_logs) > 0:
        # 数据统计卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_logs = len(df_logs)
            st.metric(get_text('log_total'), total_logs)
        
        with col2:
            if 'Username' in df_logs.columns:
                unique_users = df_logs['Username'].nunique()
                st.metric(get_text('log_active_users'), unique_users)
            else:
                st.metric(get_text('log_active_users'), 0)
        
        with col3:
            if 'Log_Time' in df_logs.columns and not df_logs['Log_Time'].empty:
                try:
                    latest_time = pd.to_datetime(df_logs['Log_Time']).max()
                    st.metric(get_text('log_latest'), latest_time.strftime("%Y-%m-%d %H:%M"))
                except:
                    st.metric(get_text('log_latest'), "N/A")
            else:
                st.metric(get_text('log_latest'), "N/A")
        
        with col4:
            if 'Action_Type' in df_logs.columns and not df_logs['Action_Type'].empty:
                # 计算最常见操作类型
                mode_result = df_logs['Action_Type'].mode()
                if not mode_result.empty:
                    most_common_action_en = mode_result.iloc[0]
                    most_common_action_cn = action_type_mapping.get(most_common_action_en, most_common_action_en)
                else:
                    most_common_action_cn = "N/A"
                st.metric(get_text('log_frequent_action'), most_common_action_cn)
            else:
                st.metric(get_text('log_frequent_action'), "N/A")
        
        # 显示数据统计信息
        if 'Username' in df_logs.columns:
            unique_users = df_logs['Username'].nunique()
            st.info(get_text('log_showing').format(count=len(df_logs), users=unique_users))
        
        # 格式化显示
        if 'Log_Time' in df_logs.columns:
            try:
                df_logs['Log_Time'] = pd.to_datetime(df_logs['Log_Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                st.warning(f"时间格式化错误: {e}")
        
        # 准备显示的DataFrame（包含中文操作类型）
        df_display = df_logs.copy()
        if 'Action_Type' in df_display.columns:
            df_display['操作类型'] = df_display['Action_Type'].apply(
                lambda x: action_type_mapping.get(x, x)
            )
        
        # 显示表格
        st.markdown(f"### {get_text('log_records')}")
        
        # 配置列显示 - 简化版，固定所有列
        column_config = {
            'Log_ID': st.column_config.NumberColumn(
                get_text('log_id'),
                width="small"
            ),
            'Log_Time': st.column_config.TextColumn(
                get_text('log_time'), 
                width="medium"
            ),
            'Username': st.column_config.TextColumn(
                get_text('log_username'), 
                width="small"
            ),
            'Role': st.column_config.TextColumn(
                get_text('log_role'), 
                width="medium"
            ),
            '操作类型': st.column_config.TextColumn(
                get_text('log_action'), 
                width="medium"
            ),
            'Details': st.column_config.TextColumn(
                get_text('log_details'), 
                width="large"
            )
        }
        
        # 显示的列顺序
        display_columns = ['Log_ID', 'Log_Time', 'Username', 'Role', '操作类型', 'Details']
        
        # 显示数据表格
        st.dataframe(
            df_display[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            height=500
        )
        
        # 显示记录数统计
        # st.caption(get_text('log_showing').format(count=len(df_display)) + " " + get_text('log_of_total').format(total=len(df_logs)))
        
        # ========== 导出功能 - 简化版 ==========
        with st.container(border=True):
            st.markdown(f"### {get_text('log_export')}")
            
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                # CSV导出 - 固定所有列
                try:
                    # 准备导出数据（英文Action_Type，其他列不变）
                    csv_data = df_logs.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label=get_text('log_export_csv'),
                        data=csv_data,
                        file_name=f"system_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        help=get_text('log_export_csv_help')
                    )
                except Exception as e:
                    st.error(get_text('error') + str(e))
            
            with export_col2:
                # Excel导出 - 固定所有列，包含中文操作类型
                try:
                    output = io.BytesIO()
                    
                    # 创建带中文操作类型的副本
                    df_excel = df_logs.copy()
                    if 'Action_Type' in df_excel.columns:
                        df_excel[get_text('log_action')] = df_excel['Action_Type'].apply(
                            lambda x: action_type_mapping.get(x, x)
                        )
                    
                    # 重命名列用于导出
                    rename_dict = {
                        'Log_ID': get_text('log_id'),
                        'Log_Time': get_text('log_time'),
                        'Username': get_text('log_username'),
                        'Role': get_text('log_role'),
                        'Details': get_text('log_details')
                    }
                    
                    df_excel_renamed = df_excel.rename(columns=rename_dict)
                    
                    # 确定导出列顺序
                    export_columns = [
                        get_text('log_id'),
                        get_text('log_time'),
                        get_text('log_username'),
                        get_text('log_role'),
                        get_text('log_action'),
                        get_text('log_details')
                    ]
                    
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_excel_renamed[export_columns].to_excel(
                            writer, index=False, sheet_name=get_text('nav_log')
                        )
                    
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label=get_text('log_export_excel'),
                        data=excel_data,
                        file_name=f"system_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        help=get_text('log_export_excel_help')
                    )
                except Exception as e:
                    st.error(get_text('error') + str(e))
        
        # ========== 日志分析 ==========
        with st.expander(f"{get_text('log_analysis')}", expanded=False):
            tab1, tab2, tab3 = st.tabs([
                get_text('log_dist_action'), 
                get_text('log_dist_user'), 
                get_text('log_time_trend')
            ])
            
            with tab1:
                if 'Action_Type' in df_logs.columns and not df_logs['Action_Type'].empty:
                    # 将英文操作类型转换为翻译后的标签用于图表显示
                    action_counts = df_logs['Action_Type'].value_counts()
                    if not action_counts.empty:
                        # 转换为翻译后的标签
                        action_counts_translated = pd.Series({
                            action_type_mapping.get(k, k): v 
                            for k, v in action_counts.items()
                        })
                        st.bar_chart(action_counts_translated)
                    else:
                        st.info("暂无操作类型数据")
                else:
                    st.info("操作类型数据不可用")
            
            with tab2:
                if 'Username' in df_logs.columns and not df_logs['Username'].empty:
                    user_counts = df_logs['Username'].value_counts().head(10)
                    if not user_counts.empty:
                        st.bar_chart(user_counts)
                    else:
                        st.info("暂无用户数据")
                else:
                    st.info("用户数据不可用")
            
            with tab3:
                if 'Log_Time' in df_logs.columns and len(df_logs) > 5:
                    try:
                        # 复制数据以避免修改原始数据
                        df_trend = df_logs.copy()
                        df_trend['Log_Time'] = pd.to_datetime(df_trend['Log_Time'])
                        df_trend['Log_Date'] = df_trend['Log_Time'].dt.date
                        
                        # 按日期统计
                        daily_counts = df_trend.groupby('Log_Date').size().reset_index()
                        daily_counts.columns = [get_text('log_time'), get_text('log_records')]
                        daily_counts = daily_counts.sort_values(get_text('log_time'))
                        
                        if not daily_counts.empty:
                            # 显示趋势图
                            st.line_chart(daily_counts.set_index(get_text('log_time')))
                        else:
                            st.info("无足够数据生成趋势图")
                    except Exception as e:
                        st.warning(f"生成趋势图时出错: {e}")
    
    else:
        # 无数据提示
        st.info(get_text('no_data_found'))
        st.caption("请尝试调整筛选条件或确保System_Log表中有数据")
        
        # 添加快速操作按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("重置筛选条件", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("查看所有日志", use_container_width=True):
                # 重置日期范围为一周
                st.session_state.log_start_date = datetime.now() - timedelta(days=30)
                st.session_state.log_end_date = datetime.now()
                st.rerun()

if __name__ == "__main__":
    main()