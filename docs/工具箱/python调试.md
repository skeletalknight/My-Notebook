### Python 调试方法（VS Code 版）

#### 一、VS Code 原生调试

**特点**：图形化界面，集成度高  
**配置**：  

1. 创建 `.vscode/launch.json`：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false  // 调试第三方库
        }]}
```

- 点击行号左侧设置断点
- `F5` 启动调试
- 核心功能：
	- 变量监视窗口
	- 步进控制（`F10`/`F11`/`Shift+F11`）
	- 调试控制台交互

------

#### 二、Debugpy（远程调试）

代码中加入

```python
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # 阻塞等待连接
```

VS Code 配置（`launch.json`）：

```json
{
    "name": "Python: Attach",
    "type": "python",
    "request": "attach",
    "connect": {"host": "localhost", "port": 5678}
}
```

**远程调试命令**：

```bash
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client your_script.py
```

------

#### 三、pdb 命令行调试

**特点**：Python 内置，无需 IDE
**核心命令**：

|     命令     |         功能         |
| :----------: | :------------------: |
|   `l(ist)`   |    查看上下文代码    |
|   `n(ext)`   |      执行下一行      |
|   `s(tep)`   |       进入函数       |
| `c(ontinue)` | 继续运行到下一个断点 |
|  `p <变量>`  |      打印变量值      |

**使用方式**：

```python
# 代码中插入断点
import pdb; pdb.set_trace()  # Python <3.7
breakpoint()                 # Python ≥3.7
```

```bash
# 终端启动
python -m pdb your_script.py
```

