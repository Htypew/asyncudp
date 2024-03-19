import asyncio
from asyncudp import AsyncUdp


MESSAGE = b'\x00\x01\x00\x00\x56\x8a\xde\xb0\xfb\x63\x3a\x30\x06\x04\xb2\x26\x94\xae\x58\x10'

async def test(stun_host):
    async with AsyncUdp() as udp_async:
        await udp_async.sendto(MESSAGE, (stun_host, 3478))
        data, addr = await udp_async.recvfrom()
        if data:
            print(stun_host, 'Yes')
        else:
            print(stun_host, 'No')

async def main():
    stun_hosts = ['stun.taxsee.com', 'stun.l.google.com', 'stun1.l.google.com', 'stun2.l.google.com', 'stun3.l.google.com', 'stun4.l.google.com', 'stun.htype.top']
    task_list = []
    for host in stun_hosts:
        task = asyncio.create_task(test(host))
        task_list.append(task)
    await asyncio.wait(task_list)





if __name__ == "__main__":
    asyncio.run(main())
