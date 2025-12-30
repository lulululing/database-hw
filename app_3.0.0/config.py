# app/config.py
import streamlit as st

# ================= 1. 数据库连接配置 =================
try:
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
        'password': '123456',
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

# ================= 4. UI 权限控制 (完善版) =================
ROLES = {
    'Manager': {
        'permissions': [
            'view_s_display',       # 查看汇总视图（历史+预测+预算对比）
            'view_display',         # 查看综合视图
            'view_history',         # 查看历史数据
            'view_budget',          # 查看预算数据
            'view_costs',           # 查看成本数据
            'view_price',           # 查看价格表
            'view_sales_price',     # 查看销售价格视图
            'analyze',              # 预算预测对比分析
            'export',               # 报表导出
            'view_user_profile',    # 访问个人中心
            'view_system_log'       # 查看系统日志
        ], 
        'db_role': 'Manager',
        'label': '经理 (Manager)'
    },
    'FBP': {
        # 财务：录入成本、汇率、费用（4个expenses）和机型、国家数据
        'permissions': [
            'data_entry_costs',     # 录入成本数据
            'data_entry_exchange',  # 录入汇率数据
            'data_entry_expenses',  # 录入4类费用数据
            'data_entry_model',     # 录入机型数据
            'data_entry_country',   # 录入国家数据
            'view_display',         # 查看综合视图（所有国家）
            'view_history',         # 查看历史数据
            'view_budget',          # 查看预算数据
            'view_costs',           # 查看成本数据
            'view_price',           # 查看价格表
            'view_sales_price',     # 查看销售价格
            'analyze',              # 对比分析
            'export',               # 报表导出
            'view_user_profile',    # 访问个人中心
            'delete_own_data'       # 删除自己录入的数据
        ], 
        'db_role': 'FBP',
        'label': '财务BP (FBP)'
    },
    'Salesperson_India': {
        # 印度业务员：录入销售量、售价、币种；查看本国所有视图
        'permissions': [
            'data_entry_sales',     # 录入销售量和售价
            'data_entry_currency',  # 录入币种
            'edit_price',           # 维护价格表（编辑）
            'view_display_country', # 查看本国综合视图（DisplayIndia）
            'view_sales_country',   # 查看本国销售视图（Sales_Price_India）
            'view_history_country', # 查看本国历史数据
            'view_budget_country',  # 查看本国预算数据
            'view_costs_country',   # 查看本国成本数据
            'view_price',           # 查看价格表
            'view_user_profile',    # 访问个人中心
            'delete_own_data'       # 删除自己录入的数据
        ], 
        'db_role': 'SalespersonIndiaRole',
        'label': '印度业务员',
        'country_view': 'DisplayIndia',
        'sales_view': 'Sales_Price_India'
    },
    'Salesperson_Pakistan': {
        'permissions': [
            'data_entry_sales',
            'data_entry_currency',
            'edit_price',
            'view_display_country',
            'view_sales_country',
            'view_history_country',
            'view_budget_country',
            'view_costs_country',
            'view_price',
            'view_user_profile',
            'delete_own_data'
        ], 
        'db_role': 'SalespersonPakistanRole',
        'label': '巴基斯坦业务员',
        'country_view': 'DisplayPakistan',
        'sales_view': 'Sales_Price_Pakistan'
    },
    'Salesperson_SouthAfrica': {
        'permissions': [
            'data_entry_sales',
            'data_entry_currency',
            'edit_price',
            'view_display_country',
            'view_sales_country',
            'view_history_country',
            'view_budget_country',
            'view_costs_country',
            'view_price',
            'view_user_profile',
            'delete_own_data'
        ], 
        'db_role': 'SalespersonSouthAfricaRole',
        'label': '南非业务员',
        'country_view': 'DisplaySouthAfrica',
        'sales_view': 'Sales_Price_South_Africa'
    },
    'Salesperson_Kenya': {
        'permissions': [
            'data_entry_sales',
            'data_entry_currency',
            'edit_price',
            'view_display_country',
            'view_sales_country',
            'view_history_country',
            'view_budget_country',
            'view_costs_country',
            'view_price',
            'view_user_profile',
            'delete_own_data'
        ], 
        'db_role': 'SalespersonKenyaRole',
        'label': '肯尼亚业务员',
        'country_view': 'DisplayKenya',
        'sales_view': 'Sales_Price_Kenya'
    }
}

# ================= 5. 数据单位配置 =================
# 用于前端显示时添加货币符号
CURRENCY_SYMBOLS = {
    'CNY': '¥',
    'CHY': '¥',  # 兼容拼写错误
    'USD': '$',
    'EUR': '€'
}

# 需要添加货币单位的列
CURRENCY_COLUMNS = [
    'Price', 'Revenues', 'Costs', 'Gross_profits', 
    'Margin_profits', 'Net_income', 'RandD_expenses',
    'After_sales_provision', 'Marketing_provision',
    'Marketing_expenses', 'Labor_cost', 'Other_variable_expenses',
    'Other_fixed_expenses', 'Functional_expenses', 'Headquarters_expenses'
]

APP_CONFIG = {
    'title': '销售数据分析系统',
    'layout': 'wide'
}