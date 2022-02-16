import asyncio
from os import environ
from time import sleep

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    async def onJoin(self, details):
        def ip():
            while True:
                try:
                    sleep(10)
                    get = '127.0.0.1'
                    return get
                finally:
                    pass

        await self.register(ip, 'com.arguments.ip')

        print("Connected")

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)
