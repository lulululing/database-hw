-- 5_更新精确权限.sql
-- ⚠️ 必须先运行过 "6_创建用户.sql" 确保用户存在

-- 1. 重置所有角色权限 (先清空，再添加)
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'SalespersonIndiaRole', 'SalespersonPakistanRole', 'SalespersonSouthAfricaRole', 'SalespersonKenyaRole', 'FBPRole', 'ManagerRole';

-- ===================================================
-- 2. 销售员 (Salesperson)
-- 权限：对应国家的 Sales_Price (所有权限), Display (只读)
-- ===================================================

-- 印度
GRANT ALL PRIVILEGES ON `大作业-test4`.`Sales_Price_India` TO 'SalespersonIndiaRole';
GRANT SELECT         ON `大作业-test4`.`DisplayIndia`      TO 'SalespersonIndiaRole';

-- 巴基斯坦
GRANT ALL PRIVILEGES ON `大作业-test4`.`Sales_Price_Pakistan` TO 'SalespersonPakistanRole';
GRANT SELECT         ON `大作业-test4`.`DisplayPakistan`      TO 'SalespersonPakistanRole';

-- 南非
GRANT ALL PRIVILEGES ON `大作业-test4`.`Sales_Price_South_Africa` TO 'SalespersonSouthAfricaRole';
GRANT SELECT         ON `大作业-test4`.`DisplaySouthAfrica`       TO 'SalespersonSouthAfricaRole';

-- 肯尼亚
GRANT ALL PRIVILEGES ON `大作业-test4`.`Sales_Price_Kenya` TO 'SalespersonKenyaRole';
GRANT SELECT         ON `大作业-test4`.`DisplayKenya`      TO 'SalespersonKenyaRole';


-- ===================================================
-- 3. 财务BP (FBP)
-- 权限：
-- Display (只读), Sales_Price (只读)
-- 禁止访问：Display+国家, Sales_Price+国家, s_Display 系列
-- 其他表 (History, Budget, Costs, Ratio..., Exchange, Model, Country, Regional_Expenses): 全部权限
-- ===================================================

GRANT SELECT ON `大作业-test4`.`Display`     TO 'FBPRole';
GRANT SELECT ON `大作业-test4`.`Sales_Price` TO 'FBPRole';

GRANT ALL PRIVILEGES ON `大作业-test4`.`History`           TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Budget`            TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Costs`             TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses1`   TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses2`   TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Ratio_Expenses3`   TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Exchange`          TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Model`             TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Country`           TO 'FBPRole';
GRANT ALL PRIVILEGES ON `大作业-test4`.`Regional_Expenses` TO 'FBPRole';


-- ===================================================
-- 4. 经理 (Manager)
-- 权限：只对 3 张 s_Display 视图有 SELECT 权限
-- ===================================================

GRANT SELECT ON `大作业-test4`.`s_Display`         TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`s_Display_Country` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Revenues`     TO 'ManagerRole'; -- 假设这是第三张，或者是 true_Expenses? 根据视图文件定

FLUSH PRIVILEGES;