import asyncio
import socket


class UdpProtocol:
    def __init__(self):
        self.__transport = None
        self.__data_received = asyncio.Event()

    # 连接建立时被调用。
    def connection_made(self, transport):
        self.__transport = transport

    # 当接收到数据报时被调用。
    def datagram_received(self, data, addr):
        self.__data_received.set()
        self.data = data
        self.addr = addr

    # 主动接收消息。
    async def recv(self):
        await self.__data_received.wait()
        self.__data_received.clear()
        return self.data, self.addr

    # 当前一个发送或接收操作引发 OSError 时被调用。
    def error_received(self, exc):
        self.__transport.close()
        raise exc

    # 连接丢失或关闭时将被调用。
    def connection_lost(self, exc):
        if exc is None:
            return
        else:
            raise exc

class AsyncUdp:
    def __init__(self, 
                 local_addr:tuple = None, 
                 family: socket.AddressFamily = socket.AF_INET
                 ) -> None:
        '''
        local_addr禁止传入('', 80)这样的空地址，表示所有地址应使用('0.0.0.0', 80)或者('::', 80)\n
        family可选socket.AF_INET、socket.AF_INET6
        '''
        # linux中不能传入空address 故提前指定
        if local_addr is None:
            if family == socket.AF_INET:
                self.local_addr = ('0.0.0.0', 0)
            elif family == socket.AF_INET6:
                self.local_addr = ('::', 0)
        else:
            self.local_addr = local_addr
        self.family = family
        self.__transport = None
        self.__protocol = None
        self.__sock = None   # 保留原始socket接口
    
    @classmethod
    async def get_udp(cls, 
                      local_addr:tuple = None, 
                      family: socket.AddressFamily = socket.AF_INET
                      ):
        '''
        这是一个协程工厂函数\n
        用于异步获得协程udp连接，相当于实例化AsyncUdp后运行了make()\n
        local_addr: 禁止传入('', 80)这样的空地址，表示所有地址应使用('0.0.0.0', 80)或者('::', 80)\n
        family: 可选socket.AF_INET、socket.AF_INET6
        返回值: Tuple(ip, port)
        '''
        async_udp = cls(local_addr, family)
        await async_udp.make()
        return async_udp

    async def make(self) -> tuple:
        '''
        这是一个协程函数\n建立协程UDPSocker。
        返回值: Tuple(ip, port)
        '''
        self.__transport, self.__protocol = await asyncio.get_event_loop().create_datagram_endpoint(
            lambda: UdpProtocol(), 
            local_addr=self.local_addr, 
            family=self.family
            )
        self.__sock = self.__transport.get_extra_info('socket')
        return self.__transport.get_extra_info('sockname')

    async def sendto(self, data:bytes, address:tuple) -> None:
        '''这是一个协程函数'''
        # DatagramTransport.sendto()只接受IP地址不接受域名 手动解析域名
        addr_info = await asyncio.get_event_loop().getaddrinfo(
            host=address[0], 
            port=address[1], 
            family=self.family, 
            type=socket.SOCK_DGRAM
            )
        try:
            self.__transport.sendto(data, addr_info[0][4])
        except AttributeError:
            raise AttributeError('实例必须执行AsyncUdp.make()后才能使用AsyncUdp.sendto()')
        except TypeError:
            raise TypeError('data')

    async def recvfrom(self) -> tuple:
        '''这是一个协程函数\n返回值-> (data: bytes, addr: tuple)'''
        try:
            return await self.__protocol.recv()
        except AttributeError:
            raise AttributeError('实例必须执行AsyncUdp.make()后才能使用AsyncUdp.recvfrom()')
    
    def close(self):
        try:
            self.__transport.close()
        except AttributeError:
            pass
        return 
    
    def __del__(self) -> None:
        try:
            self.__transport.close()
        except AttributeError:
            pass

    async def __aenter__(self):
        await self.make()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        self.close()


if __name__ == "__main__":
    pass