from autobahn.asyncio import WebSocketServerProtocol
import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, response):
        print("Connected to Server: {}".format(response.peer))

    async def onOpen(self):
        while True:
            try:
                self.sendMessage(u"Hello, world!".encode('utf8'))
                await asyncio.sleep(5)
            finally:
                pass

    async def onMessage(self, payload, isBinary):
        print("Message: {0}".format(payload.decode('utf8')))


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
