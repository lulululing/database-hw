-- 检查System_Log表是否存在
USE `大作业-test4`;

-- 查看所有表
SHOW TABLES LIKE '%log%';

-- 如果没有System_Log表，创建它
CREATE TABLE IF NOT EXISTS `System_Log` (
    `Log_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `Log_Time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `Username` VARCHAR(100) NOT NULL,
    `Role` VARCHAR(100),
    `Action_Type` VARCHAR(100),
    `Details` TEXT,
    INDEX idx_username (Username),
    INDEX idx_time (Log_Time),
    INDEX idx_action (Action_Type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 测试插入一条日志
INSERT INTO `System_Log` (Username, Role, Action_Type, Details)
VALUES ('test_user', '经理 (Manager)', 'TEST', 'System log test');

-- 查看日志表内容
SELECT * FROM `System_Log` ORDER BY Log_Time DESC LIMIT 10;