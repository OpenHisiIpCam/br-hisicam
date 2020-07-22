import asyncio
import logging
import os, sys
import json
from contextlib import contextmanager


STATUS_OK = "OK"
STATUS_FAILED = "FAILED"


logger = logging.getLogger("camstore")


class FailedRequest(Exception):
    def __init__(self, response):
        self.status = response["status"]
        self.message = response["message"]


class Device:
    def __init__(self, name, port):
        self.name = name
        self.port = port


class Connection:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *arg, **kwargs):
        await self.close()

    def __init__(self, port=43500):
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        logger.debug(f"Connect to camstore daemon on {self.port}...")
        self.reader, self.writer = await asyncio.open_connection(host="localhost", port=self.port)
        logger.debug("Connected")

        await asyncio.wait_for(self.reader.readuntil(b"#"), 2)

        username = os.getlogin()
        await self.request(f"set_user {username}")
        logger.debug(f"Interact with the daemon on behalf of user '{username}'")

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def _make_request(self, request):
        self.writer.write(request.encode("ascii") + b"\n")
        try:
            response = await self.reader.readuntil(b"#")
            return response[:-2].decode("ascii")
        except asyncio.IncompleteReadError as err:
            return err.partial.decode("ascii").strip()

    async def request(self, req):
        resp = json.loads(await self._make_request(req))
        if resp["status"] != STATUS_OK:
            raise FailedRequest(resp)
        return resp

    async def forward_serial(self, device):
        resp = await self.request(f"forward_serial {device}")
        port = int(resp["exec"].split(" ")[-1])
        return port

    async def release_device(self, device):
        await self.request(f"release_device {device}")


@contextmanager
def acquire_device(device, port=43500):
    async def acquire():
        async with Connection(port) as conn:
            return await conn.forward_serial(device)
    
    async def release():
        attempts = 5
        while attempts > 0:
            try:
                async with Connection(port) as conn:
                    await conn.release_device(device)
                    return
            except FailedRequest as err:
                logging.warning(f"Failed to release device {device}: {err.message}")
                return
            except:
                logging.exception(f"Failed to release device {device}")
                attempts -= 1
                await asyncio.sleep(1)
        logging.warning(f"Could not release device {device}")

    telnet_port = asyncio.run(acquire())
    yield Device(name=device, port=telnet_port)
    asyncio.run(release())


# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with acquire_device("/dev/ttyCAM1") as dev:
        print(dev.port)