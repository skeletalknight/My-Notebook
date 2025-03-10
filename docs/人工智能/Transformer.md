## Transformer

### 注意力机制

在现实中，人的注意力往往可以分为自主性的与非自主性的注意力（存在提示）

自主性的（无额外提示的）注意力，可以通过参数化的全连接层，甚至是非参数化的最大汇聚层来模拟

而“**是否包含自主性提示**”将注意力机制与全连接层或汇聚层区别开来，我们作出以下定义

- *查询*（query）：自主性提示，往往作为较少的意志线索进行输入
- *键*（key）：非意志线索，可以想象为感官输入
- *值*（value）：感觉输入，将查询与键匹配，引导出最匹配的值

![../_images/qkv.svg](post_content/深度学习/qkv.svg)

我们可以写出一个通用的注意力汇聚公式：

$f(x) = \sum_{i=1}^n \alpha(x, x_i) y_i$

其中$(x_i,y_i)$是键值对，而$x$为查询，通过注意力权重$\alpha$，我们实现了对不同值分配不同注意力

一般来讲，我们会设置一个注意力评分函数，经过softmax函数后对值赋权

```python
class NWKernelRegression(nn.Module): #一个简单的注意力模型
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.w = nn.Parameter(torch.rand((1,), requires_grad=True))

    def forward(self, queries, keys, values):
        # queries和attention_weights的形状为(查询个数，“键－值”对个数)
        queries = queries.repeat_interleave(keys.shape[1]).reshape((-1, keys.shape[1]))
        self.attention_weights = nn.functional.softmax(
            -((queries - keys) * self.w)**2 / 2, dim=1)
        # values的形状为(查询个数，“键－值”对个数)
        return torch.bmm(self.attention_weights.unsqueeze(1),
                         values.unsqueeze(-1)).reshape(-1) #使用bmm进行高效的小批次矩阵乘法
```

在这里我们补充一下更细节的操作：

- Mask：遮掩无意义词元，使用大负数替代
- 加性注意力：$a(\mathbf q, \mathbf k) = \mathbf w_v^\top \text{tanh}(\mathbf W_q\mathbf q + \mathbf W_k \mathbf k) \in \mathbb{R}$，

- 缩放点积注意力$a(\mathbf q, \mathbf k) = \mathbf{q}^\top \mathbf{k}  /\sqrt{d}.$：
	- 点积可以得到计算效率更高的评分函数——但它要求相同的长度
	- 为了确保点积方差为1，我们再除以$\sqrt{d}$

### Bahdanau注意力

Bahdanau等人提出了一个没有<u>严格单向对齐限制</u>的 可微注意力模型 

在预测词元时，如果不是所有输入词元都相关，模型将仅对齐（或参与）输入序列中与当前预测相关的部分

这是通过将**上下文变量**视为注意力集中的输出来实现的。

有$\mathbf{c}_{t'} = \sum_{t=1}^T \alpha(\mathbf{s}_{t' - 1}, \mathbf{h}_t) \mathbf{h}_t$ 

时间步$t^′−1$时的解码器隐状态$s_{t^′−1}$是查询， 编码器隐状态$h_t$**既是键，也是值**





![../_images/seq2seq-attention-details.svg](post_content/Transformer/seq2seq-attention-details.svg)

