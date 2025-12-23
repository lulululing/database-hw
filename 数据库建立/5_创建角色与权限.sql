-- 角色与权限（MySQL 8.0）
-- 注意：角色是全局对象（不属于某个库），如果之前已创建过会导致 1396 错误。
-- 本脚本先删除旧角色，再按需创建；随后用正确的 GRANT 语法授予权限。


DROP ROLE IF EXISTS 'FBPRole', 'SalespersonIndiaRole', 'SalespersonPakistanRole', 'SalespersonSouthAfricaRole', 'SalespersonKenyaRole', 'ManagerRole';

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
