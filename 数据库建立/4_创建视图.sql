-- 第4步：创建所有视图
-- 在 Navicat 中：右键数据库 → 运行 SQL 文件 → 选择本文件
-- 前提：已成功执行 1_创建表和索引.sql、2_插入数据.sql、3_创建触发器.sql

-- 基础视图：价格、收入、费用、利润
CREATE VIEW true_Price(id, true_Price) AS
   SELECT Sales_Price.id, 
       CASE WHEN Sales_Price.Currency = 'USD' THEN Sales_Price.Price*Exchange.Exchange_rate
             ELSE Sales_Price.Price
       END AS true_Price
   FROM Sales_Price, Exchange
   WHERE Sales_Price.Exchange_time = Exchange.Exchange_time;

CREATE VIEW true_Revenues(id, Revenues, Costs, Gross_profits) AS
SELECT Sales_Price.id, ROUND(Sales_Price.Sales*true_Price.true_Price,2) AS Revenues, Round(Sales_Price.Sales*Costs.Costs, 2) AS Costs, ROUND(Sales_Price.Sales*true_Price.true_Price - Sales_Price.Sales*Costs.Costs,2) AS Gross_profits
FROM Sales_Price, Costs, true_Price
WHERE Sales_Price.Model = Costs.Model AND Sales_Price.Country = Costs.Country AND Sales_Price.h_Time = Costs.Costs_time AND Sales_Price.id = true_Price.id;

CREATE VIEW true_Expenses(id, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_cost, Other_variable_expenses, Other_fixed_expenses, Functional_expenses, Headquarters_expenses) AS
    SELECT Sales_Price.id,
ROUND(true_Revenues.Costs*(Ratio_Expenses1.Software_product_amortization_rate_acc_cost+RandD_rate_acc_cost),2) AS RandD_expenses,
ROUND(true_Revenues.Costs*Ratio_Expenses3.After_sales_provision_rate_acc_cost,2) AS After_sales_provision,
ROUND(true_Revenues.Revenues*Ratio_Expenses2.Marketing_activities_provision_rate_acc_revenue,2) AS Marketing_provision,
Regional_Expenses.Marketing_expenses,
Regional_Expenses.Labor_cost,
Regional_Expenses.Other_variable_expenses,
Regional_Expenses.Other_fixed_expenses,
ROUND(true_Revenues.Costs*Ratio_Expenses2.Functional_cost_allocation_rate_acc_cost,2) AS Functional_expenses,
ROUND(true_Revenues.Costs*Ratio_Expenses2.Business_group_headquarters_allocation_rate_acc_cost,2) AS Headquarters_expenses
FROM Sales_Price, true_Revenues, Ratio_Expenses1, Ratio_Expenses2, Ratio_Expenses3, Regional_Expenses, Model
WHERE Sales_Price.id = true_Revenues.id AND Sales_Price.Model = Model.Model AND Ratio_Expenses1.Series = Model.Series AND Ratio_Expenses2.Country = Sales_Price.Country AND Regional_Expenses.Country = Sales_Price.Country AND Ratio_Expenses3.Model_label = Model.Model_label AND Ratio_Expenses3.Country = Sales_Price.Country AND Regional_Expenses.Expenses_time = Sales_Price.h_time;

CREATE VIEW true_Margin_profits(id, Margin_profits) AS
SELECT 
    Sales_Price.id, 
    ROUND(
        true_Revenues.Gross_profits 
        - true_Expenses.RandD_expenses 
        - true_Expenses.After_sales_provision 
        - true_Expenses.Marketing_provision 
        - true_Expenses.Marketing_expenses 
        - true_Expenses.Labor_cost 
        - true_Expenses.Other_variable_expenses, 
    2) AS Margin_profits
FROM Sales_Price, true_Revenues, true_Expenses
WHERE Sales_Price.id = true_Revenues.id 
  AND Sales_Price.id = true_Expenses.id;

CREATE VIEW true_Net_income(id, Net_income) AS
SELECT Sales_Price.id, ROUND(true_Margin_profits.Margin_profits - true_Expenses.Other_fixed_expenses - true_Expenses.Functional_expenses - true_Expenses.Headquarters_expenses,2) AS Net_income
FROM Sales_Price, true_Margin_profits, true_Expenses
WHERE Sales_Price.id = true_Margin_profits.id AND Sales_Price.id = true_Expenses.id;

-- 综合展示视图
CREATE VIEW Display(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income, Exchange_time) AS
SELECT Sales_Price.id, Sales_Price.h_Time, Sales_Price.Model, Model.Model_label, Model.Series, Sales_Price.Country, Country.Market, Sales_Price.Sales, Sales_Price.Price, true_Revenues.Revenues, ROUND(true_Revenues.Costs/Sales_Price.Sales,2) AS pre_Costs, true_Revenues.Costs, true_Revenues.Gross_profits, ROUND(true_Revenues.Gross_profits/true_Revenues.Revenues,2) AS Gross_profits_ratio, true_Expenses.RandD_expenses, true_Expenses.After_sales_provision, true_Expenses.Marketing_provision, true_Expenses.Marketing_expenses, true_Expenses.Labor_cost, true_Expenses.Other_variable_expenses, true_Margin_profits.Margin_profits, true_Expenses.Other_fixed_expenses, true_Expenses.Functional_expenses, true_Expenses.Headquarters_expenses, true_Net_income.Net_income, Sales_Price.Exchange_time
FROM Sales_Price, Model, Country, true_Revenues, true_Expenses, true_Margin_profits, true_Net_income
WHERE Sales_Price.Model = Model.Model AND Sales_Price.Country = Country.Country AND Sales_Price.id = true_Expenses.id AND Sales_Price.id = true_Margin_profits.id AND Sales_Price.id = true_Net_income.id AND Sales_Price.id = true_Revenues.id
ORDER BY Country, Model, h_Time;

-- 各国销售价格视图（业务员权限用）
CREATE VIEW Sales_Price_India(id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time) AS
SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
FROM Sales_Price
WHERE Country = 'India';

CREATE VIEW Sales_Price_Pakistan(id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time) AS
SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
FROM Sales_Price
WHERE Country = 'Pakistan';

CREATE VIEW Sales_Price_South_Africa(id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time) AS
SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
FROM Sales_Price
WHERE Country = 'South Africa';

CREATE VIEW Sales_Price_Kenya(id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time) AS
SELECT id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time
FROM Sales_Price
WHERE Country = 'Kenya';

-- 各国展示视图（业务员权限用）
CREATE VIEW DisplayIndia(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income) AS
SELECT id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income
FROM Display
WHERE Country = 'India'
ORDER BY Country, Model, h_Time;

CREATE VIEW DisplayPakistan(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income) AS
SELECT id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income
FROM Display
WHERE Country = 'Pakistan'
ORDER BY Country, Model, h_Time;

CREATE VIEW DisplaySouthAfrica(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income) AS
SELECT id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income
FROM Display
WHERE Country = 'South Africa'
ORDER BY Country, Model, h_Time;

CREATE VIEW DisplayKenya(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income) AS
SELECT id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income
FROM Display
WHERE Country = 'Kenya'
ORDER BY Country, Model, h_Time;

-- 经理聚合视图（历史、预测、预算对比）
CREATE VIEW s_Display(
    h_Time, Country, Market, Model, Model_label, Series, 
    Sales_history, Sales_forecasting, Sales_budget, 
    Revenues_history, Revenues_forecasting, Revenues_budget, 
    Gross_profits_history, Gross_profits_forecasting, Gross_profits_budget, 
    Margin_profits_history, Margin_profits_forecasting, Margin_profits_budget, 
    Net_income_history, Net_income_forecasting, Net_income_budget
) AS
SELECT 
    Display.h_Time, 
    Display.Country, 
    Display.Market,
    Display.Model, 
    Display.Model_label,
    Display.Series,
    COALESCE(History.Sales, 0) AS Sales_history,
    COALESCE(Display.Sales, 0) AS Sales_forecasting,
    COALESCE(Budget.Sales, 0) AS Sales_budget,
    COALESCE(History.Revenues, 0) AS Revenues_history,
    COALESCE(Display.Revenues, 0) AS Revenues_forecasting,
    COALESCE(Budget.Revenues, 0) AS Revenues_budget,  
    COALESCE(History.Gross_profits, 0) AS Gross_profits_history,
    COALESCE(Display.Gross_profits, 0) AS Gross_profits_forecasting,
    COALESCE(Budget.Gross_profits, 0) AS Gross_profits_budget,
    COALESCE(History.Margin_profits, 0) AS Margin_profits_history,
    COALESCE(Display.Margin_profits, 0) AS Margin_profits_forecasting,
    COALESCE(Budget.Margin_profits, 0) AS Margin_profits_budget,
    COALESCE(History.Net_income, 0) AS Net_income_history,
    COALESCE(Display.Net_income, 0) AS Net_income_forecasting,
    COALESCE(Budget.Net_income, 0) AS Net_income_budget
FROM Display
LEFT JOIN History ON 
    Display.h_Time = History.h_Time 
    AND Display.Country = History.Country 
    AND Display.Model = History.Model
LEFT JOIN Budget ON 
    Display.h_Time = Budget.h_Time 
    AND Display.Country = Budget.Country 
    AND Display.Model = Budget.Model
ORDER BY Display.Model, Display.h_Time;

CREATE VIEW s_Display_Model(
    h_Time, Model, Model_label, Series, 
    Sales_history, Sales_forecasting, Sales_budget, 
    Revenues_history, Revenues_forecasting, Revenues_budget, 
    Gross_profits_history, Gross_profits_forecasting, Gross_profits_budget, 
    Margin_profits_history, Margin_profits_forecasting, Margin_profits_budget, 
    Net_income_history, Net_income_forecasting, Net_income_budget
) AS
SELECT h_Time, Model, Model_label, Series, 
SUM(Sales_history), SUM(Sales_forecasting), SUM(Sales_budget), SUM(Revenues_history), SUM(Revenues_forecasting), SUM(Revenues_budget), SUM(Gross_profits_history), SUM(Gross_profits_forecasting), SUM(Gross_profits_budget), SUM(Margin_profits_history), SUM(Margin_profits_forecasting), SUM(Margin_profits_budget), SUM(Net_income_history), SUM(Net_income_forecasting), SUM(Net_income_budget)
FROM s_Display
GROUP BY h_Time, Model, Model_label, Series;

CREATE VIEW s_Display_Country(
    h_Time, Country, Market, Sales_history, Sales_forecasting, Sales_budget, 
    Revenues_history, Revenues_forecasting, Revenues_budget, 
    Gross_profits_history, Gross_profits_forecasting, Gross_profits_budget, 
    Margin_profits_history, Margin_profits_forecasting, Margin_profits_budget, 
    Net_income_history, Net_income_forecasting, Net_income_budget
) AS
SELECT h_Time, Country, Market, 
SUM(Sales_history), SUM(Sales_forecasting), SUM(Sales_budget), SUM(Revenues_history), SUM(Revenues_forecasting), SUM(Revenues_budget), SUM(Gross_profits_history), SUM(Gross_profits_forecasting), SUM(Gross_profits_budget), SUM(Margin_profits_history), SUM(Margin_profits_forecasting), SUM(Margin_profits_budget), SUM(Net_income_history), SUM(Net_income_forecasting), SUM(Net_income_budget)
FROM s_Display
GROUP BY h_Time, Country, Market;
