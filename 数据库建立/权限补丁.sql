-- 补全 FBP (财务) 角色的权限：允许读写历史和预算数据
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`History` TO 'FBPRole';
GRANT SELECT, INSERT, UPDATE, DELETE ON `大作业-test4`.`Budget` TO 'FBPRole';

-- 补全 Manager (经理) 角色的权限：允许查看历史和预算数据
GRANT SELECT ON `大作业-test4`.`History` TO 'ManagerRole';
GRANT SELECT ON `大作业-test4`.`Budget` TO 'ManagerRole';

-- 刷新权限使其立即生效
FLUSH PRIVILEGES;