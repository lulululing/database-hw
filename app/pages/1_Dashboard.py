import streamlit as st
from utils.database import get_db_manager

# 检查登录状态
if not st.session_state.get('logged_in', False):
    st.warning("请先登录")
    st.switch_page("app.py")

# 设置页面标题
st.set_page_config(
    page_title="用户中心",
    layout="wide"
)
st.title("用户中心 - 销售数据分析")  
# 语言管理函数
def set_language(lang):
    """设置语言"""
    st.session_state.language = lang

def get_text(text_dict):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    return text_dict.get(lang, text_dict.get('zh', ''))

# 自定义样式
st.markdown("""
<style>
.metric-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #eee;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
    cursor: pointer;  /* 添加光标指针 */
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
.main-header {
    font-size: 1.8rem;
    font-weight: bold;
    color: #1f77b4;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #eee;
}
.user-profile-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
}
.permission-badge {
    display: inline-block;
    background-color: rgba(255,255,255,0.2);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    margin: 0.2rem;
    font-size: 0.8rem;
}
.language-switcher-sidebar {
    position: fixed;
    bottom: 20px;
    left: 20px;
}
</style>
""", unsafe_allow_html=True)

def show_user_profile_section():
    """用户中心部分"""
    # 多语言文本
    text = {
        'zh': {
            'welcome': '👋 欢迎回来，',
            'role': '角色',
            'user_id': '用户ID',
            'permissions': '🔐 您的权限',
            'system_info': '📋 系统信息',
            'login_time': '登录时间',
            'permission_count': '权限数量',
            'database_role': '数据库角色',
            'logout': '🚪 退出登录'
        },
        'en': {
            'welcome': '👋 Welcome back, ',
            'role': 'Role',
            'user_id': 'User ID',
            'permissions': '🔐 Your Permissions',
            'system_info': '📋 System Information',
            'login_time': 'Login Time',
            'permission_count': 'Permission Count',
            'database_role': 'Database Role',
            'logout': '🚪 Logout'
        }
    }
    current_text = get_text(text)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(f"https://api.dicebear.com/7.x/initials/svg?seed={st.session_state.name}", width=100)
    
    with col2:
        st.markdown(f"# {st.session_state.name}")
        st.markdown(f"### {st.session_state.role}")
        st.caption(f"{current_text['user_id']}: {st.session_state.username}")
    
    # 权限展示
    st.markdown(f"### {current_text['permissions']}")
    
    # 权限翻译字典
    perm_map = {
        'zh': {
            'data_entry': '📝 数据填报',
            'view_display': '👁️ 综合视图',
            'view_s_display': '📊 汇总视图',
            'view_history': '📜 历史数据',
            'view_budget': '💰 预算数据',
            'view_costs': '💸 成本明细',
            'view_price': '🏷️ 价格查看',
            'edit_price': '✏️ 价格管理',
            'view_display_country': '🌍 区域视图',
            'analyze': '📈 对比分析',
            'export': '📤 报表导出',
            'view_user_profile': '👤 用户中心'
        },
        'en': {
            'data_entry': '📝 Data Entry',
            'view_display': '👁️ Display View',
            'view_s_display': '📊 Summary View',
            'view_history': '📜 History Data',
            'view_budget': '💰 Budget Data',
            'view_costs': '💸 Cost Details',
            'view_price': '🏷️ Price View',
            'edit_price': '✏️ Price Management',
            'view_display_country': '🌍 Regional View',
            'analyze': '📈 Data Analysis',
            'export': '📤 Report Export',
            'view_user_profile': '👤 User Profile'
        }
    }
    
    user_perms = st.session_state.permissions
    current_lang = st.session_state.get('language', 'zh')
    
    # 显示所有权限徽章
    cols = st.columns(4)
    for idx, perm in enumerate(user_perms):
        with cols[idx % 4]:
            readable_perm = perm_map[current_lang].get(perm, perm)
            st.markdown(f"**{readable_perm}**")
    
    # 系统信息
    with st.expander(current_text['system_info']):
        from datetime import datetime
        st.write(f"{current_text['login_time']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"{current_text['permission_count']}: {len(user_perms)}")
        st.write(f"{current_text['database_role']}: {st.session_state.user_info.get('db_role', 'Default')}")
    
    # 退出按钮
    if st.button(current_text['logout'], type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.switch_page("app.py")

def show_dashboard_content():
    """仪表盘内容"""
    # 多语言文本
    text = {
        'zh': {
            'quick_access': '🚀 快速访问',
            'data_entry': '📝 数据填报',
            'data_entry_desc': '快速录入销售数据',
            'go_to_entry': '前往填报',
            'data_analysis': '📈 对比分析',
            'data_analysis_desc': '查看历史与预算对比',
            'start_analysis': '开始分析',
            'report_generation': '📋 报表生成',
            'report_generation_desc': '生成各类业务报表',
            'generate_report': '生成报表',
            'system_status': '🏢 系统状态',
            'db_connected': '✅ 数据库连接正常',
            'db_failed': '❌ 数据库连接失败',
            'db_check_failed': '⚠️ 数据库状态检查失败',
            'time_periods': '时间周期',
            'countries': '国家数量',
            'product_models': '产品型号'
        },
        'en': {
            'quick_access': '🚀 Quick Access',
            'data_entry': '📝 Data Entry',
            'data_entry_desc': 'Quickly input sales data',
            'go_to_entry': 'Go to Entry',
            'data_analysis': '📈 Data Analysis',
            'data_analysis_desc': 'Compare historical vs budget data',
            'start_analysis': 'Start Analysis',
            'report_generation': '📋 Report Generation',
            'report_generation_desc': 'Generate business reports',
            'generate_report': 'Generate Report',
            'system_status': '🏢 System Status',
            'db_connected': '✅ Database connection is normal',
            'db_failed': '❌ Database connection failed',
            'db_check_failed': '⚠️ Database status check failed',
            'time_periods': 'Time Periods',
            'countries': 'Countries',
            'product_models': 'Product Models'
        }
    }
    current_text = get_text(text)
    
    st.markdown(f"### {current_text['quick_access']}")
    
    col1, col2, col3 = st.columns(3)
    
    # 数据填报卡片
    with col1:
        with st.container():
            # 使用容器包装整个卡片内容
            card_content = f"""
            <div class="metric-card">
                <h3>{current_text['data_entry']}</h3>
                <p style="color: #666; margin-bottom: 20px;">{current_text['data_entry_desc']}</p>
            </div>
            """
            st.markdown(card_content, unsafe_allow_html=True)
            
            # 按钮放在卡片外面
            if st.button(current_text['go_to_entry'], key="home_btn1", use_container_width=True):
                # 确保文件名正确：检查你的pages文件夹中文件的实际名称
                # 如果文件已经重命名为data_entry.py，就用这个
                st.switch_page("pages/2_data_entry.py")
    
    # 对比分析卡片（同理）
    with col2:
        with st.container():
            card_content = f"""
            <div class="metric-card">
                <h3>{current_text['data_analysis']}</h3>
                <p style="color: #666; margin-bottom: 20px;">{current_text['data_analysis_desc']}</p>
            </div>
            """
            st.markdown(card_content, unsafe_allow_html=True)
            
            if st.button(current_text['start_analysis'], key="home_btn2", use_container_width=True):
                # 确保文件名正确
                st.switch_page("pages/8_analysis.py")
    
    # 报表生成卡片（同理）
    with col3:
        with st.container():
            card_content = f"""
            <div class="metric-card">
                <h3>{current_text['report_generation']}</h3>
                <p style="color: #666; margin-bottom: 20px;">{current_text['report_generation_desc']}</p>
            </div>
            """
            st.markdown(card_content, unsafe_allow_html=True)
            
            if st.button(current_text['generate_report'], key="home_btn3", use_container_width=True):
                # 确保文件名正确
                st.switch_page("pages/9_report.py")
    st.markdown("---")
    
    # 系统状态
    st.markdown(f"### {current_text['system_status']}")
    db = get_db_manager()
    
    try:
        # 尝试连接数据库
        if db.connect():
            st.success(current_text['db_connected'])
            
            # 获取一些统计数据
            time_periods = db.get_all_time_periods()
            countries = db.get_all_countries()
            models = db.get_all_models()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(current_text['time_periods'], len(time_periods))
            with col2:
                st.metric(current_text['countries'], len(countries))
            with col3:
                st.metric(current_text['product_models'], len(models))
        else:
            st.error(current_text['db_failed'])
    except Exception as e:
        st.warning(f"{current_text['db_check_failed']}: {str(e)}")

def main():
    """主函数 - 整合的仪表盘"""
# 侧边栏语言切换
    with st.sidebar:
        lang = st.selectbox(
            "🌐 语言 / Language",
            options=["🇨🇳 中文", "🇺🇸 English"],
            index=0 if st.session_state.get('language', 'zh') == 'zh' else 1,
            key="sidebar_lang"
        )
        if "中文" in lang:
            set_language('zh')
        else:
            set_language('en')
    
    # 页面标题
    title_text = {
        'zh': '🏠 仪表盘 & 用户中心',
        'en': '🏠 Dashboard & User Center'
    }
    st.markdown(f'<div class="main-header">{get_text(title_text)}</div>', unsafe_allow_html=True)
    # 创建标签页
    tab_text = {
        'zh': ['👤 用户信息', '📊 快速访问'],
        'en': ['👤 User Profile', '📊 Quick Access']
    }
    current_tabs = tab_text[st.session_state.get('language', 'zh')]
    
    tab1, tab2 = st.tabs(current_tabs)
    
    with tab1:
        show_user_profile_section()
    
    with tab2:
        show_dashboard_content()

if __name__ == "__main__":
    main()