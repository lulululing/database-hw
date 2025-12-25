# app/pages/10_System_Log.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 权限检查 (可选：只允许 Manager 查看)
if st.session_state.get('role') != 'Manager':
    st.error("您没有权限访问此页面 (需要 Manager 权限)")
    st.stop()

st.set_page_config(page_title="系统日志", layout="wide")
st.title("系统操作日志")

# 刷新按钮
if st.button("刷新日志"):
    st.rerun()

# 获取数据
db = get_db_manager()
df_logs = db.get_system_logs()

if not df_logs.empty:
    # 简单的过滤功能
    search = st.text_input("搜索日志 (用户/操作/详情)", placeholder="输入关键字...")
    
    if search:
        mask = df_logs.apply(lambda x: x.astype(str).str.contains(search, case=False).any(), axis=1)
        df_display = df_logs[mask]
    else:
        df_display = df_logs

    # 样式化显示
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Log_Time": st.column_config.DatetimeColumn("时间", format="Ys-MM-DD HH:mm:ss"),
            "Username": "用户ID",
            "Role": "角色",
            "Action_Type": "操作类型",
            "Details": "详情"
        }
    )
    st.caption(f"共显示 {len(df_display)} 条记录")
else:
    st.info("暂无日志记录或数据库连接失败")