# 数据库配置文件
# Database Configuration

# 数据库基础配置
DB_BASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': '大作业-test4',
    'charset': 'utf8mb4'
}

# 默认数据库连接配置（用于应用层权限控制）
DB_CONFIG = {
    **DB_BASE_CONFIG,
    'user': 'root',
    'password': '123456'
}

# MySQL用户权限配置（数据库层权限控制）
# 当USE_DB_ROLES = True时，不同角色使用不同的数据库用户
DB_ROLE_USERS = {
    'Manager': {
        'user': 'manager_user',
        'password': 'manager123456',
        'description': '管理者 - 可查看历史预测预算对比'
    },
    'FBP': {
        'user': 'fbp_user',
        'password': 'fbp123456',
        'description': '财务BP - 可管理财务数据'
    },
    'Salesperson_India': {
        'user': 'sales_india',
        'password': 'india123456',
        'description': '印度业务员 - 只能操作印度数据'
    },
    'Salesperson_Pakistan': {
        'user': 'sales_pakistan',
        'password': 'pakistan123456',
        'description': '巴基斯坦业务员 - 只能操作巴基斯坦数据'
    },
    'Salesperson_SouthAfrica': {
        'user': 'sales_south_africa',
        'password': 'southafrica123456',
        'description': '南非业务员 - 只能操作南非数据'
    },
    'Salesperson_Kenya': {
        'user': 'sales_kenya',
        'password': 'kenya123456',
        'description': '肯尼亚业务员 - 只能操作肯尼亚数据'
    }
}

# 应用配置
APP_CONFIG = {
    'title': '销售数据分析系统',
    'page_icon': '📊',
    'layout': 'wide'
}

# 是否使用数据库层权限控制
# True: 使用MySQL用户权限（更安全，需要先执行 创建用户和权限.sql）
# False: 使用应用层权限控制（更简单，使用root账号）
USE_DB_ROLES = True

# 用户角色配置（应用层权限）
ROLES = {
    'Manager': {
        'password': 'manager123456',
        'permissions': ['view', 'edit', 'export', 'analyze'],
        'db_role': 'Manager',
        'description': '管理者 - 查看对比分析数据'
    },
    'FBP': {
        'password': 'fbp123456',
        'permissions': ['view', 'edit', 'export', 'analyze'],
        'db_role': 'FBP',
        'description': '财务BP - 管理财务数据'
    },
    'Salesperson_India': {
        'password': 'india123456',
        'permissions': ['view', 'edit'],
        'db_role': 'Salesperson_India',
        'description': '印度业务员 - 印度数据'
    },
    'Salesperson_Pakistan': {
        'password': 'pakistan123456',
        'permissions': ['view', 'edit'],
        'db_role': 'Salesperson_Pakistan',
        'description': '巴基斯坦业务员 - 巴基斯坦数据'
    },
    'Salesperson_SouthAfrica': {
        'password': 'southafrica123456',
        'permissions': ['view', 'edit'],
        'db_role': 'Salesperson_SouthAfrica',
        'description': '南非业务员 - 南非数据'
    },
    'Salesperson_Kenya': {
        'password': 'kenya123456',
        'permissions': ['view', 'edit'],
        'db_role': 'Salesperson_Kenya',
        'description': '肯尼亚业务员 - 肯尼亚数据'
    }
}
