
-- 确保 History 和 Budget 有唯一索引，以便支持"覆盖更新"
-- 如果之前没加过，请执行：
ALTER TABLE History ADD UNIQUE KEY `uk_hist` (h_Time, Country, Model);
ALTER TABLE Budget ADD UNIQUE KEY `uk_bud` (h_Time, Country, Model);