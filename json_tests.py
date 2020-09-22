import asyncio
import json
import socket
import time
from multiprocessing import Pipe, Process

import aiohttp
from aiohttp import web


def get_new_message_str(i) -> str:
    msg = f'{{"type": "l2update","product_id": "BTC-USD","time": "2019-08-14T20:42:27.265Z", ' \
          f'"t1": "{i}", "changes": [[  "buy", "10101.80000000", "0.162567" ]]}} \n'
    return msg


def send_messages(max, sending_pipe: Pipe):
    for i in range(max):
        sending_pipe.send(get_new_message_str(i))


def unix_pipe_test(count):
    sending_pipe, receiving_pipe = Pipe()

    p = Process(target=send_messages, args=(count, sending_pipe))
    p.start()

    now = time.time()

    for i in range(count):
        msg = receiving_pipe.recv()
        parsed = json.loads(msg)
    later = time.time()

    p.join()

    print(now, later)
    print((later - now) / count)


def send_to_socket(count, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            f = conn.makefile(mode="w")
            f.writelines((get_new_message_str(i) for i in range(count)))

            print(f'send {count} and done')


def socket_test(count, port):
    p = Process(target=send_to_socket, args=(count, port))
    p.start()

    time.sleep(1)
    s = socket.socket()
    s.connect(("localhost", port))
    f = s.makefile()

    now = time.time()

    s = 0
    for line in f.readlines():
        parsed = json.loads(line)
        # s += len(line)

    later = time.time()

    print(now, later)
    print((later - now) / count)
    p.join()


def send_via_websocket(count, port):
    import asyncio
    import websockets

    async def stream(websocket, path):
        for i in range(count):
            await websocket.send(get_new_message_str(i))
        await websocket.close()
        print(f"sent {count} messages")

    start_server = websockets.serve(stream, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def websocket_test_async(count, port):
    p = Process(target=send_via_websocket, args=(count, port))
    p.start()

    time.sleep(1)
    import websockets

    now = time.time()

    i = 0

    async def read():
        nonlocal i
        uri = f"ws://localhost:{port}"
        async with websockets.connect(uri) as websocket:
            async for line in websocket:
                msg = json.loads(line)
                i += 1

    asyncio.get_event_loop().run_until_complete(read())

    later = time.time()
    print(f"Received {i} messages")
    print(now, later)
    print((later - now) / count)
    p.join()


def send_via_aiohttp_websocket(count, port):
    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        for i in range(count):
            await ws.send_str(get_new_message_str(i))

        print('websocket connection closed')
        return ws

    async def make_app():
        app = web.Application()
        app.add_routes([web.get('/', websocket_handler)])
        return app

    web.run_app(make_app(), host="localhost", port=port)


def websocket_test_aiohttp(count, port):
    p = Process(target=send_via_aiohttp_websocket, args=(count, port))
    p.start()

    time.sleep(1)
    import websockets

    now = time.time()

    i = 0

    async def read():
        nonlocal i
        uri = f"ws://localhost:{port}/"
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(uri) as ws:
                async for msg in ws:
                    message = json.loads(msg.data)
                    # message = msg.data
                    i += 1

    asyncio.get_event_loop().run_until_complete(read())

    later = time.time()
    print(f"Received {i} messages")
    print(now, later)
    print((later - now) / count)
    print(int(later - now))
    p.join()


if __name__ == '__main__':
    unix_pipe_test(10 ** 6)
    socket_test(10 ** 6, 9997)
    # websocket_test_async(10 ** 5, 9991)
    # websocket_test_aiohttp(10 ** 5, 9991)
