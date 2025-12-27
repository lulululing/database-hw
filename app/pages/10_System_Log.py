# app/pages/10_System_Log.py
import streamlit as st
import pandas as pd
from utils.database import get_db_manager

# 检查登录
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 权限检查：只允许 Manager 查看
if 'view_system_log' not in st.session_state.get('permissions', []):
    st.error("您没有权限访问此页面 (需要 Manager 权限)")
    st.stop()

st.set_page_config(page_title="系统日志", layout="wide")
st.title("系统操作日志")

def main():
    # 刷新和筛选选项
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # 搜索框
        search = st.text_input("搜索日志", placeholder="输入用户ID、角色、操作类型或详情...")
    
    with col2:
        # 按操作类型筛选
        action_filter = st.multiselect(
            "筛选操作类型",
            ["LOGIN", "LOGOUT", "DATA_ENTRY", "COSTS_ENTRY", "EXCHANGE_ENTRY", 
             "EXPENSES_ENTRY", "SALES_ENTRY", "DELETE", "EXPORT"],
            default=[]
        )
    
    with col3:
        if st.button("刷新日志", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # 获取数据
    db = get_db_manager()
    df_logs = db.get_system_logs()
    
    if not df_logs.empty:
        # 数据统计
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总日志数", len(df_logs))
        
        with col2:
            unique_users = df_logs['Username'].nunique() if 'Username' in df_logs.columns else 0
            st.metric("活跃用户数", unique_users)
        
        with col3:
            if 'Log_Time' in df_logs.columns:
                latest_time = pd.to_datetime(df_logs['Log_Time']).max()
                st.metric("最新记录", latest_time.strftime("%Y-%m-%d %H:%M"))
        
        with col4:
            if 'Action_Type' in df_logs.columns:
                most_common_action = df_logs['Action_Type'].mode()[0] if not df_logs['Action_Type'].mode().empty else "N/A"
                st.metric("最频繁操作", most_common_action)
        
        st.markdown("---")
        
        # 应用搜索过滤
        df_display = df_logs.copy()
        
        if search:
            mask = df_display.apply(lambda x: x.astype(str).str.contains(search, case=False).any(), axis=1)
            df_display = df_display[mask]
        
        # 应用操作类型筛选
        if action_filter and 'Action_Type' in df_display.columns:
            df_display = df_display[df_display['Action_Type'].isin(action_filter)]
        
        # 样式化显示
        st.markdown("### 日志记录")
        
        # 格式化时间列
        if 'Log_Time' in df_display.columns:
            df_display['Log_Time'] = pd.to_datetime(df_display['Log_Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # 为不同操作类型添加emoji标记
        # 不再添加emoji
        
        # 显示表格
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Log_Time": st.column_config.TextColumn("时间", width="medium"),
                "Username": st.column_config.TextColumn("用户ID", width="small"),
                "Role": st.column_config.TextColumn("角色", width="medium"),
                "Action_Type": st.column_config.TextColumn("操作类型", width="medium"),
                "Details": st.column_config.TextColumn("详情", width="large")
            },
            height=500
        )
        
        st.caption(f"共显示 {len(df_display)} 条记录（总计 {len(df_logs)} 条）")
        
        # 导出功能
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            csv = df_logs.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="导出完整日志",
                data=csv,
                file_name=f"system_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # 日志分析
        with st.expander("查看日志统计分析"):
            col1, col2 = st.columns(2)
            
            with col1:
                if 'Action_Type' in df_logs.columns:
                    st.markdown("##### 操作类型分布")
                    action_counts = df_logs['Action_Type'].value_counts()
                    st.bar_chart(action_counts)
            
            with col2:
                if 'Username' in df_logs.columns:
                    st.markdown("##### 用户活跃度")
                    user_counts = df_logs['Username'].value_counts().head(10)
                    st.bar_chart(user_counts)
    
    else:
        st.info("暂无日志记录或数据库连接失败")
        st.caption("提示：确保System_Log表已创建且log_event方法被正确调用")

if __name__ == "__main__":
    main()