# Class and Template

## 类与封装

我们希望能定义一类对象，它包含了数据结构、常用方法，以便我们进行复用——这就是类

引入类后，我们可以方便地自定义对象，并围绕它的设计、应用展开工作——即面向对象编程的核心思想

### 类的定义

一个好的类定义习惯，是在头文件内定义类的接口，而在另一个cpp文件中给出具体实现

头文件案例：

```cpp
class StanfordID {
private:	//private下定义了访问受限的变量和函数（需要通过类内接口访问）
    std::string name;
    std::string sunet;
    int idNumber;
public:
    StanfordID(std::string name, std::string sunet, int idNumber); //定义了类的声明
    std::string getName();	
    std::string getSunet();
    int getID();
}
```

实现案例：

注意，我们在实现前加上了`StanfordID::`来表明它是类的函数

```cpp
//类的声明：
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    this->name = name;	//直接使用name是可以的，但为了表明这是类内的元素，更推荐使用this指针
    this->sunet = sunet;
    if ( idNumber > 0 ) this->idNumber = idNumber;
}
//C++11引入的新特性——直接使用`: attribute{value}`
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber): 
    name{name}, sunet{sunet}, idNumber{idNumber} {};
//不传参时的默认初始化——自动匹配符合的参数格式的函数
StanfordID::StanfordID() {
    name = "john";
    sunet = "jappleseed";
    idNumber = 1;}
```

### 常量验证

当我们声明一个**常量类**时，编译器需要知道其类函数是否会修改类的内容，否则会拒绝使用。

因此，我们需要在不修改类内容的函数后面加入`const`，来提示编译器。此时，传入函数内的类指针为`const class *`

同时，即使使用了`const`提示，当`const`成员函数返回了**非const的引用**时，仍存在值被修改的风险，而编译器无法检测。

因此，当`const`成员函数返回引用时，我们需要在前面加入`const`，防止引用被修改。此外，为了保证非常量类的能正常返回可修改的引用，我们还需要重载一个非`const`成员函数。

| 返回类型                         | 非常量对象   | 常量对象                                                     |
| -------------------------------- | ------------ | ------------------------------------------------------------ |
| 副本或者新构建的值               | 正常成员函数 | `const`成员函数                                              |
| 对象内部数据的 **引用或指针** 时 | 正常成员函数 | `const`成员函数且返回类型为常量<br />为了保证非常量下的使用，需要重载 |

对于最后一种情况，具体重载实现如下

```cpp
int& Vector::findElement(const int& value) {  //返回类型为引用
		...//具体实现
 }

const int& Vector::findElement(const int& value) const {  //双const标记
 		return const_cast<Vector&>(*this).findElement(value);
    	//const_cast<Vector&>定义了一种能将Vector&从常量转为非常量的对象
    	//const_cast<Vector&>(*this)，将对象转为非常量
    	//.findElement(value)，调用非常量对象下的非常量findElement实现
 }
```



## 继承与成员访问控制

### 继承

在class定义后接上如`: public Parent`来继承父类的属性

使用`virtual`关键词来允许子类重写父类的函数

（注意`virtual`同时是一种继承方法，主要是为了解决菱形继承的问题，含义不同）

```cpp
class Shape {
public:
    virtual double area() const = 0;
};
class Circle : public Shape {
public:
    // constructor
    Circle(double radius): _radius{radius} {};
    double area() const {
        return 3.14 * _radius * _radius;
    }
private:
    double _radius;
};
```

### 成员访问控制

为了管理类内成员对外部、子类的成员访问权限，C++中有三种类内访问控制修饰符，其限制如下：

| 访问控制修饰符 | 类内访问 | 派生类访问 | 类外访问 |       用途       |
| :------------: | :------: | :--------: | :------: | :--------------: |
|    `public`    |    ✔️     |     ✔️      |    ✔️     |   定义类的接口   |
|   `private`    |    ✔️     |     ❌      |    ❌     |   封装实现细节   |
|  `protected`   |    ✔️     |     ✔️      |    ❌     | 支持继承中的扩展 |

其中，`private`**只能**由类本身的函数访问，隐藏了封装细节，并保证数据的安全性

而为了在继承关系中提供一定的灵活性，允许派生类访问基类的某些实现细节，我们也可以使用`protected`，即子类中可以定义新的函数，对此类成员进行访问。

类的继承与成员属性类似，同样具有`public, protected, private`三类方式，它会对应地，将原先父类的高访问权限降级到低访问权限——例如，使用`protected`继承，那么原本父类的`public`成员会变为`protected`，而`private`成员不变。具体的访问控制影响如下：

| 基类成员访问权限 |     `public` 继承      |    `protected` 继承    |    `private` 继承    |
| :--------------: | :--------------------: | :--------------------: | :------------------: |
|  `public` 成员   |  派生类中为 `public`   | 派生类中为 `protected` | 派生类中为 `private` |
| `protected` 成员 | 派生类中为 `protected` | 派生类中为 `protected` | 派生类中为 `private` |
|  `private` 成员  |        不可访问        |        不可访问        |       不可访问       |

其中，`private`成员只能通过基类提供的`public`或`protected`的调用函数进行访问。

!!! note "友元函数"

    为了在其他类内访问类内私有函数，我们可以引入友元函数。在被访问的类内，通过 `friend` 声明外部函数，可以允许其可访问类的私有（`private`）和保护（`protected`）成员，举例如`friend void func(const MyClass& obj);`
    
    - **用途**：  
      1. 直接访问类私有数据（如 `obj.secret`）。  
      2. 重载操作符（如 `<<`/`>>`）时简化实现（`friend ostream& operator<<(...)`）。
    
    - **注意**：  
      - 友元关系单向且不可继承。  
      - 友元函数应当**慎重使用**！过度使用会破坏封装性，降低代码可维护性。



## 模板

当我们需要类/函数中允许相似处理不同的类型的对象时，我们可以引入模版(Template)

使用`template <typename T>`放在类/函数前，说明需要使用模板。随后可以直接使用T以及它的衍生类型，进行类和函数的撰写。

一个有趣的事实是，`<typename T>`可以很自由的改变，包括使用`class`(完全等价),  `bool`(只能使用真或假), `int`(可以使用整数)

!!! note "模板的机理"

    事实上，模板的实例化是编译期行为。编译器需要在编译每个翻译单元（.cpp文件）时，根据模板的完整定义，替换生成具体类型的代码——例如` T& at(size_t index);`会变为`int at(size_t index);`。
    
    如果模板的实现（函数或类的定义）不在头文件中，其他.cpp文件包含头文件时，编译器无法看到实现，会导致链接错误。因此，模板要求在头文件内存在，或插入实现代码。同时，由于每个T的类型会生成对应的具体类型，编译后的代码存在膨胀的隐患。

### 基础模版

#### 模板类

使用模板类，我们只需要将所有需要再定义的对象类型变为模板即可

当我们使用一个模板类时，使用`classname<T>`来初始化对应的模板类型

一个具体的模板类案例如下：

```cpp
//vector.h
template <typename T>
 class Vector {
 public:
     T& at(size_t i);
 };
#include "Vector.cpp"	//注意！我们需要在vector.h的末尾引用vector.cpp

//vector.cpp
//实现函数也需要使用模版标志
template <typename T>
T& Vector<T>::at(size_t i) {...}	//注意，命名空间（类）也含有<T>
```

#### 模板函数

与模板类类似，我们也需要前置模板标志，同时，在编译过程中，不同类型的函数会被独立实现

当我们使用一个模板函数时，我们可以省去模板类型的初始化——即让编译器去自行判断函数输入参数类型。

一个经典的STL函数的模板案例如下

```cpp
template< class InputIt, class T>
InputIt find( InputIt first, InputIt last, const T& value);
```



### Concept(C++20)

当需要对模板参数进行**约束**时，可以使用 C++20 引入的 **`concept`** 机制，明确类型必须满足的接口或特性。

使用 `template <typename T>` 后通过 `requires` 或直接定义 concept，规范模板参数的行为，限制类型必须支持的操作或特性

一个关键优势是：**编译期检查约束条件**，替代复杂的 SFINAE 技巧，提升代码可读性和错误提示。

#### 定义 Concept

通过 `requires` 表达式或逻辑运算符组合约束条件：

```cpp
// 定义支持加法操作的类型约束
template <typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::convertible_to<T>; // 要求支持 + 且结果可转 T
};
// 组合约束：整型或浮点型
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;
//要求对象存在
template <typename C>
concept Container = requires(C c) {
    c.begin();      // 必须存在 begin()
    c.end();        // 必须存在 end()
    typename C::value_type;  // 必须有内部类型 value_type
};
```

#### 使用 Concept

```cpp
template <Numeric T>  // 直接使用 concept 作为模板参数
class Calculator { 
    T add(T a, T b) { return a + b; }
};
//或者
template <typename T> requires Addable<T>   // 通过 requires 子句约束
T sum(T a, T b) { return a + b; }
```

C++20标准中也引入了许多标准的Concept，可以替换`typename`，提供更显式，便于维护的类型检查

### 可变参数模板（Variadic Templates）

有时候我们并不确定输入函数的变量的数量——我们可以通过模板来实现针对不同变量的函数的自动化重载，实现关键如下

- **定义参数包**：`template <typename... Args>`
- **展开参数包**：通过递归或折叠表达式（C++17+）处理参数。

#### 递归版本（C++11）

在一般实现中，我们需要使用递归的技巧——最后会自动展开定义n个`min`函数

```cpp
// 递归终止条件：仅一个参数时返回自身
template <typename T>
T min(T val) {
    return val;
}

// 递归展开：比较当前参数与剩余参数的最小值
template <typename T, typename... Args>
T min(T& first, Args&... args) {
    T rest_min = min(args...); // 展开剩余参数包
    return (first < rest_min) ? first : rest_min;
}
//折叠表达式c++17
template <typename... Args>
auto sum(Args... args) {
    return (args + ...); // 展开为 1 + 2 + 3 + ...
}
```

注意，每个不同参数组合生成独立实例化代码，且递归使用，会有**代码膨胀风险**，和**递归深度限制**的风险



## 重载与多态

### 符号重载

可以使用类似函数定义的方式，进行符号重载（绝大部分符合都可以重载，除了指针相关的）

符号重载既可以在类当中，也可以是全局的——这主要取决于交互的对象

例如，当符号是有两侧的对象时，且无序时，一般使用全局的定义

```cpp
//使用全局实现，调用公开接口
MyClass operator+(const MyClass& obj, int value) {
    MyClass result = obj;
    result.setData(result.getData() + value);
    return result;
}
MyClass operator+(int value, const MyClass& obj) {
    return obj + value;  // 复用上面的实现
}
```

而当需要在类外定义，且调用私密成员时，可以使用友元函数

```cpp
class Student {
    friend ostream& operator<<(ostream& os, const Student& s);
private:
    string name;
};

ostream& operator<<(ostream& os, const Student& s) {
    return os << "Student: " << s.name;
}
```

### SMF



### Move Semantics



## 报错管理
