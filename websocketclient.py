from os import environ
from threading import Thread
from multiprocessing import Process
import autobahn.exception
from autobahn.asyncio import WebSocketClientProtocol, ApplicationSession
import asyncio
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.websocket import WebSocketClientFactory
import nest_asyncio


class MyClientProtocol(WebSocketClientProtocol):

    async def onMessage(self, payload, isBinary):
        try:
            print("Message: {0}".format(payload.decode('utf8')))
        finally:
            pass
        if autobahn.exception.Disconnected:
            pass

    async def onOpen(self):
        self.sendMessage(u"Im connected".encode('utf8'))

    async def onClose(self, wasClean, code, reason):
        print('Try to reconnect')


def connect():
    nest_asyncio.apply()
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


def msg():
    get = 'Process created'
    return get


class Component(ApplicationSession):

    async def onJoin(self, details):
        await self.register(msg, 'com.arguments.msg')
        i = 0
        while i < 10:
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
                p = Process(target=Thread)
                p.start()
                loop.call_soon_threadsafe(loop.stop)
                if not p.join():
                    print('Process pid is ' + str(p.pid))
                thread.join()
                p.join()
                i += 1
            finally:
                continue


if __name__ == '__main__':
    while True:
        try:
            pass
        except KeyboardInterrupt:
            pass
