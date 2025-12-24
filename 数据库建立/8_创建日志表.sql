-- 7_创建日志表.sql
-- 用于记录用户的登录、修改等操作

CREATE TABLE IF NOT EXISTS System_Log (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL COMMENT '操作人用户名',
    Role VARCHAR(50) COMMENT '当时的角色',
    Action_Type VARCHAR(50) NOT NULL COMMENT '操作类型：LOGIN, UPDATE, EXPORT等',
    Details TEXT COMMENT '操作详情',
    Log_Time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间'
);

-- 既然加了新表，记得给管理员和财务赋予权限 (根据你的需求调整)
-- 这里为了方便，我们给所有角色赋予插入日志的权限，以便他们操作时能被记录
GRANT INSERT, SELECT ON `大作业-test4`.`System_Log` TO 'ManagerRole';
GRANT INSERT, SELECT ON `大作业-test4`.`System_Log` TO 'FBPRole';
GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonIndiaRole';
GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonPakistanRole';
GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonSouthAfricaRole';
GRANT INSERT ON `大作业-test4`.`System_Log` TO 'SalespersonKenyaRole';

FLUSH PRIVILEGES;