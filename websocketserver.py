from time import sleep

from autobahn.asyncio import WebSocketServerProtocol
import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, response):
        print("Connected to Server: {}".format(response.peer))

    def onOpen(self):
        while True:
            try:
                print('Write message')
                message = input()
                self.sendMessage(message.encode('utf8'))
                sleep(10)
            finally:
                pass


if __name__ == '__main__':

    factory = WebSocketServerFactory()
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 5000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
