import streamlit as st
import sys
from pathlib import Path

# ================= 1. 路径初始化 (必须在所有自定义导入之前) =================
# 获取当前文件所在目录
current_dir = Path(__file__).parent
# 将 app 目录加入系统路径，确保能找到 utils, config 等模块
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# ================= 2. 自定义模块导入 =================
import base64
from utils.database import get_db_manager
from utils.i18n import init_language, get_text

if 'language' not in st.session_state:
    st.session_state.language = 'zh' # 默认中文

# 获取当前语言的标题
page_title_text = get_text('app_title')

# 设置页面配置
logo_path = current_dir / 'resource' / 'logo.png'
st.set_page_config(
    page_title=page_title_text,
    page_icon=str(logo_path) if logo_path.exists() else "",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # ★★★ 登录页独立的语言切换按钮（右上角位置） ★★★
    col_lang = st.columns([5, 1])[1]
    with col_lang:
        current_idx = 0 if st.session_state.language == 'zh' else 1
        lang = st.selectbox(
            "",
            options=["🇨🇳 中文", "🇺🇸 English"],
            index=current_idx,
            label_visibility="collapsed",
            key="login_lang"
        )
        
        # 切换逻辑
        new_lang = 'zh' if "中文" in lang else 'en'
        if st.session_state.language != new_lang:
            st.session_state.language = new_lang
            st.rerun()
    
    # 加载配置
    from config import USERS, ROLES
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # 使用 get_text 获取文本
            st.markdown(f"<h1 style='text-align: center; color: #003366;'>{get_text('login_page_title')}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #666;'>{get_text('subtitle')}</p>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=True):
                st.markdown(f"##### {get_text('login_title')}")
                user_input = st.text_input("Name / User ID", placeholder=get_text('username_ph'))
                pwd_input = st.text_input("Password", type="password", placeholder=get_text('password_ph'))
                
                submit_btn = st.form_submit_button(get_text('login_btn'), use_container_width=True)
                
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
                        st.success(get_text('login_success'))
                        
                        # ========== 新增：记录登录日志 ==========
                        try:
                            db = get_db_manager()
                            db.insert_system_log(
                                action_type="LOGIN",
                                details=f"用户登录系统 - 用户名: {target_uid}, 姓名: {USERS[target_uid]['name']}, 角色: {USERS[target_uid]['role']}",
                                username=target_uid,
                                role=USERS[target_uid]['role']
                            )
                        except Exception as e:
                            print(f"记录登录日志失败: {e}")
                            # 不影响正常登录流程
                        
                        # 登录后重定向到仪表盘
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error(get_text('login_failed'))
            
            # 测试账号信息
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander(get_text('test_accounts')):
                st.markdown(get_text('test_table'))

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