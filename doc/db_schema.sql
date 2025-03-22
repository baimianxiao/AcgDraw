-- 抽卡请求记录表（记录单次抽卡操作）
CREATE TABLE gacha_records (
    record_id VARCHAR(36) PRIMARY KEY COMMENT '唯一记录ID',  -- 使用UUID或雪花算法生成
    uid VARCHAR(64) NOT NULL COMMENT '用户UID',
    game VARCHAR(50) NOT NULL COMMENT '游戏名称',
    gacha_mode ENUM('single', 'ten') NOT NULL COMMENT '抽卡模式',
    gacha_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '抽卡时间',
    gacha_count INT UNSIGNED NOT NULL COMMENT '累计抽卡数',
    INDEX idx_user (uid, game)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 抽卡结果明细表（记录每次抽卡的具体结果）
CREATE TABLE gacha_items (
    item_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '物品记录ID',
    record_id VARCHAR(36) NOT NULL COMMENT '关联记录ID',
    item_name VARCHAR(100) NOT NULL COMMENT '物品名称',
    rarity TINYINT UNSIGNED NOT NULL COMMENT '稀有度等级',
    item_type VARCHAR(50) NOT NULL COMMENT '物品类型/职业',
    FOREIGN KEY (record_id) REFERENCES gacha_records(record_id) ON DELETE CASCADE,
    INDEX idx_rarity (rarity),
    INDEX idx_record (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
