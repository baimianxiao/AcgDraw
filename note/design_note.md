# AcgDraw 设计文档

## 功能设计

### 功能概述

基于目前已有功能进行进一步改良升级，实现更多功能。大致分为以下几个部分：

- [ ] 管理面板
- [ ] 接口格式优化
- [ ] 添加抽卡保底机制（基于数据库）
- [ ] 优化抽卡算法
- [ ] 自定义结果图片合成
- [ ] 抽卡记录查询

### 接口设计

#### 1. 抽卡(json格式结果)

- **api方法：**

```
POST /api/draw/json
```

- **请求头：**

| 参数名           | 值                | 备注       |
|---------------|------------------|----------|
| Authorization | Bearer <token>   | 用于验证用户身份 |
| Content-Type  | application/json | 请求体格式    |

- **请求体：**

| 参数名         | 类型     | 是否必填 | 描述                                      | 备注                 |
|-------------|--------|------|-----------------------------------------|--------------------|
| uid         | string | 否    | 抽卡用户uid,用于记录抽卡记录和保底计算，若未提供则不记录抽卡记录和保底计算 | 需要api提供方开放相关功能后才可用 |
| game        | string | 是    | 游戏名称                                    |                    |
| draw_mode   | string | 是    | 抽卡模式                                    | "single"或"ten"     |
| result_list | list   | 否    | 是否需要返回图片URL                             |                    |

- **响应头：**

| 参数名          | 值                | 备注    |
|--------------|------------------|-------|
| Content-Type | application/json | 响应体格式 |

- **响应体：**

| 参数名  | 类型     | 描述     | 备注           |
|------|--------|--------|--------------|
| code | int    | 错误码    | 0表示成功，非0表示失败 |
| msg  | string | 错误信息   |              |
| data | object | 抽卡结果数据 |              |

- **响应体中的data字段：**

| 参数名     | 类型     | 描述                                      | 备注                 |
|---------|--------|-----------------------------------------|--------------------|
| uid     | string | 抽卡用户uid,用于记录抽卡记录和保底计算，若未提供则不记录抽卡记录和保底计算 | 需要api提供方开放相关功能后才可用 |
| game    | string | 游戏名称                                    |                    |
| mode    | string | 抽卡模式                                    | "single"或"ten"     |
| result  | array  | 抽卡结果                                    |                    |
| img_url | string | 抽卡结果图片URL                               | 仅当need_url为true时返回 |

- **例子：**

```
POST /api/draw/json
Authorization: Bearer {token}

请求体:
{
    "uid": "",
    "game":"Arknights",
    "draw_mode": "single",
    "need_url": true
}

成功响应（200）:
{
    "code": 0,
    "msg": "",
    "data": {
        "uid": "",
        "game": "Arknights",
        "mode": "single",
        "record_id": "",
        "result": [
            {
                "name": "白面鸮",
                "rarity": "5",
                "type":"医疗"
            }
        ]
        "img_url": "http://example.com/result.png"
    }
}
```

- **失败情况：**
    - 400 Bad Request：请求体格式错误
    - 401 Unauthorized：未提供token或token无效
    - 404 Not Found：未找到指定的游戏或抽卡模式
    - 500 Internal Server Error：服务器内部错误

#### 2. 抽卡(流式图片格式结果)

- **api方法：**

```
POST /api/draw/img
```

- **请求头：**

| 参数名           | 值                | 备注       |
|---------------|------------------|----------|
| Authorization | Bearer <token>   | 用于验证用户身份 |
| Content-Type  | application/json | 请求体格式    |

- **请求体：**

| 参数名       | 类型     | 是否必填 | 描述                                      | 备注                 |
|-----------|--------|------|-----------------------------------------|--------------------|
| uid       | string | 否    | 抽卡用户uid,用于记录抽卡记录和保底计算，若未提供则不记录抽卡记录和保底计算 | 需要api提供方开放相关功能后才可用 |
| game      | string | 是    | 游戏名称                                    |                    |
| draw_mode | string | 是    | 抽卡模式                                    | "single"或"ten"     |

- **响应头：**
-

| 参数名          | 值         | 备注    |
|--------------|-----------|-------|
| Content-Type | image/png | 响应体格式 |

- **响应体：**

抽卡结果图片

- **例子：**

```
POST /api/draw/img
Authorization: Bearer {token}

请求体:
{
    "uid": "",
    "game":"Arknights",
    "mode": "single"
}   
成功响应（200）:
抽卡结果图片
```

- **失败情况：**
    - 400 Bad Request：请求体格式错误
    - 401 Unauthorized：未提供token或token无效
    - 404 Not Found：未找到指定的游戏或抽卡模式

##### 3. 抽卡记录查询

- **api方法：**

```
POST /api/record/query
```

- **说明：**

查询抽卡记录，支持分页查询和按条件查询。

- **请求头：**

| 参数名           | 值                | 备注       |
|---------------|------------------|----------|
| Authorization | Bearer <token>   | 用于验证用户身份 |
| Content-Type  | application/json | 请求体格式    |

- **请求体：**

| 参数名       | 类型     | 是否必填                 | 描述      | 备注                        |
|-----------|--------|----------------------|---------|---------------------------|
| uid       | string | 是                    | 抽卡用户uid |                           |
| type      | string | 是                    | 查询类型    | "uid","record_id"         |
| record_id | string | 在type为"record_id"时必填 |         | 抽卡记录id                    |             |
| game      | string | 是                    | 游戏名称    |                           |
| page_num  | int    | 否，在type为"uid"时必填     | 页码      |                           |
| page_size | int    | 否                    | 每页记录数   | 在type为"uid"时默认为10，最大值为100 |

- **响应头：**

| 参数名          | 值                | 备注    |
|--------------|------------------|-------|
| Content-Type | application/json | 响应体格式 |

- **响应体：**

| 参数名       | 类型     | 描述     | 备注                    |
|-----------|--------|--------|-----------------------|
| code      | int    | 错误码    | 0表示成功，非0表示失败          |
| msg       | string | 错误信息   |                       |
| page_num  | int    | 当前页码   | 仅在type为"uid"时返回       |
| has_next  | bool   | 是否有下一页 | 仅在type为"uid"时返回       |
| record_id | string | 抽卡记录id | 仅在type为"record_id"时返回 |
| data      | object | 抽卡结果数据 |                       |

- **响应体中的data字段：**

| 参数名         | 类型     | 描述       | 备注 |
|-------------|--------|----------|----|
| uid         | string | 抽卡用户uid  |    |
| record_list | list   | 抽卡记录列表   |    |
| count       | int    | 本次查询的记录数 |    |

- **响应体中的data.record_list字段：**

| 参数名       | 类型     | 描述         | 备注         |
|-----------|--------|------------|------------|
| name      | string | 名称         |            |
| rarity    | string | 稀有度        |            |
| type      | string | 类型(职业/神之眼) |            |
| record_id | string | 所属抽卡记录id   |            |
| mode      | string | 抽卡时使用的模式   | single/ten |
| timestamp | int    | 记录创建时间戳    | 秒级时间戳      |

- **例子：**

```
POST /api/record/query
Authorization: Bearer {token}

请求体:
{
    "uid": "114514",
    "type": "uid",
    "game": "Arknights",
    "page_num": 1,
    "page_size": 10
}

成功响应（200）:
{
    "code": 0,
    "msg": "",
    "page_num": 1,
    "has_next": false,
    "data": {
        "uid": "114514",
        "record_list": [
            {
                "name": "白面鸮",
                "rarity": "5",
                "type": "医疗",
                "record_id": "36888",
                "mode": "single",
                "timestamp": 1145141919
            }
        ],
        "count": 1
    }
}
```

- **失败情况：**
    - 400 Bad Request：请求体格式错误
    - 401 Unauthorized：未提供token或token无效
    - 404 Not Found：未找到符合条件的抽卡记录

##### 4. 由文本生成图片

- **api方法：**

```
POST /api/text2img
```

- **请求头：**

| 参数名           | 值                | 备注       |
|---------------|------------------|----------|
| Authorization | Bearer <token>   | 用于验证用户身份 |
| Content-Type  | application/json | 请求体格式    |

- **请求体：**

| 参数名  | 类型     | 是否必填 | 描述     | 备注 |
|------|--------|------|--------|----|
| game | string | 是    | 游戏名称   |    |
| data | list   | 是    | 抽卡结果数据 |    |

- **请求体中的data字段的元素：**

// TODO: 等一个好心人来补充

- **响应头：**

| 参数名          | 值         | 备注    |
|--------------|-----------|-------|
| Content-Type | image/png | 响应体格式 |

- **响应体：**
  抽卡结果图片
- **例子：**

// TODO: 等一个好心人来补充

#### 全局错误码

| 错误码 | 错误信息   | 备注               |
|-----|--------|------------------|
| 0   | 成功     |                  |
| 400 | 无效的请求体 |                  |
| 401 | 未授权的请求 | 未提供token或token无效 |
| 403 | 禁止的请求  | 当前用户无权访问         |
| 404 | 未找到资源  |                  |
| 500 | 服务器错误  |                  |

### 抽卡生成设计

抽卡结果生成部分涉及的程序位于`AcgDraw/draw`

抽卡类必须继承父类DrawHandle，并且必须实现`char_once_pull`,`char_ten_pulls`两个方法

命名规则:DrawHandle+游戏标志

例如:DrawHandleArk(明日方舟),DrawHandleGen(原神)

抽卡类中`char_ten_pulls`输出类型为list，其中包含以下字段：

```
[
  {
    "name":"人物名",
    “rarity”:"稀有度",
    "type":"职业",
  },
  {
    "name":"人物名",
    “rarity”:"稀有度",
    "type":"职业",
  },
  ……
  {
    "name":"人物名",
    “rarity”:"稀有度",
    "type":"职业",
  }
]
```

抽卡图片合成部分涉及的程序位于`AcgDraw/image`

### 数据记录

数据储存位置位于`根目录/data/游戏名`

数据格式为

- image 图片合成素材储存目录

内部结构根据游戏合成模式自定

- data_dict.json 人物数据储存

  ```
  {
      "char_data_dict": {
          "狮蝎": {
            "name": "狮蝎", 
            "type": "特种",
            "rarity": 5,
          },
      }，
      "weapon_data_dict":{
          "胡桃": {
            "rarity": 5,
            "element": "火"
          }
      },
  } 
  ```  
  // 待确定

  rarity_dict.json 稀有度数据记录

  ```
  {
    "char_list": {
      "6": [
        "锏",
        "老鲤",
        ……
        "Mon3tr"
      ],
      "3": [
        "芬",
        "炎熔",
        ……
        "安赛尔"
      ]
    },
    "weapons_list":{
    
    }
  }
  ```

### 添加新的游戏抽卡步骤

1.在`AcgDraw/draw`中创建对应游戏的抽卡结果生成器
  
  - 在文件头导入`from AcgDraw.draw import *`

  - 创建抽卡结果合成器类,并且继承抽象类`DrawHandle`

  - super.__init__(游戏标识名)
  
  - 实现`char_once_pull`,`char_ten_pulls`两个方法

2.在`AcgDraw/image`中创建对应游戏的抽卡的图片合成器(非必要)

3.在`AcgDraw/__init__.py`中引入对应的抽卡结果生成器和图片合成器

4.在`AcgDraw/api.py`中实现接口

### 数据库设计

- **抽卡请求记录表（记录单次抽卡操作）**

```sql
CREATE TABLE gacha_records
(
    record_id   VARCHAR(36) PRIMARY KEY COMMENT '唯一记录ID',
    uid         VARCHAR(64) NOT NULL COMMENT '用户UID',
    game        VARCHAR(50) NOT NULL COMMENT '游戏名称',
    gacha_mode  ENUM('single', 'ten') NOT NULL COMMENT '抽卡模式',
    gacha_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '抽卡时间',
    gacha_count INT UNSIGNED NOT NULL COMMENT '累计抽卡数',
    INDEX       idx_user (uid, game)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

- **抽卡结果明细表（记录每次抽卡的具体结果）**

```sql
CREATE TABLE gacha_items
(
    item_id   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '物品记录ID',
    record_id VARCHAR(36)  NOT NULL COMMENT '关联记录ID',
    item_name VARCHAR(100) NOT NULL COMMENT '物品名称',
    rarity    TINYINT UNSIGNED NOT NULL COMMENT '稀有度等级',
    item_type VARCHAR(50)  NOT NULL COMMENT '物品类型/职业',
    FOREIGN KEY (record_id) REFERENCES gacha_records (record_id) ON DELETE CASCADE,
    INDEX     idx_rarity (rarity),
    INDEX     idx_record (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 管理面板设计

// TODO: 等一个好心人来补充

## 其他杂项TODO

- [ ] 完善用户手册
- [ ] 完善日志系统
- [ ] 完善错误处理系统