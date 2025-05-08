# tests/test_eventPRIVMSG.py

import pytest
import asyncio
import random

import jokeBot
from jokeBot import Bot
from joker_utils import get_joke_sequence

class DummyWriter:
    def __init__(self):
        self.buffer = b""
    def write(self, data: bytes):
        self.buffer += data

@pytest.fixture
def bot(monkeypatch):
    # stub out sleeps so we don't actually wait during tests
    async def no_sleep(_):
        return
    monkeypatch.setattr(jokeBot.asyncio, "sleep", no_sleep)

    b = Bot()
    b.writer = DummyWriter()
    return b

@pytest.mark.asyncio
async def test_dm_help(bot):
    raw = f":alice!u@host PRIVMSG {bot.nickname} :help"
    await bot.eventPRIVMSG(raw)
    assert b"DM Commands" in bot.writer.buffer

@pytest.mark.asyncio
async def test_dm_who_are_you(bot):
    raw = f":alice!u@host PRIVMSG {bot.nickname} :who are you?"
    await bot.eventPRIVMSG(raw)
    assert b"JokerBot" in bot.writer.buffer

@pytest.mark.asyncio
async def test_ping_channel(bot):
    bot.last = 0
    raw = ":alice!u@host PRIVMSG #room :!ping"
    await bot.eventPRIVMSG(raw)
    assert b"Pong!" in bot.writer.buffer

@pytest.mark.asyncio
async def test_say_channel(bot):
    bot.last = 0
    raw = ":alice!u@host PRIVMSG #room :!say echo back"
    await bot.eventPRIVMSG(raw)
    assert b"echo back" in bot.writer.buffer

@pytest.mark.asyncio
async def test_mention_joke(bot, monkeypatch):
    # Force branch=0, idx=0 in the bot’s random logic
    calls = [0, 0]
    monkeypatch.setattr(jokeBot.random, "randint", lambda a, b: calls.pop(0))

    # Capture the sequence of action() calls
    recorded = []
    async def fake_action(target, msg):
        recorded.append(msg)
    monkeypatch.setattr(bot, "action", fake_action)

    # Use lowercase @joker so it matches msg.startswith('@joker')
    raw = ":alice!u@host PRIVMSG #room :@joker joke"
    await bot.eventPRIVMSG(raw)

    expected = get_joke_sequence(0, 0)
    assert recorded == expected
