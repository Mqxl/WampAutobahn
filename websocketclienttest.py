from os import environ
from threading import Thread
from time import sleep
from autobahn.asyncio import WebSocketClientProtocol, ApplicationSession
import asyncio
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.websocket import WebSocketClientFactory
import nest_asyncio
import random


class ReconnectingTCPClientProtocol(asyncio.Protocol):
    max_delay = 3600
    initial_delay = 1.0
    factor = 2.7182818284590451
    jitter = 0.119626565582
    max_retries = None

    def __init__(self, *args, loop=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._args = args
        self._kwargs = kwargs
        self._retries = 0
        self._delay = self.initial_delay
        self._continue_trying = True
        self._call_handle = None
        self._connector = None

    def connection_lost(self, exc):
        if self._continue_trying:
            self.retry()

    def connection_failed(self, exc):
        if self._continue_trying:
            self.retry()

    def retry(self):
        if not self._continue_trying:
            return

        self._retries += 1
        if self.max_retries is not None and (self._retries > self.max_retries):
            return

        self._delay = min(self._delay * self.factor, self.max_delay)
        if self.jitter:
            self._delay = random.normalvariate(self._delay,
                                               self._delay * self.jitter)
        self._call_handle = self._loop.call_later(self._delay, self.connect)

    def connect(self):
        if self._connector is None:
            self._connector = self._loop.create_task(self._connect())

    async def _connect(self):
        try:
            await self._loop.create_connection(lambda: self,
                                               *self._args, **self._kwargs)
        except Exception as exc:
            self._loop.call_soon(self.connection_failed, exc)
        finally:
            self._connector = None

    def stop_trying(self):
        if self._call_handle:
            self._call_handle.cancel()
            self._call_handle = None
        self._continue_trying = False
        if self._connector is not None:
            self._connector.cancel()
            self._connector = None


class Component(ApplicationSession):
    async def onJoin(self, details):
        while True:
            try:
                test = await self.call('com.arguments.ip')
            finally:
                pass


class MyClientProtocol(WebSocketClientProtocol):
    class EchoClientProtocol(ReconnectingTCPClientProtocol):
        def __init__(self, message, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.message = message

        def connection_made(self, transport):
            transport.write(self.message.encode())
            print('Data sent: {!r}'.format(self.message))

        def data_received(self, data):
            print('Data received: {!r}'.format(data.decode()))

        def connection_lost(self, exc):
            print('The server closed the connection')
            print('Stop the event loop')
            self._loop.stop()

    async def onMessage(self, payload, isBinary):
        print("Message: {0}".format(payload.decode('utf8')))

    async def onOpen(self):
        while True:
            try:
                c = Component()
                loop = asyncio.get_event_loop()
                client = EchoClientProtocol('Hello, world!', c.onJoin(self.test), 5000, loop=loop)
                client.connect()
                thread = Thread(target=loop.run_forever)
                thread.start()
                loop.call_soon_threadsafe(loop.stop)
                thread.join()
                sleep(10)
                self.sendMessage(u"Im connected".encode('utf8'))
                await asyncio.sleep(15)
            finally:
                pass


if __name__ == '__main__':
    class EchoClientProtocol(ReconnectingTCPClientProtocol):
        def __init__(self, message, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.message = message

        def connection_made(self, transport):
            transport.write(self.message.encode())
            print('Data sent: {!r}'.format(self.message))

        def data_received(self, data):
            print('Data received: {!r}'.format(data.decode()))

        def connection_lost(self, exc):
            print('The server closed the connection')
            print('Stop the event loop')
            self._loop.stop()

    while True:
        try:
            loop = asyncio.get_event_loop()
            client = EchoClientProtocol('Hello, world!', '127.0.0.1', 5000, loop=loop)
            client.connect()
            thread = Thread(target=loop.run_forever)
            thread.start()
            loop.call_soon_threadsafe(loop.stop)
            thread.join()
            sleep(10)

        finally:
            pass



