-- 第1步：创建所有表和索引（不含触发器）
-- 在 Navicat 中：右键数据库 → 运行 SQL 文件 → 选择本文件

CREATE TABLE Country(
    Country VARCHAR(50) PRIMARY KEY,
    Market VARCHAR(50),
    CHECK (Market IN ('Asia', 'Africa', 'South America')));

CREATE TABLE Ratio_Expenses1(
Series VARCHAR(50) PRIMARY KEY,
Software_product_amortization_rate_acc_cost DECIMAL(5,4),
RandD_rate_acc_cost DECIMAL(5,4),
CHECK (Series IN ('Dog', 'Cat', 'Tiger')));

CREATE TABLE Model(
Model VARCHAR(50) PRIMARY KEY,
Series VARCHAR(50),
Model_label VARCHAR(50),
FOREIGN KEY (Series) REFERENCES Ratio_Expenses1(Series));

CREATE TABLE Exchange(
Exchange_time VARCHAR(50) PRIMARY KEY,
Exchange_rate DECIMAL(3,2) NOT NULL,
CHECK (Exchange_time IN ('2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09')));

CREATE TABLE Sales_Price(
id INTEGER PRIMARY KEY,
Model VARCHAR(50),
Country VARCHAR(50),
h_Time VARCHAR(50),
Currency VARCHAR(50),
Sales INTEGER,
Price DECIMAL(10,2),
Exchange_time VARCHAR(50),
CHECK (h_time In ('2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09')),
CHECK (Currency IN ('CHY', 'USD')),
CHECK (Exchange_time = h_Time),
UNIQUE(Model, Country, h_Time),
FOREIGN KEY (Model) REFERENCES Model(Model),
FOREIGN KEY (Country) REFERENCES Country(Country),
FOREIGN KEY (Exchange_time) REFERENCES Exchange(Exchange_time));

CREATE TABLE Costs(
Costs_id INTEGER PRIMARY KEY,
Model VARCHAR(50),
Country VARCHAR(50),
Costs_time VARCHAR(50),
Costs DECIMAL(10,2),
CHECK (Costs_time IN ('2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09')),
UNIQUE(Model, Country, Costs_time),
FOREIGN KEY (Model) REFERENCES Model(Model),
FOREIGN KEY (Country) REFERENCES Country(Country));

CREATE TABLE Ratio_Expenses2(
Ratio_expenses2_id INTEGER PRIMARY KEY,
Country VARCHAR(50),
Functional_cost_allocation_rate_acc_cost DECIMAL(5,4),
Business_group_headquarters_allocation_rate_acc_cost DECIMAL(5,4),
Marketing_activities_provision_rate_acc_revenue DECIMAL(5,4),
FOREIGN KEY (Country) REFERENCES Country(Country),
UNIQUE(Country));

CREATE TABLE Ratio_Expenses3(
Ratio_expenses3_id INTEGER PRIMARY KEY,
Model_label VARCHAR(50),
Country VARCHAR(50),
After_sales_provision_rate_acc_cost DECIMAL(5,4),
FOREIGN KEY (Country) REFERENCES Country(Country));

CREATE TABLE Regional_Expenses(
Country VARCHAR(50),
Expenses_time VARCHAR(50),
Marketing_expenses DECIMAL(10,2),
Labor_cost DECIMAL(10,2),
Other_variable_expenses DECIMAL(10,2),
Other_fixed_expenses DECIMAL(10,2),
UNIQUE(Country, Expenses_time),
FOREIGN KEY (Country) REFERENCES Country(Country));

CREATE TABLE History(
h_Time VARCHAR(50),
Country VARCHAR(50),
Market VARCHAR(50),
Model VARCHAR(50),
Model_label VARCHAR(50),
Series VARCHAR(50),
Sales INTEGER,
Revenues DECIMAL(20,2),
Gross_profits DECIMAL(20,2),
Margin_profits DECIMAL(20,2),
Net_income DECIMAL(20,2));

CREATE TABLE Budget(
h_Time VARCHAR(50),
Country VARCHAR(50),
Market VARCHAR(50),
Model VARCHAR(50),
Model_label VARCHAR(50),
Series VARCHAR(50),
Sales INTEGER,
Revenues DECIMAL(20,2),
Gross_profits DECIMAL(20,2),
Margin_profits DECIMAL(20,2),
Net_income DECIMAL(20,2));

-- 索引结构
CREATE INDEX idx_sales_price_composite ON Sales_Price(Model, Country, h_Time);
CREATE INDEX idx_sales_price_time ON Sales_Price(h_Time);
CREATE INDEX idx_costs_composite ON Costs(Model, Country, Costs_time);
CREATE INDEX idx_model_series ON Model(Series);
CREATE INDEX idx_regional_expenses ON Regional_Expenses(Country, Expenses_time);
