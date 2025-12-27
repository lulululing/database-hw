-- 权限补丁脚本（修正版）：基于你现有的角色结构完善权限
-- 在 Navicat 中执行此脚本

USE `大作业-test4`;

-- ============================================
-- 重要说明：
-- 你的数据库使用的是 Role（角色），需要授权给角色而不是用户
-- 角色名：FBPRole, SalespersonIndiaRole 等（带Role后缀）
-- ============================================

-- ============================================
-- 1. 为业务员角色增加查看本国所有相关数据的权限
-- ============================================

-- 印度业务员：增加查看本国History, Budget, Costs的权限
GRANT SELECT ON `大作业-test4`.`History` TO 'SalespersonIndiaRole';
GRANT SELECT ON `大作业-test4`.`Budget` TO 'SalespersonIndiaRole';
GRANT SELECT ON `大作业-test4`.`Costs` TO 'SalespersonIndiaRole';
-- 增加对基础表Sales_Price的查看和修改权限
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price` TO 'SalespersonIndiaRole';
-- 增加Model和Country表的查询权限（用于下拉选择）
GRANT SELECT ON `大作业-test4`.`Model` TO 'SalespersonIndiaRole';
GRANT SELECT ON `大作业-test4`.`Country` TO 'SalespersonIndiaRole';

-- 巴基斯坦业务员
GRANT SELECT ON `大作业-test4`.`History` TO 'SalespersonPakistanRole';
GRANT SELECT ON `大作业-test4`.`Budget` TO 'SalespersonPakistanRole';
GRANT SELECT ON `大作业-test4`.`Costs` TO 'SalespersonPakistanRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price` TO 'SalespersonPakistanRole';
GRANT SELECT ON `大作业-test4`.`Model` TO 'SalespersonPakistanRole';
GRANT SELECT ON `大作业-test4`.`Country` TO 'SalespersonPakistanRole';

-- 南非业务员
GRANT SELECT ON `大作业-test4`.`History` TO 'SalespersonSouthAfricaRole';
GRANT SELECT ON `大作业-test4`.`Budget` TO 'SalespersonSouthAfricaRole';
GRANT SELECT ON `大作业-test4`.`Costs` TO 'SalespersonSouthAfricaRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price` TO 'SalespersonSouthAfricaRole';
GRANT SELECT ON `大作业-test4`.`Model` TO 'SalespersonSouthAfricaRole';
GRANT SELECT ON `大作业-test4`.`Country` TO 'SalespersonSouthAfricaRole';

-- 肯尼亚业务员
GRANT SELECT ON `大作业-test4`.`History` TO 'SalespersonKenyaRole';
GRANT SELECT ON `大作业-test4`.`Budget` TO 'SalespersonKenyaRole';
GRANT SELECT ON `大作业-test4`.`Costs` TO 'SalespersonKenyaRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Sales_Price` TO 'SalespersonKenyaRole';
GRANT SELECT ON `大作业-test4`.`Model` TO 'SalespersonKenyaRole';
GRANT SELECT ON `大作业-test4`.`Country` TO 'SalespersonKenyaRole';

-- ============================================
-- 2. 为财务人员(FBP)增加完整的录入和删除权限
-- ============================================

-- 财务：成本数据（已有ALL PRIVILEGES，这里确认）
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Costs` TO 'FBPRole'; -- 已有

-- 财务：汇率数据（已有ALL PRIVILEGES）
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Exchange` TO 'FBPRole'; -- 已有

-- 财务：费用数据（已有ALL PRIVILEGES）
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Regional_Expenses` TO 'FBPRole'; -- 已有
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Ratio_Expenses1` TO 'FBPRole'; -- 已有
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Ratio_Expenses2` TO 'FBPRole'; -- 已有
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Ratio_Expenses3` TO 'FBPRole'; -- 已有

-- 财务：机型和国家数据（已有ALL PRIVILEGES）
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Model` TO 'FBPRole'; -- 已有
-- GRANT INSERT, UPDATE, DELETE ON `大作业-test4`.`Country` TO 'FBPRole'; -- 已有

-- 财务：确保能查看所有视图（用于数据展示页面）
GRANT SELECT ON `大作业-test4`.`true_Price` TO 'FBPRole';
GRANT SELECT ON `大作业-test4`.`true_Revenues` TO 'FBPRole';
GRANT SELECT ON `大作业-test4`.`true_Expenses` TO 'FBPRole';
GRANT SELECT ON `大作业-test4`.`true_Margin_profits` TO 'FBPRole';
GRANT SELECT ON `大作业-test4`.`true_Net_income` TO 'FBPRole';

-- ============================================
-- 3. 为经理增加必要的查看权限
-- ============================================

-- 经理：查看所有基础表（用于分析）
GRANT SELECT ON `大作业-test4`.`Sales_Price` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Costs` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Exchange` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Regional_Expenses` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Model` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Country` TO 'ManagerRole';

-- 经理：查看所有计算视图
GRANT SELECT ON `大作业-test4`.`Display` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Price` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Revenues` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Expenses` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Margin_profits` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`true_Net_income` TO 'ManagerRole';

-- ============================================
-- 4. 确保所有角色都能写入系统日志
-- ============================================

-- System_Log表的INSERT权限（已在9_更新精确权限_1.sql中设置，这里确认）
-- GRANT INSERT ON `大作业-test4`.`System_Log` TO 'ManagerRole'; -- 已有
-- GRANT INSERT, SELECT ON `大作业-test4`.`System_Log` TO 'FBPRole'; -- 已有
-- GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonIndiaRole'; -- 已有
-- GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonPakistanRole'; -- 已有
-- GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonSouthAfricaRole'; -- 已有
-- GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonKenyaRole'; -- 已有

-- ============================================
-- 5. 刷新权限
-- ============================================

FLUSH PRIVILEGES;

-- ============================================
-- 6. 验证权限设置（可选）
-- ============================================

-- 查看角色权限
SHOW GRANTS FOR 'FBPRole';
SHOW GRANTS FOR 'ManagerRole';
SHOW GRANTS FOR 'SalespersonIndiaRole';
SHOW GRANTS FOR 'SalespersonPakistanRole';
SHOW GRANTS FOR 'SalespersonSouthAfricaRole';
SHOW GRANTS FOR 'SalespersonKenyaRole';