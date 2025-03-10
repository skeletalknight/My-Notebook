# SQL标准

结构化查询语言 (Structured Query Language, **SQL**) 是最常用的数据库语言

它是由标准英文单词组成的非过程语言，只关心关系的转化

SQL中的非数值常量需要使用单引号包裹，数值常量则不使用

标准的SQL书写采用<u>巴克斯范式</u>（BNF notation）：

- 大写字母用于表示保留字，必须准确拼写；小写字母用户表示用户自定义字

- 竖线`|`表示从选项中选择，如 `a|b|c` 代表从a，b，c中选择一个

- 大括号 `{} `代表必须元素，中括号` [] `代表可选元素（非必须元素）

- 省略号 `… `代表某一个元素可选择重复零到多次

- 注释使用`--`进行单行注释，`/*..*/`

## 数据库操作

### SELECT关键词

```sql
SELECT [DISTINCT | ALL]
	 {* | [columnExpression [AS newName]] [,...] } 
FROM	TableName [alias] [, ...] 
[WHERE 	condition]
[GROUP BY columnList] [HAVING condition]
[ORDER BY columnList]
```

- `DISTINCT`：去除重复元组
- `*`：选取所有列
- `AS`：为列/表取别名，也可以在`FROM`语句使用，同时全查询语句引用，`FROM`中可省略
- `TOP N (PERCENT)`：限定查询数量/行数
- `LIMIT <M> OFFSET <N>`：进行分页展示，M为页大小，N为起始数据索引
- **字段计算**：选取时直接对column加入`+-*/`等运算，但需要指定别名

### WHERE关键词

- 可以进行逻辑运算，注意`=`为等于，`<>`为不等于
- 逻辑关键词使用`NOT, AND, OR`，顺序从左到右，有优先级，建议使用括号
- `BETWEEN A AND B`：规定查找范围，含端点，相当于逻辑运算整合
- `IN ('...', '...')`：判断选取集合成员
- `IS NULL`：匹配空值
- `LIKE`-模式匹配：
	- `%`：表示零或者多个字符序列（通配符）
	- `_`：表示任意单个字符
	- `ESCAPE`：用于定义逃离符，如`#`，来匹配特殊符号，例如`‘15%’:LIKE ‘15#%’ ESCAPE‘#’`

### ORDER BY关键词

- 由于选取的乱序性，使用`ORDER BY`进行排序
- `col ASC/DESC`：根据某列进行升序/降序排列
- `col1, col2`：从前往后主要性逐渐下降，同时需要**各自**指定排列方式

### GROUP BY关键词

往往与聚集函数一起出现，用于分组计算

使用`WHERE`对行筛选，使用`HAVING`对组筛选

用例：

```sql
SELECT branchNo,
 COUNT(staffNo)AS myCount,
 SUM(salary)AS mySum
 FROM Staff
 GROUP BY branchNo
 HAVING COUNT(staffNo) > 1
 ORDER BY branchNo;
```

### 聚集函数

ISO标准定义了五个聚集函数：`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`

聚集函数只能对表中的单个列进行操作，返回单一值

注意，聚集函数**不能**用于WHERE子句

除了**COUNT(*)**以外，其他每个函数都首先忽略空值（NULL），然后进行计算（前者会计算总行数)

用例：

```sql
SELECT COUNT(staffNo)AS myCount,
 SUM(salary) AS mySum
 FROM Staff
 WHERE position = ‘Manager’;
```

### 子查询

子查询语句包含于（）中，且需要再表达式右侧

依据结果有以下分类

- 标量子查询：往往用于相等判断，子查询内还可以使用聚集函数

- 列子查询：

	- 同属性的多个值，常用于`IN`做归属判断

	- 判断符+`ALL/ANY`能与数字类型的列子查询一起使用
		`ALL`需要所有值都满足判断，而`ANY`只需要一个值满足

	- 使用`(NOT) EXISTS`对表内每行进行子查询判断，，返回是否为空

		```sql
		SELECT SupplierName
		 FROM Suppliers
		 WHERE EXISTS (SELECT * FROM Products
		 WHERE Products.SupplierID = 
		Suppliers.supplierID AND Price < 20);
		```

### 多表连接查询

有时需要将多个表的列合并在一个结果表，这需要连接操作

#### 内连接

内连接会使得表中不能按照连接条件匹配的行会被筛除

```sql
SELECT c.clientNo, fName
 FROM Client c, Viewing v
 WHERE c.clientNo = v.clientNo;
```

以上实现了内连接，其中可以使用

```sql
FROM Client c JOIN Viewing v ON c.clientNo = v.clientNo
```

来替代后面的`FROM`+`WHERE`子句

#### 外连接

如果需要保留不满足连接条件的行，可以使用外连接，如

```sql
SELECT b.*, p.*
 FROM Branch b LEFT JOIN Property p ON b.bCity = p.pCity;
```

则会在表b的基础上补充连接，p表无对应的值会填充`NULL`

全外连接使用`FULL JOIN`关键词

### 集合操作

使用`UNION`、`INTERSECT`、`EXCEPT`进行并、交、差操作

进行集合操作的表需要有并相容性

使用`CORRESPONDING BY`使得操作在指定列执行，无指定则自动寻找相同列

使用`ALL`来让结果包括重复行

```sql
operator [ALL] [CORRESPONDING [BY{column1 [, ...]}]]
-- 基础语法
 (SELECT *
 FROM Branch)
 UNION CORRESPONDING BY city -- 或者都改为SELECT city
 (SELECT *
 FROM PropertyForRent);
```



### 数据修改操作

- `INSERT`：

	- 作用：对表插入数据

	- 基础语法：

		```sql
		INSERT INTO TableName [ (columnList) ]
		 VALUES(dataValueList)
		```

		其中数据和列必须对应

	- 插入列名可以忽略。如果忽略，SQL会严格按照表格创建时的顺序执行插入

	- 使用`SELECT`将其他表的内容插入另一个表

- `UPDATE`：

	- 作用：更新表的内容

	- 基础语法：

		```sql
		UPDATE TableName
		 SET columnName1 = dataValue1 [, columnName2 = dataValue2...]
		 [WHERE searchCondition]
		```

	- 使用表达式对选取的列的数据进行操作

	- 使用列名进行统一操作，如`salary=salary*1.2`

- `DELETE`：

	- 作用：删除表的数据

	- 基础语法：

		```sql
		 DELETE FROM TableName
		 [WHERE searchCondition]
		```

	- 若省略`WHERE`，则所有行会被删除

## 数据库定义

### 数据类型

- 整数型：bit, tinyint, smallint, int ,bigint
- 浮点型：float, money
- 日期：smalldatetime, datetime（8字节）
- 字符串型：char(m), varchar(m)【前缀n为使用unicode】

### 完整性控制机制

- `NOT NULL`：表示列属性非空

- 域约束：

	- `CHECK+(判断表达式)`：约束列的域需要满足判断表达式

	- `CREATE DOMAIN`：定义域型，再在定义列时引用

		```sql
		CREATE DOMAIN SexType AS CHAR
		 DEFAULT ‘M’
		 CHECK (VALUE IN (‘M’, ‘F’));
		 sex SexType NOTNULL
		```

- 实体完整性：使用`PRIMARY KEY`设定主码，或使用`UNIQUE`保证集合不重复

- 引用完整性：

	- 含义：保证外码的有效性
	- 定义外码：`FOREIGN KEY(branchNo) REFERENCES Branch`
	- 作用：当更新子表时，如果创建不匹配的值会拒绝操作；若更新母表，按预设定执行
	- 预设定：
		- `CASCADE`：依次自动更新/删除子表中匹配的行。 
		- `SET NULL`：设置子表中的外码值为NULL。
		- `SET DEFAULT`：设置子表中的外码值为默认值，需要外码指定过默认值
		- `NO ACTION`：拒绝对母表进行更新操作（默认设置）

	注：由于外键约束会降低数据库的性能，大部分互联网应用程序为了追求速度，并不设置外键约束。

- 一般性约束：在构建表时，使用`CONSTRAINT`和`CHECK+(判断表达式)`保证其满足一般约束，如：

	```sql
	CONSTRAINT StaffNotHandlingTooMuch
	 CHECK (NOT EXISTS (SELECT staffNo
	 FROM PropertyForRent
	 GROUPBY staffNo
	 HAVING COUNT(*) > 100))
	```

### 定义操作

使用`CREATE`创建，`DROP`删除，`ALTER`修改

可用对象有`SCHEMA`, `DOMAIN`, `TABLE`, `VIEW`

创建表前可以先创建域型

以修改为例，可以看出数据库操作的基本类型

```sql
ALTER TABLE table_name
 [ADD [COLUMN] column_name dataType [NOT NULL] [UNIQUE]
 [DEFAULT defaultOption] [CHECK (searchCondition)]
 [DROP [COLUMN] column_name [RESTRICT|CASCADE]]
 [ADD [CONSTRAINT [ConstraintName]] TableConstraintDeifnition]
 [DROP CONSTRAINT ConstraintName [RESTRICT|CASCADE]]
 [ALTER [COLUMN] SET DEFAULT defaultOption]
 [ALTER [COLUMN] DROP DEFAULT]
```

以下记录一些常见操作

- 添加索引，提高列查询速度

	```sql
	ALTER TABLE students
	ADD [UNIQUE] INDEX idx_name_score (name, score);
	```



### 数据库权限

#### 虚关系

可以通过查询来定义“虚关系”，它在概念上包含查询的结果，在使用时再进行执行（类似Define)

通过虚关系可以限制不同用户对数据库的可视范围

这种虚关系在编程实践被称为视图（**View**），其常用操作如下

```sql
CREATE VIEW view_name [(col_name...)] AS <query expression> -- 任何合法查询表达式
DROP VIEW viewName [RESTRICT | CASCADE] -- 后者会递归删除依赖该视图的对象
```

对于频繁查询的视图，也可以进行物化固定，减少查询时间

#### 用户权限

可以限制用户在读取、插入、更新、删除等方面的权限。最大的权限为数据管理员（DBA）

使用`GRANT`进行授权，`REVOKE`回收授权，其语法如下

```sql
GRANT {权限列表|ALLPRIVILEGES} -- 如SELECT等
ON 关系名或视图名
TO{用户/角色列表|PUBLIC} -- 后者是授权所有当前和未来的用户
[WITH GRANT OPTION] -- 是否具有迭代授权的权利

REVOKE [GRANT OPTION FOR] -- 可选，如果指明则只撤销该用户传递授权的权限
{权限列表|ALL PRIVILEGES}
 ON 关系名或视图名
FROM {用户/角色列表|PUBLIC}
 [RESTRICT | CASCADE] --  如果权限的授予时有WITH GRANT OPTION，回收该权限时必须使用CASCADE选项
```



