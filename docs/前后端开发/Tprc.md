## TRPC

### 选择TRPC

对于非TS语言的后端开发，会出现重复的代码和繁琐的前后端对接

在开发小型项目时，可以考虑使用TS全栈开发后端，减少工作量

在这里可以使用`Trpc`作为前后端的连接器，非常地方便



### 对象声明

引入库

```typescript
import { initTRPC } from '@trpc/server';
import * as trpcExpress from '@trpc/server/adapters/express';  //不同模板
import express from 'express';
import cors from 'cors';
```

创造对象

```typescript
const createContext = ...
type Context = Awaited<ReturnType<typeof createContext>>;
const t1 = initTRPC.context<Context>().create();
```



### 创建路由函数

```typescript
const roomRouter = t1.router({
  list: t1.procedure
  .query(async () => {
    const roomList = await db.room.getRoomList();
    return responseCreater(roomList);
  }),
  add: t1.procedure
  .input(res => res)
  .mutation(async (opts) => { 
    const input = opts.input as inter.RoomAddArgs;
    const output = await db.room.addRoomList(input);
    return responseCreater(output);
  }),
  message: roomMessageRouter,
});
```

创建路由函数后，赋予属性函数，由`t1.procedure`开始

对于`GET`请求使用`query`，对于`POST`请求使用`mutation`

也可以直接使用路由嵌套

使用`export type RoomRouter = typeof roomRouter;`将类型暴露，让前端引入



### 创造后端服务

```typescript
const app = express(); //使用express
app.use(cors(...));  //创造跨域名限制
app.use(
  '/api/room',
  trpcExpress.createExpressMiddleware({
    router: roomRouter,
    createContext,
  }),
);					//绑定路由
app.listen(3000); //监听接口
```

启动服务后，前端调用如下：

```typescript
const room_trpc = createTRPCProxyClient<RoomRouter>({
  links: [
    httpBatchLink({
      url: `${API_URL}/api/room`,
    }),
  ],
});
```

