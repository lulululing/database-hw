# app/utils/sql_queries.py
"""
SQL查询语句集中管理 - 完善版
"""

# ==================== 系统日志查询（增强版） ====================
Q_LOG_ACTION = """
    INSERT INTO System_Log (Username, Role, Action_Type, Details)
    VALUES (%s, %s, %s, %s)
"""

# 基础日志查询（保持向后兼容）
Q_GET_SYSTEM_LOGS = """
    SELECT Log_ID, Log_Time, Username, Role, Action_Type, Details
    FROM System_Log
    ORDER BY Log_Time DESC
    LIMIT 1000
"""

# 带筛选的日志查询
Q_GET_SYSTEM_LOGS_FILTERED = """
    SELECT Log_ID, Log_Time, Username, Role, Action_Type, Details
    FROM System_Log
    WHERE 1=1
    {user_filter}
    {role_filter}
    {time_filter}
    {action_filter}
    ORDER BY Log_Time DESC
    {limit_clause}
"""

# 日志统计查询
Q_GET_LOG_STATS = """
    SELECT 
        COUNT(*) as total_logs,
        COUNT(DISTINCT Username) as unique_users,
        MAX(Log_Time) as latest_log,
        (SELECT Action_Type FROM System_Log GROUP BY Action_Type ORDER BY COUNT(*) DESC LIMIT 1) as most_common_action
    FROM System_Log
    WHERE 1=1
    {user_filter}
    {time_filter}
"""

# 获取不重复的用户名列表
Q_GET_DISTINCT_USERS = """
    SELECT DISTINCT Username 
    FROM System_Log 
    ORDER BY Username
"""

# 获取不重复的角色列表
Q_GET_DISTINCT_ROLES = """
    SELECT DISTINCT Role 
    FROM System_Log 
    ORDER BY Role
"""

# 获取不重复的操作类型
Q_GET_DISTINCT_ACTIONS = """
    SELECT DISTINCT Action_Type 
    FROM System_Log 
    ORDER BY Action_Type
"""

# ==================== 基础查询 ====================
Q_GET_ALL_MODELS = """
    SELECT Model, Series, Model_label 
    FROM Model 
    ORDER BY Model
"""

Q_GET_ALL_COUNTRIES = """
    SELECT Country, Market 
    FROM Country 
    ORDER BY Country
"""

Q_GET_TIME_SERIES = """
    SELECT h_Time, 
           SUM(Sales) as total_sales,
           SUM(Revenues) as total_revenue,
           SUM(Net_income) as total_profit
    FROM History
    GROUP BY h_Time
    ORDER BY h_Time
"""

# ==================== 参数表查询（用于财务计算） ====================
Q_GET_ALL_EXCHANGE = """
    SELECT Exchange_time, Exchange_rate 
    FROM Exchange
    ORDER BY Exchange_time DESC
"""

Q_GET_ALL_COSTS = """
    SELECT Costs_id, Model, Country, Costs_time, Costs 
    FROM Costs
    ORDER BY Costs_time DESC, Model, Country
"""

Q_GET_ALL_PRICES = """
    SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
    FROM Sales_Price
    ORDER BY h_Time DESC, Model, Country
"""

Q_GET_ALL_RATIO1 = """
    SELECT Series, 
           Software_product_amortization_rate_acc_cost,
           RandD_rate_acc_cost
    FROM Ratio_Expenses1
    ORDER BY Series
"""

Q_GET_ALL_RATIO2 = """
    SELECT Country,
           Functional_cost_allocation_rate_acc_cost,
           Business_group_headquarters_allocation_rate_acc_cost,
           Marketing_activities_provision_rate_acc_revenue
    FROM Ratio_Expenses2
    ORDER BY Country
"""

Q_GET_ALL_RATIO3 = """
    SELECT Ratio_expenses3_id, Model_label, Country,
           After_sales_provision_rate_acc_cost
    FROM Ratio_Expenses3
    ORDER BY Model_label, Country
"""

Q_GET_ALL_REGIONAL = """
    SELECT Country, Expenses_time,
           Marketing_expenses, Labor_cost,
           Other_variable_expenses, Other_fixed_expenses
    FROM Regional_Expenses
    ORDER BY Expenses_time DESC, Country
"""

Q_GET_MODELS_INFO = """
    SELECT Model, Series, Model_label
    FROM Model
    ORDER BY Model
"""

# ==================== 按时间范围查询 ====================
Q_GET_HISTORY_BY_DATE_RANGE = """
    SELECT h_Time, Country, Market, Model, Model_label, Series, 
           Sales, Revenues, Gross_profits, Margin_profits, Net_income
    FROM History
    WHERE h_Time >= %s AND h_Time <= %s
    ORDER BY h_Time DESC, Country, Model
"""

Q_GET_BUDGET_BY_DATE_RANGE = """
    SELECT h_Time, Country, Market, Model, Model_label, Series, 
           Sales, Revenues, Gross_profits, Margin_profits, Net_income
    FROM Budget
    WHERE h_Time >= %s AND h_Time <= %s
    ORDER BY h_Time DESC, Country, Model
"""

Q_GET_COSTS_BY_DATE_RANGE = """
    SELECT Costs_id, Model, Country, Costs_time, Costs
    FROM Costs
    WHERE Costs_time >= %s AND Costs_time <= %s
    ORDER BY Costs_time DESC, Model, Country
"""

Q_GET_SALES_PRICE_BY_DATE_RANGE = """
    SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
    FROM Sales_Price
    WHERE h_Time >= %s AND h_Time <= %s
    ORDER BY h_Time DESC, Model, Country
"""

# ==================== 批量导出相关查询 ====================
Q_GET_ALL_TABLES_INFO = """
    SELECT table_name, table_rows, create_time, update_time
    FROM information_schema.tables 
    WHERE table_schema = DATABASE()
    AND table_name IN ('History', 'Budget', 'Costs', 'Sales_Price', 'Exchange', 'Regional_Expenses')
"""

Q_GET_TABLE_COLUMNS = """
    SELECT column_name, data_type, column_comment
    FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = %s
    ORDER BY ordinal_position
"""

# ==================== 数据保存 (UPSERT) ====================
Q_UPSERT_HISTORY = """
    INSERT INTO History (h_Time, Country, Market, Model, Model_label, Series, 
                        Sales, Revenues, Gross_profits, Margin_profits, Net_income)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Market = VALUES(Market),
        Model_label = VALUES(Model_label),
        Series = VALUES(Series),
        Sales = VALUES(Sales),
        Revenues = VALUES(Revenues),
        Gross_profits = VALUES(Gross_profits),
        Margin_profits = VALUES(Margin_profits),
        Net_income = VALUES(Net_income)
"""

Q_UPSERT_BUDGET = """
    INSERT INTO Budget (h_Time, Country, Market, Model, Model_label, Series, 
                       Sales, Revenues, Gross_profits, Margin_profits, Net_income)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Market = VALUES(Market),
        Model_label = VALUES(Model_label),
        Series = VALUES(Series),
        Sales = VALUES(Sales),
        Revenues = VALUES(Revenues),
        Gross_profits = VALUES(Gross_profits),
        Margin_profits = VALUES(Margin_profits),
        Net_income = VALUES(Net_income)
"""

Q_UPSERT_SALES_PRICE = """
    INSERT INTO Sales_Price (id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Currency = VALUES(Currency),
        Sales = VALUES(Sales),
        Price = VALUES(Price),
        Exchange_time = VALUES(Exchange_time)
"""

Q_UPSERT_COSTS = """
    INSERT INTO Costs (Costs_id, Model, Country, Costs_time, Costs)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Costs = VALUES(Costs)
"""

Q_UPSERT_EXCHANGE = """
    INSERT INTO Exchange (Exchange_time, Exchange_rate)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
        Exchange_rate = VALUES(Exchange_rate)
"""

Q_UPSERT_REGIONAL_EXPENSES = """
    INSERT INTO Regional_Expenses (Country, Expenses_time,
                                   Marketing_expenses, Labor_cost,
                                   Other_variable_expenses, Other_fixed_expenses)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Marketing_expenses = VALUES(Marketing_expenses),
        Labor_cost = VALUES(Labor_cost),
        Other_variable_expenses = VALUES(Other_variable_expenses),
        Other_fixed_expenses = VALUES(Other_fixed_expenses)
"""

# ==================== 删除操作 ====================
Q_DELETE_HISTORY = """
    DELETE FROM History 
    WHERE h_Time = %s AND Country = %s AND Model = %s
"""

Q_DELETE_BUDGET = """
    DELETE FROM Budget 
    WHERE h_Time = %s AND Country = %s AND Model = %s
"""

Q_DELETE_SALES_PRICE = """
    DELETE FROM Sales_Price 
    WHERE id = %s
"""

Q_DELETE_COSTS = """
    DELETE FROM Costs 
    WHERE Costs_id = %s
"""

Q_DELETE_REGIONAL_EXPENSES = """
    DELETE FROM Regional_Expenses 
    WHERE Country = %s AND Expenses_time = %s
"""

Q_DELETE_EXCHANGE = """
    DELETE FROM Exchange 
    WHERE Exchange_time = %s
"""

# ==================== 汇率相关 ====================
Q_GET_EXCHANGE_RATES = """
    SELECT Exchange_time as h_Time, Exchange_rate 
    FROM Exchange
    ORDER BY Exchange_time DESC
"""

Q_GET_EXCHANGE_BY_DATE_RANGE = """
    SELECT Exchange_time, Exchange_rate 
    FROM Exchange
    WHERE Exchange_time >= %s AND Exchange_time <= %s
    ORDER BY Exchange_time DESC
"""

# ==================== 工具函数查询 ====================
Q_CLEAR_SYSTEM_LOGS = """
    DELETE FROM System_Log
    WHERE Log_Time < DATE_SUB(NOW(), INTERVAL %s DAY)
"""

Q_GET_DATABASE_SIZE = """
    SELECT 
        table_schema as database_name,
        ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    GROUP BY table_schema
"""

Q_GET_TABLE_ROW_COUNTS = """
    SELECT 
        table_name,
        table_rows
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    AND table_name IN ('History', 'Budget', 'Costs', 'Sales_Price', 'System_Log')
    ORDER BY table_name
"""

# 批量更新成本数据的查询
Q_UPSERT_COSTS_BATCH = """
    INSERT INTO Costs (Model, Country, Costs_time, Costs)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Costs = VALUES(Costs)
"""

# 获取成本数据（带筛选）
Q_GET_COSTS_WITH_FILTER = """
    SELECT Costs_id, Model, Country, Costs_time, Costs
    FROM Costs
    WHERE 1=1
    {model_filter}
    {country_filter}
    {time_filter}
    ORDER BY Costs_time DESC, Model, Country
"""

# 检查成本数据是否存在
Q_CHECK_COSTS_EXISTS = """
    SELECT COUNT(*) as count 
    FROM Costs 
    WHERE Model = %s AND Country = %s AND Costs_time = %s
"""