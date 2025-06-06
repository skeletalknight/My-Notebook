## Redis

### 概念

键值数据库使用简单灵活的**键值对**（key-value pairs）为基本的数据结构

键值对使用键唯一标识一个对象，这个对象可能包含多个字段内容，且不需遵守相同的格式

键值数据库往往采用内存储存，具有很快的读写速度，适合做中间层

缺点是键值数据库**不支持**基于值的查询，且需要单独存储数据之间的关系

键值数据库的代表有**Redis**、**Memcached**等

本文以Redis为例，介绍其基本操作

### 基本类型介绍

Redis 中的所有数据类型**都基于字符串实现**，数值作为字符串储存。

- **字符串**：最基础的类型，用于存储简单的文本或二进制数据，最大长度为 512 MB

- **字符串列表**：物理地址连续的字符串，元素允许重复，顺序不能变

- **集合**：无序的字符串集合，元素唯一，适合用于存储不重复的数据。支持多种集合操作，如求并集、交集和差集

- **有序集合**：与集合类似，但每个元素都有一个分数（score），用于排序。元素是唯一的，但可以通过分数值进行排序和范围查询

- **哈希**：用于存储键值对的集合，适合表示对象。每个哈希可以存储多个字段及其对应的值

- **位图**：允许对二进制位进行操作，用于高效存储和操作大量的二进制数据。支持位操作命令如 `SETBIT` 和 `GETBIT`

- **超日志**：用于统计唯一元素的数量，适合处理大规模数据集合，常用于分析和计数

- **地理空间**：允许存储地理位置（经纬度），支持范围查询和距离计算

  

### 基本操作

#### 字符串

| 命令       | 功能说明                                   | 语法                        | 备注                                              |
| ---------- | ------------------------------------------ | --------------------------- | ------------------------------------------------- |
| `SET`      | 设置 key 的值                              | `SET key value`             | 操作失败返回nil                                   |
| `GET`      | 获取 key 对应的值                          | `GET key`                   | 仅能处理Srting                                    |
| `DEL`      | 删除 key                                   | `DEL [key...]`              | 删除指定的键值                                    |
| `EXISTS`   | 检查 key 是否存在                          | `EXISTS key`                | 键不存在则返回 0                                  |
| `EXPIRE`   | 设置 key 过期时间                          | `EXPIRE key seconds`        | 设定键的生存时间，超时后将自动删除。              |
| `Strlen`   | 返回字符串长度                             | `StrLen key`                | 键不存在则返回0                                   |
| `Append`   | 将值追加在字符串末尾                       | `Append key value`          | 键不存在则创造                                    |
| `GETRANGE` | 获取字符串切片                             | `GETRANGE key start end`    | 负数偏移类似Python                                |
| `SETRANGE` | 用指定的字符串从偏移位置开始覆盖原有字符串 | `SETRANGE key offset value` |                                                   |
| `INCR`     | 将 key 的值加 1                            | `INCR key`                  | 用`INCRBY`加指定数<br />用`INCRBYFLOAT`操作浮点数 |
| `DECR`     | 将 key 的值减 1                            | `DECR key`                  | 用`DECRBY`减指定数                                |

**字符串列表**


| 命令       | 功能说明                     | 语法                     | 备注                             |
| ---------- | ---------------------------- | ------------------------ | -------------------------------- |
| `LPUSH`    | 将元素插入到列表的头部       | `LPUSH key value`        | 返回列表长度                     |
| `RPUSH`    | 将元素插入到列表的尾部       | `RPUSH key value`        | 返回列表长度                     |
| `LPOP`     | 移除并返回列表的第一个元素   | `LPOP key`               | 移除并返回列表的第一个元素。     |
| `RPOP`     | 移除并返回列表的最后一个元素 | `RPOP key`               | 移除并返回列表的最后一个元素。   |
| `LRange`   | 读取指定范围的元素           | `LRange key start stop`  | `stop`默认为最大下标             |
| `LIndex`   | 获取对应下标的元素           | `LIndex key index`       | 可以使用负索引                   |
| `LSet`     | 设置对应下标的元素           | `LIndex key index value` |                                

**集合**

| 命令          | 功能说明                       | 语法                      | 备注                               |
| ------------- | ------------------------------ | ------------------------- | ---------------------------------- |
| `SADD`        | 向集合添加元素                 | `SADD key [member...]`    | 返回添加的元素数量                 |
| `SREM`        | 从集合中移除元素               | `SREM key [member...]`    | 返回被移除的元素数量               |
| `SMEMBERS`    | 获取集合中的所有元素           | `SMEMBERS key`            | 返回集合中的所有成员               |
| `SISMEMBER`   | 检查元素是否在集合中           | `SISMEMBER key member`    | 返回 1 如果存在，否则返回 0        |
| `SCARD`       | 获取集合的成员数量             | `SCARD key`               | 返回集合中成员的数量               |
| `SINTER`      | 计算多个集合的交集             | `SINTER key1 key2 ...`    | 返回交集的成员                     |
| `SUNION`      | 计算多个集合的并集             | `SUNION key1 key2 ...`    | 返回并集的成员                     |
| `SDIFF`       | 计算多个集合的差集             | `SDIFF key1 key2 ...`     | 返回差集的成员                     |
| `SRANDMEMBER` | 随机返回集合中的一个或多个元素 | `SRANDMEMBER key [count]` | 如果指定 `count`，返回多个随机元素 |
| `SPOP`        | 移除并返回集合中的随机元素     | `SPOP key`                | 返回并移除集合中的一个随机元素     |

补充：Redis还存在有序集合的概念，其通过一个相关联的score进行排序

**哈希表**

哈希表内部存在独立的键值对，类似于字典

**哈希表操作命令**

| 命令           | 功能说明                       | 语法                               | 备注                                       |
| -------------- | ------------------------------ | ---------------------------------- | ------------------------------------------ |
| `HSET`         | 设置哈希表中的字段值           | `HSET key [field value..]`         | 返回 1 如果字段是新建的，返回 0 如果更新   |
| `HGET`         | 获取哈希表中指定字段的值       | `HGET key [field...]`              | 返回指定字段的值                           |
| `HDEL`         | 删除哈希表中的指定字段         | `HDEL key [field...]`              | 返回被删除字段的数量                       |
| `HLEN`         | 获取哈希表中的字段数量         | `HLEN key`                         | 返回哈希表中字段的数量                     |
| `HKEYS`        | 获取哈希表中所有字段的名称     | `HKEYS key`                        | 返回哈希表中所有字段的名称                 |
| `HVALS`        | 获取哈希表中所有字段的值       | `HVALS key`                        | 返回哈希表中所有字段的值                   |
| `HGETALL`      | 获取哈希表中的所有字段及其值   | `HGETALL key`                      | 返回哈希表中所有字段及其值                 |
| `HINCRBY`      | 将指定字段的值增加指定的整数   | `HINCRBY key field increment`      | 返回增加后的值                             |
| `HEXISTS` | 检查哈希表中指定字段是否存在 | `HEXISTS key field`     | 返回 1 如果字段存在，否则返回 0                             |
| `HSETNX`       | 仅在字段不存在时设置字段值     | `HSETNX key field value`           | 返回 1 如果字段是新建的，返回 0 如果已存在 |