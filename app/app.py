"""
销售数据分析系统 - 主应用程序
Sales Data Analysis System - Main Application
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径到系统路径
sys.path.append(str(Path(__file__).parent))

from config import APP_CONFIG, ROLES, USE_DB_ROLES
from utils.database import get_db_manager

# 页面配置
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1f77b4;
        color: white;
    }
    .stButton>button:hover {
        background-color: #145a8c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'db_role' not in st.session_state:
        st.session_state.db_role = None
    if 'permissions' not in st.session_state:
        st.session_state.permissions = []


def login_page():
    """登录页面"""
    st.markdown('<div class="main-header">📊 销售数据分析系统</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 用户登录")
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.selectbox(
                "选择角色",
                options=list(ROLES.keys()),
                help="选择您的用户角色"
            )
            
            password = st.text_input(
                "密码",
                type="password",
                help="输入对应角色的密码"
            )
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit = st.form_submit_button("🚀 登录", use_container_width=True)
            
            if submit:
                if password == ROLES[username]['password']:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = username
                    st.session_state.db_role = ROLES[username].get('db_role', None)
                    st.session_state.permissions = ROLES[username]['permissions']
                    st.success(f"✅ 欢迎，{username}！")
                    st.rerun()
                else:
                    st.error("❌ 密码错误，请重试！")
        
        st.markdown("---")
        st.info("""
        **测试账号信息：**
        
        📊 **管理层：**
        - 👨‍💼 Manager（经理）: manager123 - 查看对比分析
        
        💰 **财务：**
        - � FBP（财务BP）: fbp123 - 管理财务数据
        
        🌍 **业务员：**
        - 🇮🇳 Salesperson_India: india123 - 印度数据
        - 🇵🇰 Salesperson_Pakistan: pakistan123 - 巴基斯坦数据
        - 🇿🇦 Salesperson_SouthAfrica: southafrica123 - 南非数据
        - 🇰🇪 Salesperson_Kenya: kenya123 - 肯尼亚数据
        """)


def logout():
    """退出登录"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.db_role = None
    st.session_state.permissions = []
    # 清除数据库连接缓存
    st.cache_resource.clear()
    st.rerun()


def main_app():
    """主应用界面"""
    
    # 侧边栏
    with st.sidebar:
        st.markdown(f"### 👤 当前用户")
        st.info(f"**角色**: {st.session_state.role}")
        
        # 显示数据库连接方式
        if USE_DB_ROLES and st.session_state.db_role:
            st.success(f"🔒 使用专属数据库用户")
        else:
            st.warning(f"⚠️ 使用共享数据库连接")
        
        st.markdown("---")
        
        st.markdown("### 📋 导航菜单")
        
        # 页面选择
        page = st.radio(
            "选择功能",
            options=[
                "🏠 首页",
                "📊 历史数据查询",
                "💰 预算数据查询",
                "💵 销售价格数据",
                "💸 成本数据",
                "📈 数据分析对比",
                "📑 报表生成",
                "⚙️ 系统设置"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 退出登录", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.caption("© 2025 销售数据分析系统")
    
    # 主内容区域
    if page == "🏠 首页":
        show_home_page()
    elif page == "📊 历史数据查询":
        show_history_page()
    elif page == "💰 预算数据查询":
        show_budget_page()
    elif page == "💵 销售价格数据":
        show_sales_price_page()
    elif page == "💸 成本数据":
        show_costs_page()
    elif page == "📈 数据分析对比":
        show_analysis_page()
    elif page == "📑 报表生成":
        show_report_page()
    elif page == "⚙️ 系统设置":
        show_settings_page()


def show_home_page():
    """首页"""
    st.markdown('<div class="main-header">🏠 欢迎使用销售数据分析系统</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📌 系统概述")
        st.markdown("""
        本系统是一个综合性的**销售数据分析平台**，用于管理和分析企业的销售、预算、成本等关键业务数据。
        
        **主要功能模块：**
        
        1. **📊 数据查询**
           - 历史销售数据查询
           - 预算数据查询
           - 价格和成本数据管理
        
        2. **📈 数据分析**
           - 预算 vs 实际对比分析
           - 多维度数据汇总
           - 趋势分析和可视化
        
        3. **📑 报表生成**
           - 按国家/产品/时间生成报表
           - 支持Excel导出
           - 自定义查询条件
        
        4. **👥 权限管理**
           - 多角色权限控制
           - 数据安全保护
        """)
    
    with col2:
        st.markdown("### 👤 当前用户信息")
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎭 角色</h4>
            <p style="font-size: 1.5rem; font-weight: bold;">{st.session_state.role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔑 权限说明")
        permissions = st.session_state.permissions
        perm_icons = {
            'view': '👁️ 查看数据',
            'edit': '✏️ 编辑数据',
            'export': '📤 导出报表',
            'analyze': '📊 数据分析'
        }
        for perm in permissions:
            st.success(perm_icons.get(perm, perm))
    
    # 获取数据库连接
    db = get_db_manager()
    
    # 显示关键指标
    st.markdown("---")
    st.markdown("### 📊 关键业务指标")
    
    try:
        # 获取汇总数据
        time_series = db.get_time_series_data()
        
        if time_series is not None and not time_series.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            latest = time_series.iloc[-1]
            
            with col1:
                st.metric(
                    label="📅 最新统计期间",
                    value=latest['时间']
                )
            
            with col2:
                st.metric(
                    label="📦 总销量",
                    value=f"{int(latest['总销量']):,}"
                )
            
            with col3:
                st.metric(
                    label="💰 总收入",
                    value=f"¥{latest['总收入']:,.2f}"
                )
            
            with col4:
                st.metric(
                    label="💵 总净收入",
                    value=f"¥{latest['总净收入']:,.2f}"
                )
            
            st.markdown("---")
            st.markdown("### 📈 销售趋势")
            st.line_chart(time_series.set_index('时间')[['总销量', '总收入', '总净收入']])
        else:
            st.warning("⚠️ 暂无数据，请先在数据库中添加历史数据。")
            
    except Exception as e:
        st.error(f"❌ 加载数据失败: {str(e)}")
    
    st.markdown("---")
    st.info("💡 **提示**: 使用左侧导航菜单选择不同功能模块进行操作。")


def show_history_page():
    """历史数据查询页面"""
    from pages import history
    history.show()


def show_budget_page():
    """预算数据查询页面"""
    from pages import budget
    budget.show()


def show_sales_price_page():
    """销售价格数据页面"""
    from pages import sales_price
    sales_price.show()


def show_costs_page():
    """成本数据页面"""
    from pages import costs
    costs.show()


def show_analysis_page():
    """数据分析页面"""
    from pages import analysis
    analysis.show()


def show_report_page():
    """报表生成页面"""
    from pages import report
    report.show()


def show_settings_page():
    """系统设置页面"""
    st.markdown('<div class="main-header">⚙️ 系统设置</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔧 数据库配置")
    st.info("""
    **当前数据库配置**
    - 主机: localhost
    - 端口: 3306
    - 数据库: [请在 config.py 中配置]
    
    如需修改数据库连接信息，请编辑 `config.py` 文件中的 `DB_CONFIG` 配置。
    """)
    
    st.markdown("---")
    st.markdown("### 👥 用户角色权限")
    
    for role, info in ROLES.items():
        with st.expander(f"🎭 {role}"):
            st.write(f"**权限列表**: {', '.join(info['permissions'])}")
    
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("""
    1. **数据查询**: 在对应页面选择筛选条件，查看数据
    2. **数据分析**: 支持预算与实际对比、趋势分析等
    3. **报表导出**: 支持导出 Excel 格式报表
    4. **权限控制**: 不同角色拥有不同的操作权限
    """)


def main():
    """主函数"""
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
