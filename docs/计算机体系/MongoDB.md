## MongoDB概览

### 简介与特点

MongoDB是由C++语言编写的，是一个基于分布式文件存储的开源文档数据库系统。

MongoDB采用JSON格式进行文档数据存储。这种数据格式是不规则的，同时具有“自包含”，“半结构化”的特点。

MongoDB具有以下特点：

- 提供了一个面向文档存储，操作简易，同时支持批量处理和聚合操作

- 具有较好的水平可扩展性
- 支持丰富的查询表达式，可轻易查询文档中内嵌的对象及数组
- 可以实现替换完成的文档（数据）或者一些指定的数据字段

- 支持RUBY，PYTHON，JAVA等各种编程语言

### 术语

| SQL术语/概念 | MongoDB对应术语         | 解释说明                               |
| ------------ | ----------------------- | -------------------------------------- |
| database     | database                | 数据库                                 |
| table        | collection              | 集合                                   |
| row          | document                | 文档                                   |
| column       | field                   | 字段                                   |
| index        | index                   | 索引                                   |
| table joins  | 无                      | MongoDB不支持文档连接，但可以实现嵌入  |
| primary key  | primary key/document id | 主键，MongoDB自动将 _id 字段设置为主键 |

需要注意的是，集合没有固定的结构，其中的数据键并不强制要求一致。

同时，对于执行语句，MongoDB需要使用特定的操作符，列举如下

| 操作符         | 作用                             | 示例                                                         |
| -------------- | -------------------------------- | ------------------------------------------------------------ |
| `$inc`         | 增加指定字段的值                 | `db.users.updateOne({ _id: 1 }, { $inc: { age: 2 } })`       |
| `$set`         | 设置指定字段的值                 | `db.users.updateOne({ _id: 1 }, { $set: { name: "Alice" } })` |
| `$unset`       | 删除指定字段                     | `db.users.updateOne({ _id: 1 }, { $unset: { address: "" } })` |
| `$push`        | 向数组字段中添加一个值           | `db.users.updateOne({ _id: 1 }, { $push: { ho: "reading" } })` |
| `$pull`        | 从数组中移除指定值               | `db.users.updateOne({ _id: 1 }, { $pull: { ho: "reading" } })` |
| `$addToSet`    | 向数组中添加值，但不会添加重复值 | `db.items.updateOne({ _id: 1 }, { $addToSet: { tags: "new" } })` |
| `$pop`         | 从数组中移除第一个或最后一个元素 | `db.users.updateOne({ _id: 1 }, { $pop: { hobbies: 1 } })`   |
| `$rename`      | 重命名字段                       | `db.users.updateOne({ _id: 1 }, { $rename: { fullname: "name" } })` |
| `$min`         | 只在新值比当前值小时更新字段     | `db.users.updateOne({ _id: 1 }, { $min: { score: 50 } })`    |
| `$max`         | 只在新值比当前值大时更新字段     | `db.users.updateOne({ _id: 1 }, { $max: { score: 90 } })`    |
| `$currentDate` | 将字段设置为当前日期             | `db.users.updateOne({ _id: 1 }, { $currentDate: { lastUpdated: true } })` |
| `$eq`          | 匹配等于指定值的文档             | `db.users.find({ age: { $eq: 25 } })`                        |
| `$in`          | 匹配字段值在指定数组中的文档     | `db.users.find({ status: { $in: ["active", "pending"] } })`  |
| `$nin`         | 匹配字段值不在指定数组中的文档   | `db.users.find({ status: { $nin: ["active", "pending"] } })` |
| `$regex`       | 使用正则表达式匹配字段值         | `db.users.find({ name: { $regex: "John", $options: "i" } })` |



## 数据库操作语句

MongoDB中函数使用前常有`db.`，代表当前连接的数据库

- `use 数据库名`：如果不存在，创建新数据库；否则进行连接
- `db.getCollectionNames()`：获取数据库中的集合
- `db.dropDatabase()`：删除当前连接的数据库

操作集合，需要使用`db.<collection_name>.`加对应函数，下面使用`<co>`代替该前缀

- `<co>.insertOne() / insertMany() /`：插入单个/多个文档  

- `<co>.updateOne() / updateMany()`：

	- 用于更新单个/多个文档，语法如`<update>(<query>,<update>)`

		```js
		 //在 inventory 集合上更新第一个 item 等于 "paper" 的文档
		await db.collection('inventory').updateOne(
		  { item: 'paper' },
		  { //使用 $set 操作符将 size.uom 字段的值更新为 "cm"，并将 status 字段的值更新为 "P"
		    $set: { 'size.uom': 'cm', status: 'P' },
		    //使用 $currentDate 操作符将 lastModified 字段的值更新为当前日期。如果 lastModified 字段不存在
		    $currentDate: { lastModified: true } 
		  }
		);
		```

- `<co>.deleteOne() / deleteMany()`：删除单个/多个文档（对于后者，匹配所有符合的）

- `<co>.replaceOne()`：替换文档，直接输入并列的两个文档，不需要更新操作符

查询语句使用`find`

- `<co>.find(query, projection)`:
	- 直接使用如`find({status:"D", qty:{$lt:30} })`即可进行并列查询
	- 对于同一字段，使用`find({status: {$in:['A','D']}`进行或运算
	- 对于不同条件，使用`find({ $or: [ {status:"A"},{ qty:{$lt:30} } ] }`进行或查询
	- 类似`$lt`表示小于，还有`$eq, $ne, $gt, $gte, $lte`等
	- 使用`$and: []`进行与查询，`$not:{}`进行非查询
	- 使用`$regex:..`进行正则查询，可以和`$option`合用
	- 使用`"size.m"`对嵌套字段进行查询，嵌套数组类同正常查询
	- 匹配数组若不讲究顺序和其他元素，使用`find({ tg: {$all : ['a','b'] }})`
	- 查询语句最终为文档形式
- 结果投影`projection`：
	- 方法一，明确包含字段，如`find({status:”D”}, {item:1, qty:1})`
	- 方法二，明确排除字段，如`find({status:”D”}, {size:0, status:0})`
	- 使用`{item:1, list:{$slice:-1}}`可以指定返回数组元素

聚合操作

```javascript
db.collectionName.aggregate(
    [{$match:{<field>}},
     {$group:{<field1>,<field2>}}])
```

- $match: 统计查找条件，与find()的查找条件使用方法一样

- $group: field1为分类字段；field2为含各种统计操作符的数值型字段

- 聚合操作符有`$sum,$avg,$min,$max,$addToSet,$first,$last`













