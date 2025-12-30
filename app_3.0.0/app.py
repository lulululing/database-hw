# app.py - 修正版
import streamlit as st
import os
import sys
import base64
from pathlib import Path

# ================= 修正路径问题 =================
# 获取当前文件所在目录
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# 设置页面配置
logo_path = current_dir / 'resource' / 'logo.png'
if logo_path.exists():
    st.set_page_config(
        page_title="经营预测数据库系统",
        page_icon=str(logo_path),
        layout="wide",
        initial_sidebar_state="expanded"
    )
else:
    st.set_page_config(
        page_title="经营预测数据库系统",
    page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ================= 语言管理 =================
def init_language():
    """初始化语言设置"""
    if 'language' not in st.session_state:
        st.session_state.language = 'zh'  # 默认中文

def set_language(lang):
    """设置语言"""
    st.session_state.language = lang

def get_text(text_dict):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    return text_dict.get(lang, text_dict.get('zh', ''))

# ================= 样式控制 =================
def set_login_css():
    """登录页面样式"""
    bg_path = current_dir / 'resource' / 'background.jpg'
    
    css = """<style>"""
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            bin_str = base64.b64encode(f.read()).decode()
        css += f"""
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
        }}
        """
    css += """
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stForm"] {
        background-color: rgba(255,255,255,0.95);
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        width: 1000px !important;          /* 固定宽度 */
        max-width: 90% !important;        /* 响应式：在小屏幕上不超过90% */
        margin: 0 auto !important;        /* 水平居中 */
        min-height: 400px;                /* 可选：设置最小高度 */
    }
    .language-switcher {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
     /* 修改标题盒子样式 */
    .stTitle, 
    div[data-testid="stTitle"],
    .title-container,
    h1, h2, h3, h4, h5, h6 { 
        /* 调整盒子宽度 */
        max-width: 100% !important;          /* 最大宽度 */
        min-width: 300px !important;        /* 最小宽度 */
        
        /* 文字居中 */
        text-align: center !important;
    }
    
    /* 只针对主标题容器的特定样式 */
    .main-title-container {
        padding: 30px 40px !important;
        margin: 20px auto !important;
        width: 500px !important;            /* 固定宽度 */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }

    """
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

# ================= 会话管理 =================
def init_session():
    """初始化会话状态"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.session_state.name = ''
        st.session_state.role = ''
        st.session_state.permissions = []
        st.session_state.user_info = {}

# ================= 登录页面 =================
def login_page():
    """登录页面"""
    set_login_css()
    
    # 语言切换按钮
    col_lang = st.columns([5, 1])[1]
    with col_lang:
        lang = st.selectbox(
            "",
            options=["🇨🇳 中文", "🇺🇸 English"],
            index=0 if st.session_state.language == 'zh' else 1,
            label_visibility="collapsed",
            key="login_lang"
        )
        if "中文" in lang:
            set_language('zh')
        else:
            set_language('en')
    
    # 加载配置
    from config import USERS, ROLES
    
    # 定义多语言文本
    text = {
        'zh': {
            'title': '经营预测数据库系统',
            'subtitle': '数据驱动的业务智能平台',
            'login_title': '用户登录',
            'username_placeholder': '例如：张经理 或 manager_user',
            'password_placeholder': '请输入密码',
            'login_button': '登录',
            'login_success': '登录成功！',
            'login_failed': '认证失败：账号不存在或密码错误',
            'test_accounts': '测试账号信息',
            'test_table': """
            | 角色 | 账号(ID) | 姓名 | 密码 |
            |---|---|---|---|
            | **经理** | `manager_user` | 张经理 | `123` |
            | **财务** | `fbp_user` | 李财务 | `123` |
            | **印度业务** | `sales_india` | Rahul | `123` |
            | **巴基斯坦** | `sales_pakistan` | Ahmed | `123` |
            | **南非业务** | `sales_south_africa` | Botha | `123` |
            | **肯尼亚** | `sales_kenya` | Kipchoge | `123` |
            """
        },
        'en': {
            'title': 'Sales Data Analysis System',
            'subtitle': 'Data-driven business intelligence platform',
            'login_title': 'User Login',
            'username_placeholder': 'e.g., Zhang Manager or manager_user',
            'password_placeholder': 'Enter your password',
            'login_button': 'Login',
            'login_success': 'Login successful!',
            'login_failed': 'Authentication failed: User not found or password incorrect',
            'test_accounts': 'Test Account Information',
            'test_table': """
            | Role | User ID | Name | Password |
            |---|---|---|---|
            | **Manager** | `manager_user` | Zhang Manager | `123` |
            | **FBP** | `fbp_user` | Li Finance | `123` |
            | **India Sales** | `sales_india` | Rahul | `123` |
            | **Pakistan Sales** | `sales_pakistan` | Ahmed | `123` |
            | **South Africa Sales** | `sales_south_africa` | Botha | `123` |
            | **Kenya Sales** | `sales_kenya` | Kipchoge | `123` |
            """
        }
    }
    
    current_text = text[st.session_state.language]
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2,1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            st.markdown(f"<h1 style='text-align: center; color: #003366;'>{current_text['title']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #666;'>{current_text['subtitle']}</p>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=True):
                st.markdown(f"##### {current_text['login_title']}")
                user_input = st.text_input("Name / User ID", placeholder=current_text['username_placeholder'])
                pwd_input = st.text_input("Password", type="password", placeholder=current_text['password_placeholder'])
                
                submit_btn = st.form_submit_button(current_text['login_button'], use_container_width=True)
                
                if submit_btn:
                    # 1. 查找用户
                    target_uid = None
                    if user_input in USERS:
                        target_uid = user_input
                    else:
                        for uid, info in USERS.items():
                            if info['name'] == user_input:
                                target_uid = uid
                                break
                    
                    # 2. 校验密码
                    if target_uid and USERS[target_uid]['password'] == pwd_input:
                        st.session_state.logged_in = True
                        st.session_state.username = target_uid
                        st.session_state.name = USERS[target_uid]['name']
                        st.session_state.role = USERS[target_uid]['role']
                        st.session_state.permissions = ROLES[USERS[target_uid]['role']]['permissions']
                        st.session_state.user_info = {
                            'id': target_uid,
                            'name': USERS[target_uid]['name'],
                            'role': USERS[target_uid]['role'],
                            'country': USERS[target_uid].get('country'),
                            'db_role': ROLES[USERS[target_uid]['role']].get('db_role', 'Default')
                        }
                        st.success(current_text['login_success'])
                        # 登录后重定向到仪表盘
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error(current_text['login_failed'])
            
            # 测试账号信息
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander(current_text['test_accounts']):
                st.markdown(current_text['test_table'])

def home_page():
    """主页 - 如果直接访问app.py，重定向到仪表盘或登录页"""
    if st.session_state.logged_in:
        st.switch_page("pages/1_Dashboard.py")
    else:
        login_page()

# ================= 主程序 =================
if __name__ == "__main__":
    init_language()
    init_session()
    home_page()