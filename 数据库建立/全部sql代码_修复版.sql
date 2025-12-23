-- 创建关系
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

DELIMITER $$

CREATE TRIGGER validate_model_label_insert
BEFORE INSERT ON Ratio_Expenses3
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Model WHERE Model_label = NEW.Model_label) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Model_label does not exist in Model table';
    END IF;
END
$$

CREATE TRIGGER validate_model_label_update
BEFORE UPDATE ON Ratio_Expenses3
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Model WHERE Model_label = NEW.Model_label) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Model_label does not exist in Model table';
    END IF;
END$$

DELIMITER ;

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

-- 索引结构：
CREATE INDEX idx_sales_price_composite ON Sales_Price(Model, Country, h_Time);
CREATE INDEX idx_sales_price_time ON Sales_Price(h_Time);
CREATE INDEX idx_sales_price_currency ON Sales_Price(Currency);
CREATE INDEX idx_sales_price_exchange_time ON Sales_Price(Exchange_time);
CREATE INDEX idx_costs_composite ON Costs(Model, Country, Costs_time);
CREATE INDEX idx_ratio_expenses3_composite ON Ratio_Expenses3(Model_label, Country);
CREATE INDEX idx_regional_expenses_composite ON Regional_Expenses(Country, Expenses_time);
CREATE INDEX idx_model_series ON Model(Series);
CREATE INDEX idx_model_label ON Model(Model_label);
CREATE INDEX idx_model_composite ON Model(Model, Series, Model_label);
CREATE INDEX idx_ratio_expenses2_country_covers ON Ratio_Expenses2(Country, 
    Functional_cost_allocation_rate_acc_cost, 
    Business_group_headquarters_allocation_rate_acc_cost, 
Marketing_activities_provision_rate_acc_revenue);
CREATE INDEX idx_country_market ON Country(Market);
CREATE INDEX idx_true_revenues_join ON Sales_Price(Model, Country, id, h_Time, Sales);
CREATE INDEX idx_history_main ON History(h_Time, Country, Model, Market, Model_label, Series);
CREATE INDEX idx_history_columns ON History(h_Time, Country, Model, Sales, Revenues, Gross_profits, Margin_profits, Net_income);
CREATE INDEX idx_budget_main ON Budget(h_Time, Country, Model, Market, Model_label, Series);
CREATE INDEX idx_budget_columns ON Budget(h_Time, Country, Model, Sales, Revenues, Gross_profits, Margin_profits, Net_income);

-- 试验数据：
INSERT INTO Country(Country, Market)
VALUES
    ('India', 'Asia'),
	('Pakistan', 'Asia'),
	('South Africa', 'Africa'),
	('Kenya', 'Africa'),
	('Mexico', 'South America'),
	('Peru', 'South America');

INSERT INTO Ratio_Expenses1 (Series, Software_product_amortization_rate_acc_cost, RandD_rate_acc_cost)
VALUES
    ('Dog', 0.0450, 0.0300),
	('Cat', 0.0150, 0.0250),
	('Tiger', 0.0350, 0.0200);

INSERT INTO Model(Model, Series, Model_label)
VALUES
    ('DA 128+8', 'Dog', 'DA'),
	('DA 256+8', 'Dog', 'DA'),
	('DB 128+8', 'Dog', 'DB'),
	('DB 256+8', 'Dog', 'DB'),
	('CA 128+8', 'Cat', 'CA'),
	('CA 256+8', 'Cat', 'CA'),
	('CB 128+8', 'Cat', 'CB'),
	('CB 256+8', 'Cat', 'CB'),
	('TA 128+8', 'Tiger', 'TA'),
	('TA 256+8', 'Tiger', 'TA'),
	('TB 128+8', 'Tiger', 'TB'),
	('TB 256+8', 'Tiger', 'TB');

INSERT INTO Exchange(Exchange_time, Exchange_rate)
VALUES
    ('2025-10', 7.15),
	('2025-11', 7.20),
	('2025-12', 7.19),
	('2026-01', 7.16),
	('2026-02', 7.17),
	('2026-03', 7.18),
	('2026-04', 7.19),
	('2026-05', 7.20),
	('2026-06', 7.17),
	('2026-07', 7.18),
	('2026-08', 7.20),
	('2026-09', 7.21);

INSERT INTO sales_price(id, Model, Country, h_Time, Currency, Sales, Price, Exchange_time)
VALUES
	(1, 'DA 128+8', 'India', '2025-12', 'CHY', 20, 101.00, '2025-12'),
	(2, 'DA 128+8', 'Pakistan', '2026-01', 'CHY', 35, 102.00,'2026-01'),
	(3, 'DA 256+8', 'Pakistan', '2025-12', 'CHY', 15, 110.00,'2025-12'),
	(4, 'DA 256+8', 'South Africa', '2026-01', 'USD', 30, 17.20,'2026-01'),
	(5, 'DB 128+8', 'India', '2025-12', 'CHY', 30, 105.00,'2025-12'),
	(6, 'DB 128+8', 'India', '2026-01', 'CHY', 37, 106.00,'2026-01'),
	(7, 'DB 256+8', 'South Africa', '2025-12', 'USD', 40, 17.50,'2025-12'),
	(8, 'DB 256+8', 'Kenya', '2026-01', 'CHY', 40, 100.00,'2026-01'),
	(9, 'CA 128+8', 'Kenya', '2025-12', 'CHY', 41, 100.00,'2025-12'),
	(10, 'CA 128+8', 'Pakistan', '2026-01', 'CHY', 37, 108.00,'2026-01'),
	(11, 'CA 256+8', 'Pakistan', '2025-12', 'CHY', 38, 109.00,'2025-12'),
	(12, 'CA 256+8', 'Pakistan', '2026-01', 'CHY', 39, 105.00,'2026-01'),
	(13, 'CB 128+8', 'India', '2025-12', 'CHY', 20, 99.00,'2025-12'),
	(14, 'CB 128+8', 'Kenya', '2026-01', 'CHY', 25, 103.50,'2026-01'),
	(15, 'CB 256+8', 'Kenya', '2025-12', 'CHY', 30, 103.50,'2025-12'),
	(16, 'CB 256+8', 'South Africa', '2026-01', 'USD', 44, 15.50,'2026-01'),
	(17, 'TA 128+8', 'India', '2025-12', 'CHY', 30, 106.00,'2025-12'),
	(18, 'TA 128+8', 'Kenya', '2026-01', 'CHY', 34, 104.00,'2026-01'),
	(19, 'TA 256+8', 'South Africa', '2025-12', 'USD', 34, 17.00,'2025-12'),
	(20, 'TA 256+8', 'South Africa', '2026-01', 'USD', 35, 16.50,'2026-01');



INSERT INTO Costs(Costs_id, Model, Country, Costs_time, Costs)
VALUES
    (1, 'DA 128+8', 'India', '2025-12', 75.00),
	(2, 'DA 128+8', 'Pakistan', '2026-01', 76.00 ),
	(3, 'DA 256+8', 'Pakistan', '2025-12', 74.00 ),
	(4, 'DA 256+8', 'South Africa', '2026-01',77.00),
	(5, 'DB 128+8', 'India', '2025-12', 80.00),
	(6, 'DB 128+8', 'India', '2026-01', 72.00),
	(7, 'DB 256+8', 'South Africa', '2025-12', 75.00),
	(8, 'DB 256+8', 'Kenya', '2026-01', 76.00),
	(9, 'CA 128+8', 'Kenya', '2025-12', 60.00),
	(10, 'CA 128+8', 'Pakistan', '2026-01', 61.00),
	(11, 'CA 256+8', 'Pakistan', '2025-12', 62.00),
	(12, 'CA 256+8', 'Pakistan', '2026-01', 63.00),
	(13, 'CB 128+8', 'India', '2025-12', 66.00),
	(14, 'CB 128+8', 'Kenya', '2026-01', 67.00),
	(15, 'CB 256+8', 'Kenya', '2025-12', 68.00),
	(16, 'CB 256+8', 'South Africa', '2026-01', 66.00),
	(17, 'TA 128+8', 'India', '2025-12', 81.00),
	(18, 'TA 128+8', 'Kenya', '2026-01', 85.00),
	(19, 'TA 256+8', 'South Africa', '2025-12', 85.00),
	(20, 'TA 256+8', 'South Africa', '2026-01', 83.00),
	(21, 'TB 128+8', 'Pakistan', '2025-12', 87.00),
	(22, 'TB 128+8', 'Pakistan', '2026-01', 85.00),
(23, 'TB 256+8', 'India', '2025-12', 75.00),
(24, 'TB 256+8', 'Pakistan', '2026-01', 76.00);

INSERT INTO Ratio_Expenses2(Ratio_expenses2_id, Country, Functional_cost_allocation_rate_acc_cost, Business_group_headquarters_allocation_rate_acc_cost, Marketing_activities_provision_rate_acc_revenue)
VALUES
    (1, 'Kenya', 0.0250, 0.0350,0.0500),
	(2, 'South Africa', 0.0300, 0.0300, 0.0500),
	(3, 'India', 0.0150, 0.0250, 0.0300),
	(4, 'Mexico', 0.0200, 0.0350, 0.0400),
	(5, 'Peru', 0.0250, 0.0350, 0.0450),
	(6, 'Pakistan', 0.0300, 0.0350, 0.0250);

INSERT INTO Ratio_Expenses3(Ratio_expenses3_id, Model_label, Country, After_sales_provision_rate_acc_cost)
VALUES
    (1, 'DA', 'India', 0.0250),
	(2, 'DA', 'Pakistan', 0.0260),
	(3, 'DA', 'Kenya', 0.0240),
	(4, 'DA', 'South Africa', 0.0250),
	(5, 'DA', 'Mexico', 0.0240),
	(6, 'DA', 'Peru', 0.0210),
	(7, 'DB', 'India', 0.0300),
	(8, 'DB', 'Pakistan', 0.0310),
	(9, 'DB', 'Kenya', 0.0290),
	(10, 'DB', 'South Africa', 0.0250),
	(11, 'DB', 'Mexico', 0.0300),
	(12, 'DB', 'Peru', 0.0270),
	(13, 'CA', 'India', 0.0260),
	(14, 'CA', 'Pakistan', 0.0310),
	(15, 'CA', 'Kenya', 0.0290),
	(16, 'CA', 'South Africa', 0.0190),
	(17, 'CA', 'Mexico', 0.0280),
	(18, 'CA', 'Peru', 0.0270),
	(19, 'CB', 'India', 0.0260),
	(20, 'CB', 'Pakistan', 0.0190),
	(21, 'CB', 'Kenya', 0.0390),
	(22, 'CB', 'South Africa', 0.0270),
	(23, 'CB', 'Mexico', 0.0280),
	(24, 'CB', 'Peru', 0.0230),
	(25, 'TA', 'India', 0.0270),
	(26, 'TA', 'Pakistan', 0.0190),
	(27, 'TA', 'Kenya', 0.0280),
	(28, 'TA', 'South Africa', 0.0250),
	(29, 'TA', 'Mexico', 0.0250),
	(30, 'TA', 'Peru', 0.0230),
	(31, 'TB', 'India', 0.0240),
	(32, 'TB', 'Pakistan', 0.0220),
	(33, 'TB', 'Kenya', 0.0270),
	(34, 'TB', 'South Africa', 0.0280),
	(35, 'TB', 'Mexico', 0.0240),
	(36, 'TB', 'Peru', 0.0240);

INSERT INTO Regional_Expenses(Country, Expenses_time, Marketing_expenses, Labor_cost, Other_variable_expenses, Other_fixed_expenses)
VALUES
    ('India', '2025-12', 25.00, 30.00, 25.00, 30.00),
	('India', '2026-01', 26.00, 27.00, 28.00, 29.00),
	('India', '2026-02', 27.00, 25.00, 26.00, 30.00),
	('India', '2026-03', 28.00, 26.00, 27.00, 31.00),
	('India', '2026-04', 24.00, 23.00, 29.00, 31.00),
	('India', '2026-05', 25.00, 26.00, 27.00, 30.00),
	('Pakistan', '2025-12', 27.00, 26.00, 25.00, 24.00),
	('Pakistan', '2026-01', 28.00, 26.00, 28.00, 29.00),
	('Pakistan', '2026-02', 25.00, 25.00, 27.00, 29.00),
	('Pakistan', '2026-03', 27.00, 25.00, 26.00, 30.00),
	('Pakistan', '2026-04', 25.00, 22.00, 26.00, 29.00),
	('Pakistan', '2026-05', 25.00, 27.00, 27.00, 30.00),
	('South Africa', '2025-12', 28.00, 27.00, 24.00, 25.00),
	('South Africa', '2026-01', 29.00, 24.00, 26.00, 27.00),
	('South Africa', '2026-02', 26.00, 27.00, 23.00, 28.00),
	('South Africa', '2026-03', 24.00, 30.00, 26.00, 30.00),
	('South Africa', '2026-04', 26.00, 21.00, 21.00, 29.00),
	('South Africa', '2026-05', 23.00, 30.00, 27.00, 30.00),
	('Kenya', '2025-12', 26.00, 28.00, 29.00, 25.00),
	('Kenya', '2026-01', 23.00, 24.00, 25.00, 28.00),
	('Kenya', '2026-02', 26.00, 28.00, 28.00, 24.00),
	('Kenya', '2026-03', 26.00, 26.00, 27.00, 29.00),
	('Kenya', '2026-04', 27.00, 28.00, 21.00, 29.00),
	('Kenya', '2026-05', 26.00, 24.00, 27.00, 28.00),
	('Mexico', '2025-12', 27.00, 23.00, 31.00, 22.00),
	('Mexico', '2026-01', 25.00, 29.00, 22.00, 24.00),
	('Mexico', '2026-02', 23.00, 30.00, 22.00, 24.00),
	('Mexico', '2026-03', 25.00, 25.00, 25.00, 25.00),
	('Mexico', '2026-04', 26.00, 27.00, 29.00, 22.00),
	('Mexico', '2026-05', 24.00, 26.00, 24.00, 26.00),
	('Peru', '2025-12', 25.00, 26.00, 27.00, 26.00),
	('Peru', '2026-01', 24.00, 28.00, 21.00, 21.00),
	('Peru', '2026-02', 27.00, 26.00, 21.00, 26.00),
	('Peru', '2026-03', 24.00, 26.00, 28.00, 29.00),
	('Peru', '2026-04', 22.00, 25.00, 27.00, 21.00),
	('Peru', '2026-05', 26.00, 28.00, 23.00, 29.00);

INSERT INTO History(h_Time, Country, Market, Model, Model_label, Series, Sales, Revenues, Gross_profits, Margin_profits, Net_income)
VALUES 
('2025-10', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 36, 3600.00, 3000.00, 1000.00, 600.00),
('2025-10', 'India', 'Asia', 'CA 128+8', 'CA', 'Cat', 35, 3600.00, 2876.00, 879.86, 589.96),
('2025-10', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 29, 3000.00, 1600.00, 875.35, 325.78),
('2025-10', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 34, 3700.00, 3010.00, 866.66, 788.44),
('2025-11', 'Pakistan', 'Asia', 'TA 128+8', 'TA', 'Tiger', 38, 3700.00, 3020.00, 800.00, 710.00),
('2025-11', 'India', 'Asia', 'TA 256+8', 'TA', 'Tiger', 29, 2900.00, 2500.00, 750.76, 590.00),
('2025-11', 'South Africa', 'Africa', 'TB 128+8', 'TB', 'Tiger', 40, 4200.00, 3200.00, 976.38, 755.98),
('2025-11', 'Kenya', 'Africa', 'DA 128+8', 'DA', 'Dog', 35, 3400.00, 2900.00, 799.34, 601.23);

INSERT INTO Budget(h_Time, Country, Market, Model, Model_label, Series, Sales, Revenues, Gross_profits, Margin_profits, Net_income)
VALUES
('2025-10', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 35, 3400.00, 2956.00, 1200.00, 605.00),
('2025-10', 'India', 'Asia', 'CA 128+8', 'CA', 'Cat', 32, 3200.00, 2500.00, 800.00, 540.35),
('2025-10', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 30, 3000.00, 2700.00, 899.26, 376.38),
('2025-10', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 29, 3500.00, 2900.00, 1000.00, 705.21),
('2025-11', 'Pakistan', 'Asia', 'TA 128+8', 'TA', 'Tiger', 35, 3700.00, 2903.00, 784.04, 623.00),
('2025-11', 'India', 'Asia', 'TA 256+8', 'TA', 'Tiger', 35, 3400.00, 2500.00, 750.76, 590.00),
('2025-11', 'South Africa', 'Africa', 'TB 128+8', 'TB', 'Tiger', 40, 4000.00, 3200.00, 976.38, 755.98),
('2025-11', 'Kenya', 'Africa', 'DA 128+8', 'DA', 'Dog', 33, 3500.00, 2900.00, 799.34, 601.23),
('2025-12', 'India', 'Asia', 'DA 128+8', 'DA', 'Dog', 34, 3300.00, 2500.00, 766.53, 599.08),
('2026-01', 'Pakistan', 'Asia', 'DA 128+8', 'DA', 'Dog', 33, 3100.00, 3010.00, 876.54, 622.35),
('2025-12', 'Pakistan', 'Asia', 'DA 256+8', 'DA', 'Dog', 20, 2000.00, 1550.00, 621.22, 376.21),
('2026-01', 'South Africa', 'Africa', 'DA 256+8', 'DA', 'Dog', 35, 3200.00, 2988.00, 876.43, 599.43),
('2025-12', 'India', 'Asia', 'DB 128+8', 'DB', 'Dog', 27, 2900.00, 2555.00, 611.65, 398.44),
('2026-01', 'India', 'Asia', 'DB 128+8', 'DB', 'Dog', 36, 3500.00, 2800.00, 654.38, 589.25),
('2025-12', 'South Africa', 'Africa', 'DB 256+8', 'DB', 'Dog', 37, 3700.00, 2988.00, 879.76, 698.76),
('2026-01', 'Kenya', 'Africa', 'DB 256+8', 'DB', 'Dog', 40, 4000.00, 3287.00, 1087.34, 966.26),
('2025-12', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 37, 3700.00, 3000.00, 1020.00, 876.21),
('2026-01', 'Pakistan', 'Asia', 'CA 128+8', 'CA', 'Cat', 35, 3591.00, 2900.00, 1003.00, 754.00),
('2025-12', 'Pakistan', 'Asia', 'CA 256+8', 'CA', 'Cat', 38, 3800.00, 3000.00, 1200.00, 645.38),
('2026-01', 'Pakistan', 'Asia', 'CA 256+8', 'CA', 'Cat', 35, 3600.00, 2877.00, 1100.00, 988.00),
('2025-12', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 27, 2800.00, 2300.00, 987.00, 654.21),
('2026-01', 'Kenya', 'Africa', 'CB 128+8', 'CB', 'Cat', 30, 3000.00, 2500.00, 1300.00, 1000.00),
('2025-12', 'Kenya', 'Africa', 'CB 256+8', 'CB', 'Cat', 27, 2900.00, 2497.00, 1087.40, 964.37),
('2026-01', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 40, 4000.00, 3500.00, 2000.00, 1432.88),
('2025-12', 'India', 'Asia', 'TA 128+8', 'TA', 'Tiger', 36, 3800.00, 3210.00, 1030.00, 783.41),
('2026-01', 'Kenya', 'Africa', 'TA 128+8', 'TA', 'Tiger', 35, 3600.00, 2900.00, 1028.00, 652.78),
('2025-12', 'South Africa', 'Africa', 'TA 256+8', 'TA', 'Tiger', 30, 3200.00, 2586.00, 999.00, 580.45),
('2026-01', 'South Africa', 'Africa', 'TA 256+8', 'TA', 'Tiger', 37, 3800.00, 3109.00, 1028.73, 618.76),
('2025-12', 'Pakistan', 'Asia', 'TB 128+8', 'TB', 'Tiger', 27, 3000.00, 2200.00, 980.00, 652.81),
('2026-01', 'Pakistan', 'Asia', 'TB 128+8', 'TB', 'Tiger', 26, 2600.00, 2000.00, 950.87, 579.62),
('2025-12', 'India', 'Asia', 'TB 256+8', 'TB', 'Tiger', 38, 3800.00, 3020.00, 1265.43, 873.24),
('2026-01', 'Pakistan', 'Asia', 'TB 256+8', 'TB', 'Tiger', 27, 2800.00, 2046.00, 986.38, 670.25);

-- 生成视图：

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

CREATE VIEW Display(id, h_Time, Model, Model_Label, Series, Country, Market, Sales, Price, Revenues, pre_Costs, Costs, Gross_profits, Gross_profits_ratio, RandD_expenses, After_sales_provision, Marketing_provision, Marketing_expenses, Labor_costs, Other_variable_expenses, Margin_profits, Other_fixed_expenses, Functional_expenses, Headquarters_expenses, Net_income, Exchange_time) AS
SELECT Sales_Price.id, Sales_Price.h_Time, Sales_Price.Model, Model.Model_label, Model.Series, Sales_Price.Country, Country.Market, Sales_Price.Sales, Sales_Price.Price, true_Revenues.Revenues, ROUND(true_Revenues.Costs/Sales_Price.Sales,2) AS pre_Costs, true_Revenues.Costs, true_Revenues.Gross_profits, ROUND(true_Revenues.Gross_profits/true_Revenues.Revenues,2) AS Gross_profits_ratio, true_Expenses.RandD_expenses, true_Expenses.After_sales_provision, true_Expenses.Marketing_provision, true_Expenses.Marketing_expenses, true_Expenses.Labor_cost, true_Expenses.Other_variable_expenses, true_Margin_profits.Margin_profits, true_Expenses.Other_fixed_expenses, true_Expenses.Functional_expenses, true_Expenses.Headquarters_expenses, true_Net_income.Net_income, Sales_Price.Exchange_time
FROM Sales_Price, Model, Country, true_Revenues, true_Expenses, true_Margin_profits, true_Net_income
WHERE Sales_Price.Model = Model.Model AND Sales_Price.Country = Country.Country AND Sales_Price.id = true_Expenses.id AND Sales_Price.id = true_Margin_profits.id AND Sales_Price.id = true_Net_income.id AND Sales_Price.id = true_Revenues.id
ORDER BY Country, Model, h_Time;

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

-- 角色
-- 注意：角色是全局对象（不属于某个库），如果之前已创建过会导致 1396 错误。
-- 先删除旧角色，再按需创建；并使用正确的 MySQL GRANT 语法，明确指定数据库对象。
DROP ROLE IF EXISTS 'FBPRole', 'SalespersonIndiaRole', 'SalespersonPakistanRole', 'SalespersonSouthAfricaRole', 'SalespersonKenyaRole', 'ManagerRole';

-- 创建角色（如已存在则跳过）
CREATE ROLE IF NOT EXISTS
	'FBPRole',
	'SalespersonIndiaRole',
	'SalespersonPakistanRole',
	'SalespersonSouthAfricaRole',
	'SalespersonKenyaRole',
	'ManagerRole';

-- FBP：表可读写，销售价格只读，综合展示视图只读
GRANT ALL PRIVILEGES ON `大作业-test4`.`Model`              TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Country`            TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Exchange`           TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Costs`              TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses1`    TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses2`    TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses3`    TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Regional_Expenses`  TO 'FBPRole';
GRANT SELECT           ON `大作业-test4`.`Sales_Price`      TO 'FBPRole';
GRANT SELECT           ON `大作业-test4`.`Display`          TO 'FBPRole';

-- 业务员：仅能操作本国销售价格视图，展示视图只读
GRANT SELECT                       ON `大作业-test4`.`DisplayIndia`        TO 'SalespersonIndiaRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price_India`   TO 'SalespersonIndiaRole';

GRANT SELECT                       ON `大作业-test4`.`DisplayPakistan`     TO 'SalespersonPakistanRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price_Pakistan` TO 'SalespersonPakistanRole';

GRANT SELECT                       ON `大作业-test4`.`DisplaySouthAfrica`  TO 'SalespersonSouthAfricaRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price_South_Africa` TO 'SalespersonSouthAfricaRole';

GRANT SELECT                       ON `大作业-test4`.`DisplayKenya`        TO 'SalespersonKenyaRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price_Kenya`    TO 'SalespersonKenyaRole';

-- 经理：聚合视图只读
GRANT SELECT ON `大作业-test4`.`s_Display`         TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`s_Display_Model`   TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`s_Display_Country` TO 'ManagerRole';
