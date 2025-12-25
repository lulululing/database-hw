# app/utils/sql_queries.py

# 1. 基础业务数据查询
Q_GET_HISTORY = """
    SELECT h_Time as 时间, Country as 国家, Market as 市场, 
           Model as 型号, Model_label as 标签, Series as 系列,
           Sales as 销量, Revenues as 收入, 
           Gross_profits as 毛利, Margin_profits as 边际利润,
           Net_income as 净收入
    FROM History
    ORDER BY h_Time DESC, Country, Model
"""

Q_GET_BUDGET = """
    SELECT h_Time as 时间, Country as 国家, Market as 市场, 
           Model as 型号, Model_label as 标签, Series as 系列,
           Sales as 销量, Revenues as 收入, 
           Gross_profits as 毛利, Margin_profits as 边际利润,
           Net_income as 净收入
    FROM Budget
    ORDER BY h_Time DESC, Country, Model
"""

# 2. 参数表查询 (用于 Python 自动计算)
Q_GET_ALL_EXCHANGE = "SELECT Exchange_time, Exchange_rate FROM Exchange"
Q_GET_ALL_COSTS = "SELECT Model, Country, Costs_time, Costs FROM Costs"
Q_GET_ALL_PRICES = "SELECT Model, Country, h_Time, Price, Currency FROM Sales_Price"
Q_GET_ALL_RATIO1 = "SELECT Series, Software_product_amortization_rate_acc_cost, RandD_rate_acc_cost FROM Ratio_Expenses1"
Q_GET_ALL_RATIO2 = "SELECT Ratio_expenses2_id, Country, Functional_cost_allocation_rate_acc_cost, Business_group_headquarters_allocation_rate_acc_cost, Marketing_activities_provision_rate_acc_revenue FROM Ratio_Expenses2"
Q_GET_ALL_RATIO3 = "SELECT Model_label, Country, After_sales_provision_rate_acc_cost FROM Ratio_Expenses3"
Q_GET_ALL_REGIONAL = "SELECT Country, Expenses_time, Marketing_expenses, Labor_cost, Other_variable_expenses, Other_fixed_expenses FROM Regional_Expenses"
Q_GET_MODELS_INFO = "SELECT Model, Series, Model_label FROM Model"

# 3. 覆盖更新语句 (UPSERT)
# 只要 h_Time, Country, Model 相同，就直接覆盖旧数据
Q_UPSERT_HISTORY = """
    INSERT INTO History (
        h_Time, Country, Market, Model, Model_label, Series, 
        Sales, Revenues, Gross_profits, Margin_profits, Net_income
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Sales = VALUES(Sales),
        Revenues = VALUES(Revenues),
        Gross_profits = VALUES(Gross_profits),
        Margin_profits = VALUES(Margin_profits),
        Net_income = VALUES(Net_income)
"""

Q_UPSERT_BUDGET = """
    INSERT INTO Budget (
        h_Time, Country, Market, Model, Model_label, Series, 
        Sales, Revenues, Gross_profits, Margin_profits, Net_income
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Sales = VALUES(Sales),
        Revenues = VALUES(Revenues),
        Gross_profits = VALUES(Gross_profits),
        Margin_profits = VALUES(Margin_profits),
        Net_income = VALUES(Net_income)
"""

# 4. 视图查询 (用于 Display 页面)
Q_GET_VIEW_DATA = "SELECT * FROM {view_name}"

# 5. 其他辅助
Q_GET_ALL_MODELS = "SELECT DISTINCT Model FROM Model ORDER BY Model"
Q_LOG_ACTION = "INSERT INTO System_Log (Username, Role, Action_Type, Details, Log_Time) VALUES (%s, %s, %s, %s, NOW())"

Q_UPSERT_SALES_PRICE = """
    INSERT INTO Sales_Price (id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Sales = VALUES(Sales),
        Price = VALUES(Price),
        Currency = VALUES(Currency)
"""

# 新增：查询系统日志
Q_GET_SYSTEM_LOGS = """
    SELECT Log_ID, Username, Role, Action_Type, Details, Log_Time 
    FROM System_Log 
    ORDER BY Log_Time DESC
    LIMIT 1000
"""