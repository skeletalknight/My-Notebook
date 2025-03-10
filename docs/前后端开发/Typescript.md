## Typescript

### 概述

TypeScript（简称 TS）是微软公司开发的一种基于 JavaScript （简称 JS）语言的编程语言

TS是JS的超集，在兼容JS的基础上，他完善了JS<u>类型系统</u>，并增加了许多特性

使用TS，可以使用**`tsc`** 编译生成`.js`文件，使用**`tsx`** 热加载并运行TS文件



### 类型系统

#### 类型的意义

类型是人为添加的一种编程约束和用法提示，它能

- 帮助开发者进行错误排查，尽早发现错误
- 完善函数的定义，提示开发者如何使用
- 利于发挥IDE提示、补全、纠错功能

JS的变量是<u>动态类型</u>，变量的类型、属性缺乏约束

TS引入了<u>静态类型</u>，他需要额外的工作量去编写类型声明，但更加规范、稳定

TS可能会丧失灵活性，增加工作量，这使得他不一定适合短期、小型的项目

但是由于纠错、重构、合作的巨大改进，大多情况下TS是值得的，特别是大型项目

#### 类型声明

```typescript
let foo:string;  //在变量后使用冒号进行类型声明
let num = 123;  //未进行声明时会自动进行类型判断

function toString(num:number||null):string {  //函数的类型声明
  return String(num);						//使用联合类型
}

let s:unknown = 'hello';  //使用unknow的顶层类型，需要在判断后进行调用
if (typeof s === 'string') {
  s.length; // 正确
}

let rep = requst() as Response //强制确定类型
```

对于复用的类型，可以用`type`进行声明

#### 类型判断

未进行声明的变量，编译器会自动推断变量类型

如果无法推断，他会将变量标记为**`any`**，他是所有类型的全集！（同时会污染正常的变量）

如果不想被推断为**`any`**，可以开启`noImplicitAny`编译选项



### 基础类型

#### 原始类型

- boolean
- string
- number
- bigint
- symbol

上面这五种原始类型的值，都有对应的**包装对象**（wrapper object）

包装对象，指的是这些值在需要时，会自动产生的对象。

```javascript
const s = new String('hello');
typeof s // 'object'
s.charAt(1) // 'e'
```

#### 对象类型

小写的`object`类型代表 JavaScript 里面的狭义对象，即对象、数组和函数

```javascript
obj = { foo: 123 };
const {val:foo} = obj; //解构赋值用于直接从对象中提取属性。
let { x: foo, y: bar }
  : { x: string; y: number } = obj; //指定x,y类型
```

#### 函数类型

`(  ) => (  )`是函数的标识

```typescript
const repeat = (
  str:string="",		//可以使用默认值
  times?:number			//使用？表示可选
):string => str.repeat(times);  //():表示返回值

function sum(
  { a, b, c }: {
     a: number;
     b: number;
     c: number			//变量解构/对象类型
  }						//避免冲突，故typescript对象的类型声明另起
) {console.log(a + b + c);}
```

