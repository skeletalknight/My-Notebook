## 迭代器

python中的迭代器`Iterator`是一个数据流，通过`next()`函数调用并不断返回下一个数据，直到没有数据时抛出`StopIteration`错误

使用`(x for x in range(10))`的python语法可以便捷产生迭代器

在函数内嵌入`yield`关键词也会将函数转为可迭代函数

`list`、`dict`、`str`虽然是`Iterable`，却不是`Iterator`，但可以使用`iter()`函数将他们变为可迭代对象

`map(函数，Iterable)`将传入的函数依次作用到序列的每个元素，并把结果作为新的`Iterator`返回

`ruduce(函数，Iterable)`则不断将函数作用于元素，并做累积计算，如

`reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)`

`filter(函数，Iterable)`传入的函数依次作用于每个元素，然后根据返回值是`True`还是`False`决定保留还是丢弃该元素



## 闭包函数

高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回，如

```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
```

这种程序结构称为**闭包**（Closure），它能将相关参数和变量都保存在返回的函数中

但需要注意，闭包在存储变量时，只是引用变量而非存储值，所以**不要**引用任何循环变量，或者后续会发生变化的变量

一定要引用可变变量时，可以再创建一个函数来绑定该值，如

```python
for i in range(1, 4):
    def f():
    	return i*i
    yield f				#错误，最后三个f都输出9
   
def f(j):
    def g():
        return j*j
    return g
fs = []
for i in range(1, 4):
    yield (f(i)			#正确，分别输出1,4,9
```

使用闭包，就是内层函数引用了外层函数的局部变量，如果只是读取就一切正常

如果要对这个变量赋值，Python解释器会把`x`当作闭包内函数`fn()`的局部变量而报错

所以需要在闭包内函数`fn()`函数内部加一个`nonlocal x`的声明，之后解释器就会把把`fn()`的`x`看作外层函数的局部变量

