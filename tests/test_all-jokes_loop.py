import pytest
import asyncio

import jokeBot
from jokeBot import Bot

class DummyWriter:
    def __init__(self):
        self.buffer = b""
    def write(self, data: bytes):
        self.buffer += data

@pytest.fixture
def bot(monkeypatch):
    # stub out sleep
    async def no_sleep(_): return
    monkeypatch.setattr(jokeBot.asyncio, "sleep", no_sleep)
    b = Bot()
    b.writer = DummyWriter()
    return b

@pytest.mark.asyncio
async def test_every_joke_sends_output(bot, monkeypatch):
    total = 0
    for branch in (0, 1):
        for idx in range(10):   # assumes you have 10 jokes in each list
            seq = [branch, idx]
            monkeypatch.setattr(jokeBot.random, "randint", lambda a,b, seq=seq: seq.pop(0))

            bot.writer.buffer = b""
            data = ":u!h PRIVMSG #room :@joker joke"
            await bot.eventPRIVMSG(data)

            assert bot.writer.buffer, f"No output for branch={branch}, idx={idx}"
            total += 1

    assert total == 20
