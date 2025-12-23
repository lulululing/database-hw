-- 第3步：创建触发器
-- ⚠️ 重要：此文件需要在 Navicat 查询窗口手动执行（不要用"运行SQL文件"功能）
-- 前提：已成功执行 1_创建表和索引.sql 和 2_插入数据.sql

-- 步骤：
-- 1. 打开 Navicat，双击数据库 `大作业-test4`，打开"查询"窗口
-- 2. 将本文件全部内容复制粘贴到查询窗口
-- 3. 点击"运行"按钮（或按F5）

DELIMITER $$

CREATE TRIGGER validate_model_label_insert
BEFORE INSERT ON Ratio_Expenses3
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Model WHERE Model_label = NEW.Model_label) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Model_label does not exist in Model table';
    END IF;
END$$

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
