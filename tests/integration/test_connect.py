# tests/integration/test_connect.py

import asyncio
import pytest
from types import SimpleNamespace
import jokeBot
from jokeBot import Bot

class FakeReader:
    def __init__(self):
        self._lines = [
            b"PING :irc.test\r\n",
            b"ERROR :Closing Link: banned\r\n"
        ]

    async def readuntil(self, sep=b"\r\n"):
        if self._lines:
            return self._lines.pop(0)
        # No more data → signal EOF to break out of inner loop
        raise asyncio.IncompleteReadError(partial=b"", expected=0)

    def at_eof(self):
        # Once _lines is empty, inner loop will exit into except/finally
        return not self._lines

class FakeWriter:
    def __init__(self):
        self.buffer = b""
    def write(self, data: bytes):
        self.buffer += data

@pytest.fixture(autouse=True)
def setup_args_and_sleep(monkeypatch):
    # 1) Provide a minimal args so connect() does USER/NICK
    jokeBot.args = SimpleNamespace(
        server="irc.test",
        channel="#room",
        password=None,
        port=None,
        ssl=False,
        v4=False,
        v6=False,
        vhost=None,
        key=None
    )
    # 2) Stub out that 30‑second reconnect sleep
    async def no_sleep(_):
        return
    monkeypatch.setattr(jokeBot.asyncio, "sleep", no_sleep)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_connect_does_handshake_and_pong(monkeypatch):
    bot = Bot()
    fake_reader = FakeReader()
    fake_writer = FakeWriter()

    async def fake_open_connection(**kwargs):
        return fake_reader, fake_writer

    monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)

    # Wrap in wait_for so we don't hang—timeout after 1 second
    await asyncio.wait_for(bot.connect(), timeout=1)

    out = fake_writer.buffer.decode()
    # It should have sent the USER/NICK lines...
    assert "USER Joker" in out
    assert "NICK Joker" in out
    # ...and it should have replied to PING
    assert "PONG :irc.test" in out
