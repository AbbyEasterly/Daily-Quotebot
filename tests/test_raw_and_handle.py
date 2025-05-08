import asyncio
import pytest
from jokeBot import Bot

class DummyWriter:
    def __init__(self):
        self.buffer = b""
    def write(self, data: bytes):
        self.buffer += data

@pytest.fixture
def bot():
    b = Bot()
    b.writer = DummyWriter()
    return b

def test_raw_truncates_and_adds_crlf(bot):
    long = "x" * 600
    asyncio.get_event_loop().run_until_complete(bot.raw(long))
    out = bot.writer.buffer
    assert out.endswith(b"\r\n")
    assert len(out) - 2 <= 510

@pytest.mark.asyncio
async def test_handle_ping(bot):
    await bot.handle("PING :irc.example.org")
    assert bot.writer.buffer == b"PONG :irc.example.org\r\n"
