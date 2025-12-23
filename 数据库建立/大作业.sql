/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80032 (8.0.32)
 Source Host           : localhost:3306
 Source Schema         : 大作业-test4

 Target Server Type    : MySQL
 Target Server Version : 80032 (8.0.32)
 File Encoding         : 65001

 Date: 22/12/2025 12:25:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for budget
-- ----------------------------
DROP TABLE IF EXISTS `budget`;
CREATE TABLE `budget`  (
  `h_Time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Market` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Model_label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Series` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sales` int NULL DEFAULT NULL,
  `Revenues` decimal(20, 2) NULL DEFAULT NULL,
  `Gross_profits` decimal(20, 2) NULL DEFAULT NULL,
  `Margin_profits` decimal(20, 2) NULL DEFAULT NULL,
  `Net_income` decimal(20, 2) NULL DEFAULT NULL,
  INDEX `idx_budget_main`(`h_Time` ASC, `Country` ASC, `Model` ASC, `Market` ASC, `Model_label` ASC, `Series` ASC) USING BTREE,
  INDEX `idx_budget_columns`(`h_Time` ASC, `Country` ASC, `Model` ASC, `Sales` ASC, `Revenues` ASC, `Gross_profits` ASC, `Margin_profits` ASC, `Net_income` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of budget
-- ----------------------------
INSERT INTO `budget` VALUES ('2025-10', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 35, 3400.00, 2956.00, 1200.00, 605.00);
INSERT INTO `budget` VALUES ('2025-10', 'India', 'Asia', 'CA 128+8', 'CA', 'Cat', 32, 3200.00, 2500.00, 800.00, 540.35);
INSERT INTO `budget` VALUES ('2025-10', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 30, 3000.00, 2700.00, 899.26, 376.38);
INSERT INTO `budget` VALUES ('2025-10', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 29, 3500.00, 2900.00, 1000.00, 705.21);
INSERT INTO `budget` VALUES ('2025-11', 'Pakistan', 'Asia', 'TA 128+8', 'TA', 'Tiger', 35, 3700.00, 2903.00, 784.04, 623.00);
INSERT INTO `budget` VALUES ('2025-11', 'India', 'Asia', 'TA 256+8', 'TA', 'Tiger', 35, 3400.00, 2500.00, 750.76, 590.00);
INSERT INTO `budget` VALUES ('2025-11', 'South Africa', 'Africa', 'TB 128+8', 'TB', 'Tiger', 40, 4000.00, 3200.00, 976.38, 755.98);
INSERT INTO `budget` VALUES ('2025-11', 'Kenya', 'Africa', 'DA 128+8', 'DA', 'Dog', 33, 3500.00, 2900.00, 799.34, 601.23);
INSERT INTO `budget` VALUES ('2025-12', 'India', 'Asia', 'DA 128+8', 'DA', 'Dog', 34, 3300.00, 2500.00, 766.53, 599.08);
INSERT INTO `budget` VALUES ('2026-01', 'Pakistan', 'Asia', 'DA 128+8', 'DA', 'Dog', 33, 3100.00, 3010.00, 876.54, 622.35);
INSERT INTO `budget` VALUES ('2025-12', 'Pakistan', 'Asia', 'DA 256+8', 'DA', 'Dog', 20, 2000.00, 1550.00, 621.22, 376.21);
INSERT INTO `budget` VALUES ('2026-01', 'South Africa', 'Africa', 'DA 256+8', 'DA', 'Dog', 35, 3200.00, 2988.00, 876.43, 599.43);
INSERT INTO `budget` VALUES ('2025-12', 'India', 'Asia', 'DB 128+8', 'DB', 'Dog', 27, 2900.00, 2555.00, 611.65, 398.44);
INSERT INTO `budget` VALUES ('2026-01', 'India', 'Asia', 'DB 128+8', 'DB', 'Dog', 36, 3500.00, 2800.00, 654.38, 589.25);
INSERT INTO `budget` VALUES ('2025-12', 'South Africa', 'Africa', 'DB 256+8', 'DB', 'Dog', 37, 3700.00, 2988.00, 879.76, 698.76);
INSERT INTO `budget` VALUES ('2026-01', 'Kenya', 'Africa', 'DB 256+8', 'DB', 'Dog', 40, 4000.00, 3287.00, 1087.34, 966.26);
INSERT INTO `budget` VALUES ('2025-12', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 37, 3700.00, 3000.00, 1020.00, 876.21);
INSERT INTO `budget` VALUES ('2026-01', 'Pakistan', 'Asia', 'CA 128+8', 'CA', 'Cat', 35, 3591.00, 2900.00, 1003.00, 754.00);
INSERT INTO `budget` VALUES ('2025-12', 'Pakistan', 'Asia', 'CA 256+8', 'CA', 'Cat', 38, 3800.00, 3000.00, 1200.00, 645.38);
INSERT INTO `budget` VALUES ('2026-01', 'Pakistan', 'Asia', 'CA 256+8', 'CA', 'Cat', 35, 3600.00, 2877.00, 1100.00, 988.00);
INSERT INTO `budget` VALUES ('2025-12', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 27, 2800.00, 2300.00, 987.00, 654.21);
INSERT INTO `budget` VALUES ('2026-01', 'Kenya', 'Africa', 'CB 128+8', 'CB', 'Cat', 30, 3000.00, 2500.00, 1300.00, 1000.00);
INSERT INTO `budget` VALUES ('2025-12', 'Kenya', 'Africa', 'CB 256+8', 'CB', 'Cat', 27, 2900.00, 2497.00, 1087.40, 964.37);
INSERT INTO `budget` VALUES ('2026-01', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 40, 4000.00, 3500.00, 2000.00, 1432.88);
INSERT INTO `budget` VALUES ('2025-12', 'India', 'Asia', 'TA 128+8', 'TA', 'Tiger', 36, 3800.00, 3210.00, 1030.00, 783.41);
INSERT INTO `budget` VALUES ('2026-01', 'Kenya', 'Africa', 'TA 128+8', 'TA', 'Tiger', 35, 3600.00, 2900.00, 1028.00, 652.78);
INSERT INTO `budget` VALUES ('2025-12', 'South Africa', 'Africa', 'TA 256+8', 'TA', 'Tiger', 30, 3200.00, 2586.00, 999.00, 580.45);
INSERT INTO `budget` VALUES ('2026-01', 'South Africa', 'Africa', 'TA 256+8', 'TA', 'Tiger', 37, 3800.00, 3109.00, 1028.73, 618.76);
INSERT INTO `budget` VALUES ('2025-12', 'Pakistan', 'Asia', 'TB 128+8', 'TB', 'Tiger', 27, 3000.00, 2200.00, 980.00, 652.81);
INSERT INTO `budget` VALUES ('2026-01', 'Pakistan', 'Asia', 'TB 128+8', 'TB', 'Tiger', 26, 2600.00, 2000.00, 950.87, 579.62);
INSERT INTO `budget` VALUES ('2025-12', 'India', 'Asia', 'TB 256+8', 'TB', 'Tiger', 38, 3800.00, 3020.00, 1265.43, 873.24);
INSERT INTO `budget` VALUES ('2026-01', 'Pakistan', 'Asia', 'TB 256+8', 'TB', 'Tiger', 27, 2800.00, 2046.00, 986.38, 670.25);

-- ----------------------------
-- Table structure for costs
-- ----------------------------
DROP TABLE IF EXISTS `costs`;
CREATE TABLE `costs`  (
  `Costs_id` int NOT NULL,
  `Model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Costs_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Costs` decimal(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`Costs_id`) USING BTREE,
  UNIQUE INDEX `Model`(`Model` ASC, `Country` ASC, `Costs_time` ASC) USING BTREE,
  INDEX `Country`(`Country` ASC) USING BTREE,
  INDEX `idx_costs_composite`(`Model` ASC, `Country` ASC, `Costs_time` ASC) USING BTREE,
  CONSTRAINT `costs_ibfk_1` FOREIGN KEY (`Model`) REFERENCES `model` (`Model`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `costs_ibfk_2` FOREIGN KEY (`Country`) REFERENCES `country` (`Country`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `costs_chk_1` CHECK (`Costs_time` in (_utf8mb4'2025-10',_utf8mb4'2025-11',_utf8mb4'2025-12',_utf8mb4'2026-01',_utf8mb4'2026-02',_utf8mb4'2026-03',_utf8mb4'2026-04',_utf8mb4'2026-05',_utf8mb4'2026-06',_utf8mb4'2026-07',_utf8mb4'2026-08',_utf8mb4'2026-09'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of costs
-- ----------------------------
INSERT INTO `costs` VALUES (1, 'DA 128+8', 'India', '2025-12', 75.00);
INSERT INTO `costs` VALUES (2, 'DA 128+8', 'Pakistan', '2026-01', 76.00);
INSERT INTO `costs` VALUES (3, 'DA 256+8', 'Pakistan', '2025-12', 74.00);
INSERT INTO `costs` VALUES (4, 'DA 256+8', 'South Africa', '2026-01', 77.00);
INSERT INTO `costs` VALUES (5, 'DB 128+8', 'India', '2025-12', 80.00);
INSERT INTO `costs` VALUES (6, 'DB 128+8', 'India', '2026-01', 72.00);
INSERT INTO `costs` VALUES (7, 'DB 256+8', 'South Africa', '2025-12', 75.00);
INSERT INTO `costs` VALUES (8, 'DB 256+8', 'Kenya', '2026-01', 76.00);
INSERT INTO `costs` VALUES (9, 'CA 128+8', 'Kenya', '2025-12', 60.00);
INSERT INTO `costs` VALUES (10, 'CA 128+8', 'Pakistan', '2026-01', 61.00);
INSERT INTO `costs` VALUES (11, 'CA 256+8', 'Pakistan', '2025-12', 62.00);
INSERT INTO `costs` VALUES (12, 'CA 256+8', 'Pakistan', '2026-01', 63.00);
INSERT INTO `costs` VALUES (13, 'CB 128+8', 'India', '2025-12', 66.00);
INSERT INTO `costs` VALUES (14, 'CB 128+8', 'Kenya', '2026-01', 67.00);
INSERT INTO `costs` VALUES (15, 'CB 256+8', 'Kenya', '2025-12', 68.00);
INSERT INTO `costs` VALUES (16, 'CB 256+8', 'South Africa', '2026-01', 66.00);
INSERT INTO `costs` VALUES (17, 'TA 128+8', 'India', '2025-12', 81.00);
INSERT INTO `costs` VALUES (18, 'TA 128+8', 'Kenya', '2026-01', 85.00);
INSERT INTO `costs` VALUES (19, 'TA 256+8', 'South Africa', '2025-12', 85.00);
INSERT INTO `costs` VALUES (20, 'TA 256+8', 'South Africa', '2026-01', 83.00);
INSERT INTO `costs` VALUES (21, 'TB 128+8', 'Pakistan', '2025-12', 87.00);
INSERT INTO `costs` VALUES (22, 'TB 128+8', 'Pakistan', '2026-01', 85.00);
INSERT INTO `costs` VALUES (23, 'TB 256+8', 'India', '2025-12', 75.00);
INSERT INTO `costs` VALUES (24, 'TB 256+8', 'Pakistan', '2026-01', 76.00);

-- ----------------------------
-- Table structure for country
-- ----------------------------
DROP TABLE IF EXISTS `country`;
CREATE TABLE `country`  (
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Market` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Country`) USING BTREE,
  INDEX `idx_country_market`(`Market` ASC) USING BTREE,
  CONSTRAINT `country_chk_1` CHECK (`Market` in (_utf8mb4'Asia',_utf8mb4'Africa',_utf8mb4'South America'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of country
-- ----------------------------
INSERT INTO `country` VALUES ('Kenya', 'Africa');
INSERT INTO `country` VALUES ('South Africa', 'Africa');
INSERT INTO `country` VALUES ('India', 'Asia');
INSERT INTO `country` VALUES ('Pakistan', 'Asia');
INSERT INTO `country` VALUES ('Mexico', 'South America');
INSERT INTO `country` VALUES ('Peru', 'South America');

-- ----------------------------
-- Table structure for exchange
-- ----------------------------
DROP TABLE IF EXISTS `exchange`;
CREATE TABLE `exchange`  (
  `Exchange_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Exchange_rate` decimal(3, 2) NOT NULL,
  PRIMARY KEY (`Exchange_time`) USING BTREE,
  CONSTRAINT `exchange_chk_1` CHECK (`Exchange_time` in (_utf8mb4'2025-10',_utf8mb4'2025-11',_utf8mb4'2025-12',_utf8mb4'2026-01',_utf8mb4'2026-02',_utf8mb4'2026-03',_utf8mb4'2026-04',_utf8mb4'2026-05',_utf8mb4'2026-06',_utf8mb4'2026-07',_utf8mb4'2026-08',_utf8mb4'2026-09'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of exchange
-- ----------------------------
INSERT INTO `exchange` VALUES ('2025-10', 7.15);
INSERT INTO `exchange` VALUES ('2025-11', 7.20);
INSERT INTO `exchange` VALUES ('2025-12', 7.19);
INSERT INTO `exchange` VALUES ('2026-01', 7.16);
INSERT INTO `exchange` VALUES ('2026-02', 7.17);
INSERT INTO `exchange` VALUES ('2026-03', 7.18);
INSERT INTO `exchange` VALUES ('2026-04', 7.19);
INSERT INTO `exchange` VALUES ('2026-05', 7.20);
INSERT INTO `exchange` VALUES ('2026-06', 7.17);
INSERT INTO `exchange` VALUES ('2026-07', 7.18);
INSERT INTO `exchange` VALUES ('2026-08', 7.20);
INSERT INTO `exchange` VALUES ('2026-09', 7.21);

-- ----------------------------
-- Table structure for history
-- ----------------------------
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history`  (
  `h_Time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Market` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Model_label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Series` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sales` int NULL DEFAULT NULL,
  `Revenues` decimal(20, 2) NULL DEFAULT NULL,
  `Gross_profits` decimal(20, 2) NULL DEFAULT NULL,
  `Margin_profits` decimal(20, 2) NULL DEFAULT NULL,
  `Net_income` decimal(20, 2) NULL DEFAULT NULL,
  INDEX `idx_history_main`(`h_Time` ASC, `Country` ASC, `Model` ASC, `Market` ASC, `Model_label` ASC, `Series` ASC) USING BTREE,
  INDEX `idx_history_columns`(`h_Time` ASC, `Country` ASC, `Model` ASC, `Sales` ASC, `Revenues` ASC, `Gross_profits` ASC, `Margin_profits` ASC, `Net_income` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of history
-- ----------------------------
INSERT INTO `history` VALUES ('2025-10', 'Kenya', 'Africa', 'CA 128+8', 'CA', 'Cat', 36, 3600.00, 3000.00, 1000.00, 600.00);
INSERT INTO `history` VALUES ('2025-10', 'India', 'Asia', 'CA 128+8', 'CA', 'Cat', 35, 3600.00, 2876.00, 879.86, 589.96);
INSERT INTO `history` VALUES ('2025-10', 'South Africa', 'Africa', 'CB 256+8', 'CB', 'Cat', 29, 3000.00, 1600.00, 875.35, 325.78);
INSERT INTO `history` VALUES ('2025-10', 'India', 'Asia', 'CB 128+8', 'CB', 'Cat', 34, 3700.00, 3010.00, 866.66, 788.44);
INSERT INTO `history` VALUES ('2025-11', 'Pakistan', 'Asia', 'TA 128+8', 'TA', 'Tiger', 38, 3700.00, 3020.00, 800.00, 710.00);
INSERT INTO `history` VALUES ('2025-11', 'India', 'Asia', 'TA 256+8', 'TA', 'Tiger', 29, 2900.00, 2500.00, 750.76, 590.00);
INSERT INTO `history` VALUES ('2025-11', 'South Africa', 'Africa', 'TB 128+8', 'TB', 'Tiger', 40, 4200.00, 3200.00, 976.38, 755.98);
INSERT INTO `history` VALUES ('2025-11', 'Kenya', 'Africa', 'DA 128+8', 'DA', 'Dog', 35, 3400.00, 2900.00, 799.34, 601.23);

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model`  (
  `Model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Series` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Model_label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Model`) USING BTREE,
  INDEX `idx_model_series`(`Series` ASC) USING BTREE,
  INDEX `idx_model_label`(`Model_label` ASC) USING BTREE,
  INDEX `idx_model_composite`(`Model` ASC, `Series` ASC, `Model_label` ASC) USING BTREE,
  CONSTRAINT `model_ibfk_1` FOREIGN KEY (`Series`) REFERENCES `ratio_expenses1` (`Series`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of model
-- ----------------------------
INSERT INTO `model` VALUES ('CA 128+8', 'Cat', 'CA');
INSERT INTO `model` VALUES ('CA 256+8', 'Cat', 'CA');
INSERT INTO `model` VALUES ('CB 128+8', 'Cat', 'CB');
INSERT INTO `model` VALUES ('CB 256+8', 'Cat', 'CB');
INSERT INTO `model` VALUES ('DA 128+8', 'Dog', 'DA');
INSERT INTO `model` VALUES ('DA 256+8', 'Dog', 'DA');
INSERT INTO `model` VALUES ('DB 128+8', 'Dog', 'DB');
INSERT INTO `model` VALUES ('DB 256+8', 'Dog', 'DB');
INSERT INTO `model` VALUES ('TA 128+8', 'Tiger', 'TA');
INSERT INTO `model` VALUES ('TA 256+8', 'Tiger', 'TA');
INSERT INTO `model` VALUES ('TB 128+8', 'Tiger', 'TB');
INSERT INTO `model` VALUES ('TB 256+8', 'Tiger', 'TB');

-- ----------------------------
-- Table structure for ratio_expenses1
-- ----------------------------
DROP TABLE IF EXISTS `ratio_expenses1`;
CREATE TABLE `ratio_expenses1`  (
  `Series` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Software_product_amortization_rate_acc_cost` decimal(5, 4) NULL DEFAULT NULL,
  `RandD_rate_acc_cost` decimal(5, 4) NULL DEFAULT NULL,
  PRIMARY KEY (`Series`) USING BTREE,
  CONSTRAINT `ratio_expenses1_chk_1` CHECK (`Series` in (_utf8mb4'Dog',_utf8mb4'Cat',_utf8mb4'Tiger'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ratio_expenses1
-- ----------------------------
INSERT INTO `ratio_expenses1` VALUES ('Cat', 0.0150, 0.0250);
INSERT INTO `ratio_expenses1` VALUES ('Dog', 0.0450, 0.0300);
INSERT INTO `ratio_expenses1` VALUES ('Tiger', 0.0350, 0.0200);

-- ----------------------------
-- Table structure for ratio_expenses2
-- ----------------------------
DROP TABLE IF EXISTS `ratio_expenses2`;
CREATE TABLE `ratio_expenses2`  (
  `Ratio_expenses2_id` int NOT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Functional_cost_allocation_rate_acc_cost` decimal(5, 4) NULL DEFAULT NULL,
  `Business_group_headquarters_allocation_rate_acc_cost` decimal(5, 4) NULL DEFAULT NULL,
  `Marketing_activities_provision_rate_acc_revenue` decimal(5, 4) NULL DEFAULT NULL,
  PRIMARY KEY (`Ratio_expenses2_id`) USING BTREE,
  UNIQUE INDEX `Country`(`Country` ASC) USING BTREE,
  INDEX `idx_ratio_expenses2_country_covers`(`Country` ASC, `Functional_cost_allocation_rate_acc_cost` ASC, `Business_group_headquarters_allocation_rate_acc_cost` ASC, `Marketing_activities_provision_rate_acc_revenue` ASC) USING BTREE,
  CONSTRAINT `ratio_expenses2_ibfk_1` FOREIGN KEY (`Country`) REFERENCES `country` (`Country`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ratio_expenses2
-- ----------------------------
INSERT INTO `ratio_expenses2` VALUES (3, 'India', 0.0150, 0.0250, 0.0300);
INSERT INTO `ratio_expenses2` VALUES (1, 'Kenya', 0.0250, 0.0350, 0.0500);
INSERT INTO `ratio_expenses2` VALUES (4, 'Mexico', 0.0200, 0.0350, 0.0400);
INSERT INTO `ratio_expenses2` VALUES (6, 'Pakistan', 0.0300, 0.0350, 0.0250);
INSERT INTO `ratio_expenses2` VALUES (5, 'Peru', 0.0250, 0.0350, 0.0450);
INSERT INTO `ratio_expenses2` VALUES (2, 'South Africa', 0.0300, 0.0300, 0.0500);

-- ----------------------------
-- Table structure for ratio_expenses3
-- ----------------------------
DROP TABLE IF EXISTS `ratio_expenses3`;
CREATE TABLE `ratio_expenses3`  (
  `Ratio_expenses3_id` int NOT NULL,
  `Model_label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `After_sales_provision_rate_acc_cost` decimal(5, 4) NULL DEFAULT NULL,
  PRIMARY KEY (`Ratio_expenses3_id`) USING BTREE,
  INDEX `Country`(`Country` ASC) USING BTREE,
  INDEX `idx_ratio_expenses3_composite`(`Model_label` ASC, `Country` ASC) USING BTREE,
  CONSTRAINT `ratio_expenses3_ibfk_1` FOREIGN KEY (`Country`) REFERENCES `country` (`Country`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ratio_expenses3
-- ----------------------------
INSERT INTO `ratio_expenses3` VALUES (1, 'DA', 'India', 0.0250);
INSERT INTO `ratio_expenses3` VALUES (2, 'DA', 'Pakistan', 0.0260);
INSERT INTO `ratio_expenses3` VALUES (3, 'DA', 'Kenya', 0.0240);
INSERT INTO `ratio_expenses3` VALUES (4, 'DA', 'South Africa', 0.0250);
INSERT INTO `ratio_expenses3` VALUES (5, 'DA', 'Mexico', 0.0240);
INSERT INTO `ratio_expenses3` VALUES (6, 'DA', 'Peru', 0.0210);
INSERT INTO `ratio_expenses3` VALUES (7, 'DB', 'India', 0.0300);
INSERT INTO `ratio_expenses3` VALUES (8, 'DB', 'Pakistan', 0.0310);
INSERT INTO `ratio_expenses3` VALUES (9, 'DB', 'Kenya', 0.0290);
INSERT INTO `ratio_expenses3` VALUES (10, 'DB', 'South Africa', 0.0250);
INSERT INTO `ratio_expenses3` VALUES (11, 'DB', 'Mexico', 0.0300);
INSERT INTO `ratio_expenses3` VALUES (12, 'DB', 'Peru', 0.0270);
INSERT INTO `ratio_expenses3` VALUES (13, 'CA', 'India', 0.0260);
INSERT INTO `ratio_expenses3` VALUES (14, 'CA', 'Pakistan', 0.0310);
INSERT INTO `ratio_expenses3` VALUES (15, 'CA', 'Kenya', 0.0290);
INSERT INTO `ratio_expenses3` VALUES (16, 'CA', 'South Africa', 0.0190);
INSERT INTO `ratio_expenses3` VALUES (17, 'CA', 'Mexico', 0.0280);
INSERT INTO `ratio_expenses3` VALUES (18, 'CA', 'Peru', 0.0270);
INSERT INTO `ratio_expenses3` VALUES (19, 'CB', 'India', 0.0260);
INSERT INTO `ratio_expenses3` VALUES (20, 'CB', 'Pakistan', 0.0190);
INSERT INTO `ratio_expenses3` VALUES (21, 'CB', 'Kenya', 0.0390);
INSERT INTO `ratio_expenses3` VALUES (22, 'CB', 'South Africa', 0.0270);
INSERT INTO `ratio_expenses3` VALUES (23, 'CB', 'Mexico', 0.0280);
INSERT INTO `ratio_expenses3` VALUES (24, 'CB', 'Peru', 0.0230);
INSERT INTO `ratio_expenses3` VALUES (25, 'TA', 'India', 0.0270);
INSERT INTO `ratio_expenses3` VALUES (26, 'TA', 'Pakistan', 0.0190);
INSERT INTO `ratio_expenses3` VALUES (27, 'TA', 'Kenya', 0.0280);
INSERT INTO `ratio_expenses3` VALUES (28, 'TA', 'South Africa', 0.0250);
INSERT INTO `ratio_expenses3` VALUES (29, 'TA', 'Mexico', 0.0250);
INSERT INTO `ratio_expenses3` VALUES (30, 'TA', 'Peru', 0.0230);
INSERT INTO `ratio_expenses3` VALUES (31, 'TB', 'India', 0.0240);
INSERT INTO `ratio_expenses3` VALUES (32, 'TB', 'Pakistan', 0.0220);
INSERT INTO `ratio_expenses3` VALUES (33, 'TB', 'Kenya', 0.0270);
INSERT INTO `ratio_expenses3` VALUES (34, 'TB', 'South Africa', 0.0280);
INSERT INTO `ratio_expenses3` VALUES (35, 'TB', 'Mexico', 0.0240);
INSERT INTO `ratio_expenses3` VALUES (36, 'TB', 'Peru', 0.0240);

-- ----------------------------
-- Table structure for regional_expenses
-- ----------------------------
DROP TABLE IF EXISTS `regional_expenses`;
CREATE TABLE `regional_expenses`  (
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Expenses_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Marketing_expenses` decimal(10, 2) NULL DEFAULT NULL,
  `Labor_cost` decimal(10, 2) NULL DEFAULT NULL,
  `Other_variable_expenses` decimal(10, 2) NULL DEFAULT NULL,
  `Other_fixed_expenses` decimal(10, 2) NULL DEFAULT NULL,
  UNIQUE INDEX `Country`(`Country` ASC, `Expenses_time` ASC) USING BTREE,
  INDEX `idx_regional_expenses_composite`(`Country` ASC, `Expenses_time` ASC) USING BTREE,
  CONSTRAINT `regional_expenses_ibfk_1` FOREIGN KEY (`Country`) REFERENCES `country` (`Country`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of regional_expenses
-- ----------------------------
INSERT INTO `regional_expenses` VALUES ('India', '2025-12', 25.00, 30.00, 25.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('India', '2026-01', 26.00, 27.00, 28.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('India', '2026-02', 27.00, 25.00, 26.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('India', '2026-03', 28.00, 26.00, 27.00, 31.00);
INSERT INTO `regional_expenses` VALUES ('India', '2026-04', 24.00, 23.00, 29.00, 31.00);
INSERT INTO `regional_expenses` VALUES ('India', '2026-05', 25.00, 26.00, 27.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2025-12', 27.00, 26.00, 25.00, 24.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2026-01', 28.00, 26.00, 28.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2026-02', 25.00, 25.00, 27.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2026-03', 27.00, 25.00, 26.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2026-04', 25.00, 22.00, 26.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Pakistan', '2026-05', 25.00, 27.00, 27.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2025-12', 28.00, 27.00, 24.00, 25.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2026-01', 29.00, 24.00, 26.00, 27.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2026-02', 26.00, 27.00, 23.00, 28.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2026-03', 24.00, 30.00, 26.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2026-04', 26.00, 21.00, 21.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('South Africa', '2026-05', 23.00, 30.00, 27.00, 30.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2025-12', 26.00, 28.00, 29.00, 25.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2026-01', 23.00, 24.00, 25.00, 28.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2026-02', 26.00, 28.00, 28.00, 24.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2026-03', 26.00, 26.00, 27.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2026-04', 27.00, 28.00, 21.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Kenya', '2026-05', 26.00, 24.00, 27.00, 28.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2025-12', 27.00, 23.00, 31.00, 22.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2026-01', 25.00, 29.00, 22.00, 24.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2026-02', 23.00, 30.00, 22.00, 24.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2026-03', 25.00, 25.00, 25.00, 25.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2026-04', 26.00, 27.00, 29.00, 22.00);
INSERT INTO `regional_expenses` VALUES ('Mexico', '2026-05', 24.00, 26.00, 24.00, 26.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2025-12', 25.00, 26.00, 27.00, 26.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2026-01', 24.00, 28.00, 21.00, 21.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2026-02', 27.00, 26.00, 21.00, 26.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2026-03', 24.00, 26.00, 28.00, 29.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2026-04', 22.00, 25.00, 27.00, 21.00);
INSERT INTO `regional_expenses` VALUES ('Peru', '2026-05', 26.00, 28.00, 23.00, 29.00);

-- ----------------------------
-- Table structure for sales_price
-- ----------------------------
DROP TABLE IF EXISTS `sales_price`;
CREATE TABLE `sales_price`  (
  `id` int NOT NULL,
  `Model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `h_Time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Currency` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sales` int NULL DEFAULT NULL,
  `Price` decimal(10, 2) NULL DEFAULT NULL,
  `Exchange_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `Model`(`Model` ASC, `Country` ASC, `h_Time` ASC) USING BTREE,
  INDEX `Country`(`Country` ASC) USING BTREE,
  INDEX `idx_sales_price_composite`(`Model` ASC, `Country` ASC, `h_Time` ASC) USING BTREE,
  INDEX `idx_sales_price_time`(`h_Time` ASC) USING BTREE,
  INDEX `idx_sales_price_currency`(`Currency` ASC) USING BTREE,
  INDEX `idx_sales_price_exchange_time`(`Exchange_time` ASC) USING BTREE,
  INDEX `idx_true_revenues_join`(`Model` ASC, `Country` ASC, `id` ASC, `h_Time` ASC, `Sales` ASC) USING BTREE,
  CONSTRAINT `sales_price_ibfk_1` FOREIGN KEY (`Model`) REFERENCES `model` (`Model`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sales_price_ibfk_2` FOREIGN KEY (`Country`) REFERENCES `country` (`Country`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sales_price_ibfk_3` FOREIGN KEY (`Exchange_time`) REFERENCES `exchange` (`Exchange_time`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sales_price_chk_1` CHECK (`h_Time` in (_utf8mb4'2025-10',_utf8mb4'2025-11',_utf8mb4'2025-12',_utf8mb4'2026-01',_utf8mb4'2026-02',_utf8mb4'2026-03',_utf8mb4'2026-04',_utf8mb4'2026-05',_utf8mb4'2026-06',_utf8mb4'2026-07',_utf8mb4'2026-08',_utf8mb4'2026-09')),
  CONSTRAINT `sales_price_chk_2` CHECK (`Currency` in (_utf8mb4'CHY',_utf8mb4'USD')),
  CONSTRAINT `sales_price_chk_3` CHECK (`Exchange_time` = `h_Time`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sales_price
-- ----------------------------
INSERT INTO `sales_price` VALUES (1, 'DA 128+8', 'India', '2025-12', 'CHY', 20, 101.00, '2025-12');
INSERT INTO `sales_price` VALUES (2, 'DA 128+8', 'Pakistan', '2026-01', 'CHY', 35, 102.00, '2026-01');
INSERT INTO `sales_price` VALUES (3, 'DA 256+8', 'Pakistan', '2025-12', 'CHY', 15, 110.00, '2025-12');
INSERT INTO `sales_price` VALUES (4, 'DA 256+8', 'South Africa', '2026-01', 'USD', 30, 17.20, '2026-01');
INSERT INTO `sales_price` VALUES (5, 'DB 128+8', 'India', '2025-12', 'CHY', 30, 105.00, '2025-12');
INSERT INTO `sales_price` VALUES (6, 'DB 128+8', 'India', '2026-01', 'CHY', 37, 106.00, '2026-01');
INSERT INTO `sales_price` VALUES (7, 'DB 256+8', 'South Africa', '2025-12', 'USD', 40, 17.50, '2025-12');
INSERT INTO `sales_price` VALUES (8, 'DB 256+8', 'Kenya', '2026-01', 'CHY', 40, 100.00, '2026-01');
INSERT INTO `sales_price` VALUES (9, 'CA 128+8', 'Kenya', '2025-12', 'CHY', 41, 100.00, '2025-12');
INSERT INTO `sales_price` VALUES (10, 'CA 128+8', 'Pakistan', '2026-01', 'CHY', 37, 108.00, '2026-01');
INSERT INTO `sales_price` VALUES (11, 'CA 256+8', 'Pakistan', '2025-12', 'CHY', 38, 109.00, '2025-12');
INSERT INTO `sales_price` VALUES (12, 'CA 256+8', 'Pakistan', '2026-01', 'CHY', 39, 105.00, '2026-01');
INSERT INTO `sales_price` VALUES (13, 'CB 128+8', 'India', '2025-12', 'CHY', 20, 99.00, '2025-12');
INSERT INTO `sales_price` VALUES (14, 'CB 128+8', 'Kenya', '2026-01', 'CHY', 25, 103.50, '2026-01');
INSERT INTO `sales_price` VALUES (15, 'CB 256+8', 'Kenya', '2025-12', 'CHY', 30, 103.50, '2025-12');
INSERT INTO `sales_price` VALUES (16, 'CB 256+8', 'South Africa', '2026-01', 'USD', 44, 15.50, '2026-01');
INSERT INTO `sales_price` VALUES (17, 'TA 128+8', 'India', '2025-12', 'CHY', 30, 106.00, '2025-12');
INSERT INTO `sales_price` VALUES (18, 'TA 128+8', 'Kenya', '2026-01', 'CHY', 34, 104.00, '2026-01');
INSERT INTO `sales_price` VALUES (19, 'TA 256+8', 'South Africa', '2025-12', 'USD', 34, 17.00, '2025-12');
INSERT INTO `sales_price` VALUES (20, 'TA 256+8', 'South Africa', '2026-01', 'USD', 35, 16.50, '2026-01');

-- ----------------------------
-- View structure for display
-- ----------------------------
DROP VIEW IF EXISTS `display`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `display` AS select `sales_price`.`id` AS `id`,`sales_price`.`h_Time` AS `h_Time`,`sales_price`.`Model` AS `Model`,`model`.`Model_label` AS `Model_label`,`model`.`Series` AS `Series`,`sales_price`.`Country` AS `Country`,`country`.`Market` AS `Market`,`sales_price`.`Sales` AS `Sales`,`sales_price`.`Price` AS `Price`,`true_revenues`.`Revenues` AS `Revenues`,round((`true_revenues`.`Costs` / `sales_price`.`Sales`),2) AS `pre_Costs`,`true_revenues`.`Costs` AS `Costs`,`true_revenues`.`Gross_profits` AS `Gross_profits`,round((`true_revenues`.`Gross_profits` / `true_revenues`.`Revenues`),2) AS `Gross_profits_ratio`,`true_expenses`.`RandD_expenses` AS `RandD_expenses`,`true_expenses`.`After_sales_provision` AS `After_sales_provision`,`true_expenses`.`Marketing_provision` AS `Marketing_provision`,`true_expenses`.`Marketing_expenses` AS `Marketing_expenses`,`true_expenses`.`Labor_cost` AS `Labor_cost`,`true_expenses`.`Other_variable_expenses` AS `Other_variable_expenses`,`true_margin_profits`.`Margin_profits` AS `Margin_profits`,`true_expenses`.`Other_fixed_expenses` AS `Other_fixed_expenses`,`true_expenses`.`Functional_expenses` AS `Functional_expenses`,`true_expenses`.`Headquarters_expenses` AS `Headquarters_expenses`,`true_net_income`.`Net_income` AS `Net_income`,`sales_price`.`Exchange_time` AS `Exchange_time` from ((((((`sales_price` join `model`) join `country`) join `true_revenues`) join `true_expenses`) join `true_margin_profits`) join `true_net_income`) where ((`sales_price`.`Model` = `model`.`Model`) and (`sales_price`.`Country` = `country`.`Country`) and (`sales_price`.`id` = `true_expenses`.`id`) and (`sales_price`.`id` = `true_margin_profits`.`id`) and (`sales_price`.`id` = `true_net_income`.`id`) and (`sales_price`.`id` = `true_revenues`.`id`)) order by `sales_price`.`Country`,`sales_price`.`Model`,`sales_price`.`h_Time`;

-- ----------------------------
-- View structure for displayindia
-- ----------------------------
DROP VIEW IF EXISTS `displayindia`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `displayindia` AS select `display`.`id` AS `id`,`display`.`h_Time` AS `h_Time`,`display`.`Model` AS `Model`,`display`.`Model_Label` AS `Model_Label`,`display`.`Series` AS `Series`,`display`.`Country` AS `Country`,`display`.`Market` AS `Market`,`display`.`Sales` AS `Sales`,`display`.`Price` AS `Price`,`display`.`Revenues` AS `Revenues`,`display`.`pre_Costs` AS `pre_Costs`,`display`.`Costs` AS `Costs`,`display`.`Gross_profits` AS `Gross_profits`,`display`.`Gross_profits_ratio` AS `Gross_profits_ratio`,`display`.`RandD_expenses` AS `RandD_expenses`,`display`.`After_sales_provision` AS `After_sales_provision`,`display`.`Marketing_provision` AS `Marketing_provision`,`display`.`Marketing_expenses` AS `Marketing_expenses`,`display`.`Labor_costs` AS `Labor_costs`,`display`.`Other_variable_expenses` AS `Other_variable_expenses`,`display`.`Margin_profits` AS `Margin_profits`,`display`.`Other_fixed_expenses` AS `Other_fixed_expenses`,`display`.`Functional_expenses` AS `Functional_expenses`,`display`.`Headquarters_expenses` AS `Headquarters_expenses`,`display`.`Net_income` AS `Net_income` from `display` where (`display`.`Country` = 'India') order by `display`.`Country`,`display`.`Model`,`display`.`h_Time`;

-- ----------------------------
-- View structure for displaykenya
-- ----------------------------
DROP VIEW IF EXISTS `displaykenya`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `displaykenya` AS select `display`.`id` AS `id`,`display`.`h_Time` AS `h_Time`,`display`.`Model` AS `Model`,`display`.`Model_Label` AS `Model_Label`,`display`.`Series` AS `Series`,`display`.`Country` AS `Country`,`display`.`Market` AS `Market`,`display`.`Sales` AS `Sales`,`display`.`Price` AS `Price`,`display`.`Revenues` AS `Revenues`,`display`.`pre_Costs` AS `pre_Costs`,`display`.`Costs` AS `Costs`,`display`.`Gross_profits` AS `Gross_profits`,`display`.`Gross_profits_ratio` AS `Gross_profits_ratio`,`display`.`RandD_expenses` AS `RandD_expenses`,`display`.`After_sales_provision` AS `After_sales_provision`,`display`.`Marketing_provision` AS `Marketing_provision`,`display`.`Marketing_expenses` AS `Marketing_expenses`,`display`.`Labor_costs` AS `Labor_costs`,`display`.`Other_variable_expenses` AS `Other_variable_expenses`,`display`.`Margin_profits` AS `Margin_profits`,`display`.`Other_fixed_expenses` AS `Other_fixed_expenses`,`display`.`Functional_expenses` AS `Functional_expenses`,`display`.`Headquarters_expenses` AS `Headquarters_expenses`,`display`.`Net_income` AS `Net_income` from `display` where (`display`.`Country` = 'Kenya') order by `display`.`Country`,`display`.`Model`,`display`.`h_Time`;

-- ----------------------------
-- View structure for displaypakistan
-- ----------------------------
DROP VIEW IF EXISTS `displaypakistan`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `displaypakistan` AS select `display`.`id` AS `id`,`display`.`h_Time` AS `h_Time`,`display`.`Model` AS `Model`,`display`.`Model_Label` AS `Model_Label`,`display`.`Series` AS `Series`,`display`.`Country` AS `Country`,`display`.`Market` AS `Market`,`display`.`Sales` AS `Sales`,`display`.`Price` AS `Price`,`display`.`Revenues` AS `Revenues`,`display`.`pre_Costs` AS `pre_Costs`,`display`.`Costs` AS `Costs`,`display`.`Gross_profits` AS `Gross_profits`,`display`.`Gross_profits_ratio` AS `Gross_profits_ratio`,`display`.`RandD_expenses` AS `RandD_expenses`,`display`.`After_sales_provision` AS `After_sales_provision`,`display`.`Marketing_provision` AS `Marketing_provision`,`display`.`Marketing_expenses` AS `Marketing_expenses`,`display`.`Labor_costs` AS `Labor_costs`,`display`.`Other_variable_expenses` AS `Other_variable_expenses`,`display`.`Margin_profits` AS `Margin_profits`,`display`.`Other_fixed_expenses` AS `Other_fixed_expenses`,`display`.`Functional_expenses` AS `Functional_expenses`,`display`.`Headquarters_expenses` AS `Headquarters_expenses`,`display`.`Net_income` AS `Net_income` from `display` where (`display`.`Country` = 'Pakistan') order by `display`.`Country`,`display`.`Model`,`display`.`h_Time`;

-- ----------------------------
-- View structure for displaysouthafrica
-- ----------------------------
DROP VIEW IF EXISTS `displaysouthafrica`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `displaysouthafrica` AS select `display`.`id` AS `id`,`display`.`h_Time` AS `h_Time`,`display`.`Model` AS `Model`,`display`.`Model_Label` AS `Model_Label`,`display`.`Series` AS `Series`,`display`.`Country` AS `Country`,`display`.`Market` AS `Market`,`display`.`Sales` AS `Sales`,`display`.`Price` AS `Price`,`display`.`Revenues` AS `Revenues`,`display`.`pre_Costs` AS `pre_Costs`,`display`.`Costs` AS `Costs`,`display`.`Gross_profits` AS `Gross_profits`,`display`.`Gross_profits_ratio` AS `Gross_profits_ratio`,`display`.`RandD_expenses` AS `RandD_expenses`,`display`.`After_sales_provision` AS `After_sales_provision`,`display`.`Marketing_provision` AS `Marketing_provision`,`display`.`Marketing_expenses` AS `Marketing_expenses`,`display`.`Labor_costs` AS `Labor_costs`,`display`.`Other_variable_expenses` AS `Other_variable_expenses`,`display`.`Margin_profits` AS `Margin_profits`,`display`.`Other_fixed_expenses` AS `Other_fixed_expenses`,`display`.`Functional_expenses` AS `Functional_expenses`,`display`.`Headquarters_expenses` AS `Headquarters_expenses`,`display`.`Net_income` AS `Net_income` from `display` where (`display`.`Country` = 'South Africa') order by `display`.`Country`,`display`.`Model`,`display`.`h_Time`;

-- ----------------------------
-- View structure for s_display
-- ----------------------------
DROP VIEW IF EXISTS `s_display`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `s_display` AS select `display`.`h_Time` AS `h_Time`,`display`.`Country` AS `Country`,`display`.`Market` AS `Market`,`display`.`Model` AS `Model`,`display`.`Model_Label` AS `Model_label`,`display`.`Series` AS `Series`,coalesce(`history`.`Sales`,0) AS `Sales_history`,coalesce(`display`.`Sales`,0) AS `Sales_forecasting`,coalesce(`budget`.`Sales`,0) AS `Sales_budget`,coalesce(`history`.`Revenues`,0) AS `Revenues_history`,coalesce(`display`.`Revenues`,0) AS `Revenues_forecasting`,coalesce(`budget`.`Revenues`,0) AS `Revenues_budget`,coalesce(`history`.`Gross_profits`,0) AS `Gross_profits_history`,coalesce(`display`.`Gross_profits`,0) AS `Gross_profits_forecasting`,coalesce(`budget`.`Gross_profits`,0) AS `Gross_profits_budget`,coalesce(`history`.`Margin_profits`,0) AS `Margin_profits_history`,coalesce(`display`.`Margin_profits`,0) AS `Margin_profits_forecasting`,coalesce(`budget`.`Margin_profits`,0) AS `Margin_profits_budget`,coalesce(`history`.`Net_income`,0) AS `Net_income_history`,coalesce(`display`.`Net_income`,0) AS `Net_income_forecasting`,coalesce(`budget`.`Net_income`,0) AS `Net_income_budget` from ((`display` left join `history` on(((`display`.`h_Time` = `history`.`h_Time`) and (`display`.`Country` = `history`.`Country`) and (`display`.`Model` = `history`.`Model`)))) left join `budget` on(((`display`.`h_Time` = `budget`.`h_Time`) and (`display`.`Country` = `budget`.`Country`) and (`display`.`Model` = `budget`.`Model`)))) order by `display`.`Model`,`display`.`h_Time`;

-- ----------------------------
-- View structure for s_display_country
-- ----------------------------
DROP VIEW IF EXISTS `s_display_country`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `s_display_country` AS select `s_display`.`h_Time` AS `h_Time`,`s_display`.`Country` AS `Country`,`s_display`.`Market` AS `Market`,sum(`s_display`.`Sales_history`) AS `SUM(Sales_history)`,sum(`s_display`.`Sales_forecasting`) AS `SUM(Sales_forecasting)`,sum(`s_display`.`Sales_budget`) AS `SUM(Sales_budget)`,sum(`s_display`.`Revenues_history`) AS `SUM(Revenues_history)`,sum(`s_display`.`Revenues_forecasting`) AS `SUM(Revenues_forecasting)`,sum(`s_display`.`Revenues_budget`) AS `SUM(Revenues_budget)`,sum(`s_display`.`Gross_profits_history`) AS `SUM(Gross_profits_history)`,sum(`s_display`.`Gross_profits_forecasting`) AS `SUM(Gross_profits_forecasting)`,sum(`s_display`.`Gross_profits_budget`) AS `SUM(Gross_profits_budget)`,sum(`s_display`.`Margin_profits_history`) AS `SUM(Margin_profits_history)`,sum(`s_display`.`Margin_profits_forecasting`) AS `SUM(Margin_profits_forecasting)`,sum(`s_display`.`Margin_profits_budget`) AS `SUM(Margin_profits_budget)`,sum(`s_display`.`Net_income_history`) AS `SUM(Net_income_history)`,sum(`s_display`.`Net_income_forecasting`) AS `SUM(Net_income_forecasting)`,sum(`s_display`.`Net_income_budget`) AS `SUM(Net_income_budget)` from `s_display` group by `s_display`.`h_Time`,`s_display`.`Country`,`s_display`.`Market`;

-- ----------------------------
-- View structure for s_display_model
-- ----------------------------
DROP VIEW IF EXISTS `s_display_model`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `s_display_model` AS select `s_display`.`h_Time` AS `h_Time`,`s_display`.`Model` AS `Model`,`s_display`.`Model_label` AS `Model_label`,`s_display`.`Series` AS `Series`,sum(`s_display`.`Sales_history`) AS `SUM(Sales_history)`,sum(`s_display`.`Sales_forecasting`) AS `SUM(Sales_forecasting)`,sum(`s_display`.`Sales_budget`) AS `SUM(Sales_budget)`,sum(`s_display`.`Revenues_history`) AS `SUM(Revenues_history)`,sum(`s_display`.`Revenues_forecasting`) AS `SUM(Revenues_forecasting)`,sum(`s_display`.`Revenues_budget`) AS `SUM(Revenues_budget)`,sum(`s_display`.`Gross_profits_history`) AS `SUM(Gross_profits_history)`,sum(`s_display`.`Gross_profits_forecasting`) AS `SUM(Gross_profits_forecasting)`,sum(`s_display`.`Gross_profits_budget`) AS `SUM(Gross_profits_budget)`,sum(`s_display`.`Margin_profits_history`) AS `SUM(Margin_profits_history)`,sum(`s_display`.`Margin_profits_forecasting`) AS `SUM(Margin_profits_forecasting)`,sum(`s_display`.`Margin_profits_budget`) AS `SUM(Margin_profits_budget)`,sum(`s_display`.`Net_income_history`) AS `SUM(Net_income_history)`,sum(`s_display`.`Net_income_forecasting`) AS `SUM(Net_income_forecasting)`,sum(`s_display`.`Net_income_budget`) AS `SUM(Net_income_budget)` from `s_display` group by `s_display`.`h_Time`,`s_display`.`Model`,`s_display`.`Model_label`,`s_display`.`Series`;

-- ----------------------------
-- View structure for sales_price_india
-- ----------------------------
DROP VIEW IF EXISTS `sales_price_india`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sales_price_india` AS select `sales_price`.`id` AS `id`,`sales_price`.`Model` AS `Model`,`sales_price`.`Country` AS `Country`,`sales_price`.`h_Time` AS `h_Time`,`sales_price`.`Currency` AS `Currency`,`sales_price`.`Sales` AS `Sales`,`sales_price`.`Price` AS `Price`,`sales_price`.`Exchange_time` AS `Exchange_time` from `sales_price` where (`sales_price`.`Country` = 'India');

-- ----------------------------
-- View structure for sales_price_kenya
-- ----------------------------
DROP VIEW IF EXISTS `sales_price_kenya`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sales_price_kenya` AS select `sales_price`.`id` AS `id`,`sales_price`.`Model` AS `Model`,`sales_price`.`Country` AS `Country`,`sales_price`.`h_Time` AS `h_Time`,`sales_price`.`Currency` AS `Currency`,`sales_price`.`Sales` AS `Sales`,`sales_price`.`Price` AS `Price`,`sales_price`.`Exchange_time` AS `Exchange_time` from `sales_price` where (`sales_price`.`Country` = 'Kenya');

-- ----------------------------
-- View structure for sales_price_pakistan
-- ----------------------------
DROP VIEW IF EXISTS `sales_price_pakistan`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sales_price_pakistan` AS select `sales_price`.`id` AS `id`,`sales_price`.`Model` AS `Model`,`sales_price`.`Country` AS `Country`,`sales_price`.`h_Time` AS `h_Time`,`sales_price`.`Currency` AS `Currency`,`sales_price`.`Sales` AS `Sales`,`sales_price`.`Price` AS `Price`,`sales_price`.`Exchange_time` AS `Exchange_time` from `sales_price` where (`sales_price`.`Country` = 'Pakistan');

-- ----------------------------
-- View structure for sales_price_south_africa
-- ----------------------------
DROP VIEW IF EXISTS `sales_price_south_africa`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sales_price_south_africa` AS select `sales_price`.`id` AS `id`,`sales_price`.`Model` AS `Model`,`sales_price`.`Country` AS `Country`,`sales_price`.`h_Time` AS `h_Time`,`sales_price`.`Currency` AS `Currency`,`sales_price`.`Sales` AS `Sales`,`sales_price`.`Price` AS `Price`,`sales_price`.`Exchange_time` AS `Exchange_time` from `sales_price` where (`sales_price`.`Country` = 'South Africa');

-- ----------------------------
-- View structure for true_expenses
-- ----------------------------
DROP VIEW IF EXISTS `true_expenses`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `true_expenses` AS select `sales_price`.`id` AS `id`,round((`true_revenues`.`Costs` * (`ratio_expenses1`.`Software_product_amortization_rate_acc_cost` + `ratio_expenses1`.`RandD_rate_acc_cost`)),2) AS `RandD_expenses`,round((`true_revenues`.`Costs` * `ratio_expenses3`.`After_sales_provision_rate_acc_cost`),2) AS `After_sales_provision`,round((`true_revenues`.`Revenues` * `ratio_expenses2`.`Marketing_activities_provision_rate_acc_revenue`),2) AS `Marketing_provision`,`regional_expenses`.`Marketing_expenses` AS `Marketing_expenses`,`regional_expenses`.`Labor_cost` AS `Labor_cost`,`regional_expenses`.`Other_variable_expenses` AS `Other_variable_expenses`,`regional_expenses`.`Other_fixed_expenses` AS `Other_fixed_expenses`,round((`true_revenues`.`Costs` * `ratio_expenses2`.`Functional_cost_allocation_rate_acc_cost`),2) AS `Functional_expenses`,round((`true_revenues`.`Costs` * `ratio_expenses2`.`Business_group_headquarters_allocation_rate_acc_cost`),2) AS `Headquarters_expenses` from ((((((`sales_price` join `true_revenues`) join `ratio_expenses1`) join `ratio_expenses2`) join `ratio_expenses3`) join `regional_expenses`) join `model`) where ((`sales_price`.`id` = `true_revenues`.`id`) and (`sales_price`.`Model` = `model`.`Model`) and (`ratio_expenses1`.`Series` = `model`.`Series`) and (`ratio_expenses2`.`Country` = `sales_price`.`Country`) and (`regional_expenses`.`Country` = `sales_price`.`Country`) and (`ratio_expenses3`.`Model_label` = `model`.`Model_label`) and (`ratio_expenses3`.`Country` = `sales_price`.`Country`) and (`regional_expenses`.`Expenses_time` = `sales_price`.`h_Time`));

-- ----------------------------
-- View structure for true_margin_profits
-- ----------------------------
DROP VIEW IF EXISTS `true_margin_profits`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `true_margin_profits` AS select `sales_price`.`id` AS `id`,round(((((((`true_revenues`.`Gross_profits` - `true_expenses`.`RandD_expenses`) - `true_expenses`.`After_sales_provision`) - `true_expenses`.`Marketing_provision`) - `true_expenses`.`Marketing_expenses`) - `true_expenses`.`Labor_cost`) - `true_expenses`.`Other_variable_expenses`),2) AS `Margin_profits` from ((`sales_price` join `true_revenues`) join `true_expenses`) where ((`sales_price`.`id` = `true_revenues`.`id`) and (`sales_price`.`id` = `true_expenses`.`id`));

-- ----------------------------
-- View structure for true_net_income
-- ----------------------------
DROP VIEW IF EXISTS `true_net_income`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `true_net_income` AS select `sales_price`.`id` AS `id`,round((((`true_margin_profits`.`Margin_profits` - `true_expenses`.`Other_fixed_expenses`) - `true_expenses`.`Functional_expenses`) - `true_expenses`.`Headquarters_expenses`),2) AS `Net_income` from ((`sales_price` join `true_margin_profits`) join `true_expenses`) where ((`sales_price`.`id` = `true_margin_profits`.`id`) and (`sales_price`.`id` = `true_expenses`.`id`));

-- ----------------------------
-- View structure for true_price
-- ----------------------------
DROP VIEW IF EXISTS `true_price`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `true_price` AS select `sales_price`.`id` AS `id`,(case when (`sales_price`.`Currency` = 'USD') then (`sales_price`.`Price` * `exchange`.`Exchange_rate`) else `sales_price`.`Price` end) AS `true_Price` from (`sales_price` join `exchange`) where (`sales_price`.`Exchange_time` = `exchange`.`Exchange_time`);

-- ----------------------------
-- View structure for true_revenues
-- ----------------------------
DROP VIEW IF EXISTS `true_revenues`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `true_revenues` AS select `sales_price`.`id` AS `id`,round((`sales_price`.`Sales` * `true_price`.`true_Price`),2) AS `Revenues`,round((`sales_price`.`Sales` * `costs`.`Costs`),2) AS `Costs`,round(((`sales_price`.`Sales` * `true_price`.`true_Price`) - (`sales_price`.`Sales` * `costs`.`Costs`)),2) AS `Gross_profits` from ((`sales_price` join `costs`) join `true_price`) where ((`sales_price`.`Model` = `costs`.`Model`) and (`sales_price`.`Country` = `costs`.`Country`) and (`sales_price`.`h_Time` = `costs`.`Costs_time`) and (`sales_price`.`id` = `true_price`.`id`));

-- ----------------------------
-- Triggers structure for table ratio_expenses3
-- ----------------------------
DROP TRIGGER IF EXISTS `validate_model_label_insert`;
delimiter ;;
CREATE TRIGGER `validate_model_label_insert` BEFORE INSERT ON `ratio_expenses3` FOR EACH ROW BEGIN
    IF NOT EXISTS (SELECT 1 FROM Model WHERE Model_label = NEW.Model_label) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Model_label does not exist in Model table';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table ratio_expenses3
-- ----------------------------
DROP TRIGGER IF EXISTS `validate_model_label_update`;
delimiter ;;
CREATE TRIGGER `validate_model_label_update` BEFORE UPDATE ON `ratio_expenses3` FOR EACH ROW BEGIN
    IF NOT EXISTS (SELECT 1 FROM Model WHERE Model_label = NEW.Model_label) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Model_label does not exist in Model table';
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
