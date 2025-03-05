
import asyncio
import websockets
import datetime


class IRCBot:
    def __init__(self, server: str, port: int, nickname: str, channel: str):
        """
        Initializes the IRC bot with connection details.
        :param server: IRC server address
        :param port: IRC server port
        :param nickname: Bot's nickname
        :param channel: Channel to join
        """
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.websocket = None

    async def connect(self):
        """
        Establishes a connection to the IRC server and joins the channel.
        """
        try:
            print(f"Connecting to {self.server}:{self.port}...")
            self.websocket = await websockets.connect(f"ws://{self.server}:{self.port}")
            await self.raw(f"NICK {self.nickname}")
            await self.raw(f"USER {self.nickname} 0 * :{self.nickname}")
            await asyncio.sleep(1)
            await self.raw(f"JOIN {self.channel}")
            print(f"Joined {self.channel} as {self.nickname}")
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)
            await self.connect()  # Attempt reconnection

    async def raw(self, data: str):
        """
        Sends a raw command to the IRC server.
        """
        if self.websocket:
            await self.websocket.send(data + "\r\n")

    async def sendmsg(self, target: str, msg: str):
        """
        Sends a message to a channel or user.
        :param target: The recipient (channel or user)
        :param msg: The message to send
        """
        await self.raw(f"PRIVMSG {target} :{msg}")

    async def log_message(self, data: str):
        """
        Logs messages received from the server.
        """
        with open("chat_log.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} - {data}\n")

    async def eventPRIVMSG(self, data: str):
        """
        Handles incoming messages and responds to specific keywords.
        """
        parts = data.split(" ", 3)
        if len(parts) > 3:
            sender = parts[0].split("!")[0][1:]
            message = parts[3][1:].strip()
