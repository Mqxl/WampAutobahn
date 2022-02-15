import asyncio
from os import environ

from autobahn.asyncio.component import Component
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    async def onJoin(self, details):
        def test():
            while True:
                try:
                    print('Write ip:')
                    get = input()
                    return get
                finally:
                    pass
        await self.register(test, 'com.arguments.test')
        print("Connected")

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)