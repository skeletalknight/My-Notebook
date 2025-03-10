## React

React的设计哲学是**组件化**

### 基础语法

```typescript
import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';  //用于路由跳转

const Welcome = ()=> {
  const [inputValue, setInputValue] = useState('');  //创建钩子
  const handleSend = async () => {			
    if (inputValue.trim()) {
      const userName = inputValue.trim();
      navigate("/room", { state: userName });
    }
  };

  return (
    <div className="welcome-container">
          <div className="form-group">
            <input type="text"
            className="form-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)} />	//传递输入框的值
          </div>
          <button type="submit" className="submit-button" onClick={()=>handleSend()}>提交</button>
    </div>
  );};

export default Welcome;
```

#### 组件化

目前主流的设计理念是函数化组件

组件会具有从上到下的树状结构关系，函数、参量可以有上到下传递

在`tsx`中，使用` <ComponentName value={...} />`使用组件并传递参量

 使用`export` 关键字使此函数可以在此文件之外访问。`default` 关键字表明它是文件中的主要函数。



### 钩子函数

#### useState

`useState`用于创建一个可更新的状态量，它可以在组件中自上而下传递

使用例如：`const [inputValue（值）, setInputValue（更改函数）] = useState(初始值);`

可以读取值，但不能直接赋值，而是使用更改函数进行替换（如果要合并，使用`[... Newdata]`）

#### useRef

`useRef`用于创造一个引用，它可以让函数实时获取最新的、相同的值

使用`const ref = useRef(初始值)`进行初始化，使用`.current`获取/修改其值

修改`ref`并不会导致组件重新渲染

#### useEffect

`useEffect`用于处理副作用（side effects），即那些影响到组件外部环境的操作，其语法如下：

```typescript
useEffect(() => {
  ...  // 副作用逻辑
  return () => {
  ...  // 清理逻辑
  };
}, [dependencies]);//触发依赖
```

- 副作用逻辑：每次触发时会执行的函数
- 清理逻辑：使用清理逻辑清除遗留效果
- 触发依赖：
  - 空数组 `[]`: 仅在组件挂载（触发副作用）和卸载（触发清理）时执行。
  - 依赖项变化时: 当依赖项中的某个值发生变化时，<u>先执行旧逻辑的清理函数</u>，然后执行新的副作用。

<u>然而`useEffect`的功能比较初级，对许多情况下推荐使用集成的第三方库</u>

#### useSWR

使用`import useSWR, { mutate }  from 'swr';`进行引入

基础语法: `const {data, error, isLoading} = useSWR(key, fetcher，{...设置})`

`key`是一个状态量唯一的标识，`fetcher`会接受`key`并获取数据，其返回值会自动更新状态量

设置中可以传入如`refreshInterval:300`，对自动更新间隔等进行更新

可以全局使用由`key`标记的状态量

可以全局使用`mutate(key)`的方式，立即进行更新并重新渲染

（注意，由于使用`mutate`更新与获取数据是异步的，需要使用`await`等方式延后`mutate`的更新）



### 设计哲学

- 将 UI 拆解为组件层级结构
- 使用 React 构建一个静态版本
- 找出 UI 精简且完整的 state 表示与位置
- 添加数据流逻辑



 

