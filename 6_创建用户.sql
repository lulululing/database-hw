-- 创建数据库用户并分配角色
-- 在 Navicat 中：右键数据库 → 运行 SQL 文件 → 选择本文件
-- 或在查询窗口直接执行

-- 注意：
-- 1. 以下密码为示例，请根据实际需求修改
-- 2. 用户创建后会拥有对应角色的所有权限
-- 3. '%' 表示可以从任何主机连接，生产环境建议改为具体 IP

-- 删除已存在的用户（如果有）
DROP USER IF EXISTS 'fbp_user'@'%';
DROP USER IF EXISTS 'manager_user'@'%';
DROP USER IF EXISTS 'sales_india'@'%';
DROP USER IF EXISTS 'sales_pakistan'@'%';
DROP USER IF EXISTS 'sales_south_africa'@'%';
DROP USER IF EXISTS 'sales_kenya'@'%';

-- 创建 FBP 用户（财务总监）
CREATE USER 'fbp_user'@'%' IDENTIFIED BY 'fbp123456';
GRANT 'FBPRole' TO 'fbp_user'@'%';
SET DEFAULT ROLE 'FBPRole' TO 'fbp_user'@'%';

-- 创建 Manager 用户（经理）
CREATE USER 'manager_user'@'%' IDENTIFIED BY 'manager123456';
GRANT 'ManagerRole' TO 'manager_user'@'%';
SET DEFAULT ROLE 'ManagerRole' TO 'manager_user'@'%';

-- 创建 India Salesperson
CREATE USER 'sales_india'@'%' IDENTIFIED BY 'india123456';
GRANT 'SalespersonIndiaRole' TO 'sales_india'@'%';
SET DEFAULT ROLE 'SalespersonIndiaRole' TO 'sales_india'@'%';

-- 创建 Pakistan Salesperson
CREATE USER 'sales_pakistan'@'%' IDENTIFIED BY 'pakistan123456';
GRANT 'SalespersonPakistanRole' TO 'sales_pakistan'@'%';
SET DEFAULT ROLE 'SalespersonPakistanRole' TO 'sales_pakistan'@'%';

-- 创建 South Africa Salesperson
CREATE USER 'sales_south_africa'@'%' IDENTIFIED BY 'southafrica123456';
GRANT 'SalespersonSouthAfricaRole' TO 'sales_south_africa'@'%';
SET DEFAULT ROLE 'SalespersonSouthAfricaRole' TO 'sales_south_africa'@'%';

-- 创建 Kenya Salesperson
CREATE USER 'sales_kenya'@'%' IDENTIFIED BY 'kenya123456';
GRANT 'SalespersonKenyaRole' TO 'sales_kenya'@'%';
SET DEFAULT ROLE 'SalespersonKenyaRole' TO 'sales_kenya'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 验证用户创建
SELECT user, host FROM mysql.user WHERE user LIKE 'fbp_%' OR user LIKE 'manager_%' OR user LIKE 'sales_%';
