from os import environ
from threading import Thread
from time import sleep
from autobahn.asyncio import WebSocketClientProtocol, ApplicationSession
import asyncio
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.websocket import WebSocketClientFactory
import nest_asyncio


class MyClientProtocol(WebSocketClientProtocol):
    async def onMessage(self, payload, isBinary):
        print("Message: {0}".format(payload.decode('utf8')))

    async def onOpen(self):
        while True:
            try:
                self.sendMessage(u"Im connected".encode('utf8'))
                await asyncio.sleep(15)
            finally:
                pass


class Component(ApplicationSession):
    async def onJoin(self, details):
        while True:
            try:
                test = await self.call('com.arguments.ip')
                nest_asyncio.apply()
                factory = WebSocketClientFactory()
                factory.protocol = MyClientProtocol
                loop = asyncio.get_event_loop()
                coro = loop.create_connection(factory, '{}'.format(test), 5000)
                loop.run_until_complete(coro)
                thread = Thread(target=loop.run_forever)
                thread.start()
                print('Requested stop!')
                loop.call_soon_threadsafe(loop.stop)
                thread.join()
            except IndexError:
                print('Error')


if __name__ == '__main__':
    while True:
        try:
            loop = asyncio.get_event_loop()
            url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
            realm = "realm1"
            runner = ApplicationRunner(url, realm)
            run = runner.run(Component)
            loop.run_until_complete(run)
            thread = Thread(target=loop.run_forever)
            thread.start()
            loop.call_soon_threadsafe(loop.stop)
            thread.join()
        except IndexError:
            print('Connected')
