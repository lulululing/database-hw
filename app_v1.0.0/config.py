# app/config.py
import streamlit as st

# ================= 1. 数据库连接配置 =================
try:
    # 优先读取 .streamlit/secrets.toml
    db_secrets = st.secrets["mysql"]
    DB_BASE_CONFIG = {
        'host': db_secrets['host'],
        'port': db_secrets['port'],
        'user': db_secrets['username'],
        'password': db_secrets['password'],
        'database': db_secrets['database'],
        'charset': db_secrets['charset']
    }
except FileNotFoundError:
    DB_BASE_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',  # <--- 请修改为你电脑上 MySQL 的真实密码！！！
        'database': '大作业-test4',
        'charset': 'utf8mb4'
    }

DB_CONFIG = DB_BASE_CONFIG
USE_DB_ROLES = True

# ================= 2. 用户名单 (登录用) =================
USERS = {
    'manager_user': {'password': '123', 'role': 'Manager', 'name': '张经理'},
    'fbp_user':     {'password': '123', 'role': 'FBP', 'name': '李财务'},
    'sales_india':  {'password': '123', 'role': 'Salesperson_India', 'name': 'Rahul 🇮🇳', 'country': 'India'},
    'sales_pakistan': {'password': '123', 'role': 'Salesperson_Pakistan', 'name': 'Ahmed 🇵🇰', 'country': 'Pakistan'},
    'sales_south_africa': {'password': '123', 'role': 'Salesperson_SouthAfrica', 'name': 'Botha 🇿🇦', 'country': 'South Africa'},
    'sales_kenya':  {'password': '123', 'role': 'Salesperson_Kenya', 'name': 'Kipchoge 🇰🇪', 'country': 'Kenya'}
}

# ================= 3. 数据库角色映射 (连接用) =================
DB_ROLE_USERS = {
    'Manager': {'user': 'manager_user', 'password': 'manager123456'},
    'FBP': {'user': 'fbp_user', 'password': 'fbp123456'},
    'Salesperson_India': {'user': 'sales_india', 'password': 'india123456'},
    'Salesperson_Pakistan': {'user': 'sales_pakistan', 'password': 'pakistan123456'},
    'Salesperson_SouthAfrica': {'user': 'sales_south_africa', 'password': 'southafrica123456'},
    'Salesperson_Kenya': {'user': 'sales_kenya', 'password': 'kenya123456'}
}

# ================= 4. UI 权限控制 (修正版) =================
ROLES = {
    'Manager': {
        # 经理：查看所有数据 + 分析 + 导出
        'permissions': [
            'view_s_display',  # 查看汇总视图
            'view_display',    # 查看综合视图
            'view_history',    # 查看历史数据
            'view_budget',     # 查看预算数据
            'view_costs',      # 查看成本数据
            'view_price',      # 查看价格表(只读)
            'analyze',         # 对比分析
            'export',          # 报表导出
            'view_user_profile' # 访问个人中心
        ], 
        'db_role': 'Manager',
        'label': '经理 (Manager)'
    },
    'FBP': {
        # FBP：财务人员 - 填报数据 + 查看所有 + 导出报表
        'permissions': [
            'data_entry',           # 数据填报
            'view_display',         # 查看综合视图
            'view_s_display',       # 查看汇总视图
            'view_price',           # 查看价格表(只读)
            'view_history',         # 查看历史数据
            'view_budget',          # 查看预算数据
            'view_costs',           # 查看成本数据
            'analyze',              # 对比分析
            'export',               # 报表导出
            'view_user_profile'     # 访问个人中心
        ], 
        'db_role': 'FBP',
        'label': '财务BP (FBP)'
    },
    'Salesperson_India': {
        # 印度业务员：维护价格表 + 查看本国数据
        'permissions': [
            'edit_price',           # 维护价格表(编辑)
            'view_display_country', # 查看区域视图
            'view_price',           # 查看价格表
            'data_entry',           # 数据填报(可添加)
            'view_user_profile'     # 访问个人中心
        ], 
        'db_role': 'SalespersonIndiaRole',
        'label': '印度业务员'
    },
    'Salesperson_Pakistan': {
        'permissions': [
            'edit_price',           # 维护价格表(编辑)
            'view_display_country', # 查看区域视图
            'view_price',           # 查看价格表
            'data_entry',           # 数据填报(可添加)
            'view_user_profile'     # 访问个人中心
        ], 
        'db_role': 'SalespersonPakistanRole',
        'label': '巴基斯坦业务员'
    },
    'Salesperson_SouthAfrica': {
        'permissions': [
            'edit_price',           # 维护价格表(编辑)
            'view_display_country', # 查看区域视图
            'view_price',           # 查看价格表
            'data_entry',           # 数据填报(可添加)
            'view_user_profile'     # 访问个人中心
        ], 
        'db_role': 'SalespersonSouthAfricaRole',
        'label': '南非业务员'
    },
    'Salesperson_Kenya': {
        'permissions': [
            'edit_price',           # 维护价格表(编辑)
            'view_display_country', # 查看区域视图
            'view_price',           # 查看价格表
            'data_entry',           # 数据填报(可添加)
            'view_user_profile'     # 访问个人中心
        ], 
        'db_role': 'SalespersonKenyaRole',
        'label': '肯尼亚业务员'
    }
}

APP_CONFIG = {
    'title': '销售数据分析系统',
    'layout': 'wide'
}