是一个基于 Python 的异步 UDP（User Datagram Protocol）通信库，利用了 asyncio 库来实现高效、非阻塞的网络数据报传输。这个项目旨在简化在 asyncio 环境中进行 UDP 通信的操作，并提供了易于使用的 API。

## 功能特性

- 使用 AsyncUdp 类能够轻松地异步发送和接收 UDP 数据报文。
- 支持 IPv4 和 IPv6 地址族（通过 socket.AF_INET 或 socket.AF_INET6 参数指定）。
- 提供上下文管理协议支持，可通过 async with 语句安全地初始化和关闭连接。
- 包含类方法 get_udp，作为一个协程工厂函数，用于快速创建并启动一个异步 UDP 连接。


### 示例
实现一个简单的DNS请求：
```python
import asyncio
from asyncudp import AsyncUdp

DATA = '\x5a\x6d\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77\x05\x68\x74\x79\x70\x65\x03\x74\x6f\x70\x00\x00\x1c\x00\x01'

async def main():
    async with AsyncUdp() as udp_async:
        await udp_async.sendto(DATA, ('8.8.8.8', 53))
        data, addr = await udp_async.recvfrom()
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```
示例中使用上下文方式，还可以手动建立asyncudp：
```python
# 使用get_udp()函数建立
udp_async = await AsyncUdp.get_udp()

# 手动实例化并使用mske()方法
udp_async = AsyncUdp()
await udp_async.make()
```

# AsyncUdp对象：

## AsyncUdp()
语法：AsyncUdp(local_addr:tuple = None,  family: socket.AddressFamily = socket.AF_INET )
参数：
- local_addr：元组类型，需要绑定的本地套接字，禁止传入('', 80)这样的空地址，表示所有地址应使用('0.0.0.0', 80)或者('::', 80)
- family：一个socket.AddressFamily对象，可选socket.AF_INET、socket.AF_INET6
返回值：
- 一个AsyncUdp对象

### async AsyncUdp.make()
这是一个协程函数，用于在AsyncUdp对象上建立协程UDPSocker。
返回值: 类型Tuple(ip, port)，代表本地Address 


### async AsyncUdp.sendto()
语法：AsyncUdp.sendto(data: bytes, address: tuple)
发送数据到指定的Address。和socket.sendto()相同。
参数：
- data：bytes类型，需要传输的数据
- address：Tuple类型，需要传输给哪个Address


### async AsyncUdp.recvfrom()
在AsyncUDP上接收数据。和socket.recvfrom()类似。
返回值：
- 返回Tuple(data: bytes, addr: tuple)


### async AsyncUdp.close()
释放Async UDP。

## async AsyncUdp.get_udp()
这是一个协程的工厂函数
用于异步获得协程udp连接，相当于实例化AsyncUdp后运行了make()
参数：
- local_addr：禁止传入('', 80)这样的空地址，表示所有地址应使用('0.0.0.0', 80)或者('::', 80)
- family：可选socket.AF_INET、socket.AF_INET6
返回值：
- 返回一个 Tuple(ip, port)，代表本地地址的Address


