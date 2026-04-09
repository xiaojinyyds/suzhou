-- 数据库迁移脚本：修复 statues 表字段以匹配模型定义
-- 执行时间：2025-11-20

-- 1. 重命名字段以匹配模型定义
ALTER TABLE statues CHANGE COLUMN check_radius radius INT DEFAULT 100 COMMENT '打卡半径（米）';
ALTER TABLE statues CHANGE COLUMN description introduction TEXT NULL COMMENT '简介';
ALTER TABLE statues CHANGE COLUMN image_url images TEXT NULL COMMENT '图片URL列表（JSON）';

-- 2. 添加缺失的字段（如果字段已存在会报错，可忽略）
ALTER TABLE statues ADD COLUMN icon VARCHAR(50) NULL COMMENT '图标 emoji' AFTER name;
ALTER TABLE statues ADD COLUMN order_index INT DEFAULT 0 COMMENT '排序序号' AFTER images;

-- 3. 查看表结构确认
DESCRIBE statues;

-- 4. 查看现有数据
SELECT * FROM statues;