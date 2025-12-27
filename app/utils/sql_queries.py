# app/utils/sql_queries.py
"""
SQL查询语句集中管理
"""

# ==================== 系统日志 ====================
Q_LOG_ACTION = """
    INSERT INTO System_Log (Username, Role, Action_Type, Details)
    VALUES (%s, %s, %s, %s)
"""

Q_GET_SYSTEM_LOGS = """
    SELECT Log_ID, Log_Time, Username, Role, Action_Type, Details
    FROM System_Log
    ORDER BY Log_Time DESC
    LIMIT 1000
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
"""

Q_GET_ALL_COSTS = """
    SELECT Costs_id, Model, Country, Costs_time, Costs 
    FROM Costs
"""

Q_GET_ALL_PRICES = """
    SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
    FROM Sales_Price
"""

Q_GET_ALL_RATIO1 = """
    SELECT Series, 
           Software_product_amortization_rate_acc_cost,
           RandD_rate_acc_cost
    FROM Ratio_Expenses1
"""

Q_GET_ALL_RATIO2 = """
    SELECT Country,
           Functional_cost_allocation_rate_acc_cost,
           Business_group_headquarters_allocation_rate_acc_cost,
           Marketing_activities_provision_rate_acc_revenue
    FROM Ratio_Expenses2
"""

Q_GET_ALL_RATIO3 = """
    SELECT Ratio_expenses3_id, Model_label, Country,
           After_sales_provision_rate_acc_cost
    FROM Ratio_Expenses3
"""

Q_GET_ALL_REGIONAL = """
    SELECT Country, Expenses_time,
           Marketing_expenses, Labor_cost,
           Other_variable_expenses, Other_fixed_expenses
    FROM Regional_Expenses
"""

Q_GET_MODELS_INFO = """
    SELECT Model, Series, Model_label
    FROM Model
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