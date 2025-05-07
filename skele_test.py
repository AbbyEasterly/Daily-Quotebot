#edits of jokeBot but still changing DON'T DELETE EITHER ONE


#!/usr/bin/env python3
import argparse
import asyncio
import logging
import logging.handlers
import ssl
import time
import re
import pandas as pd
import random
import string
# === Settings ===
cmd_flood = 3

bold = '\x02'; italic = '\x1D'; underline = '\x1F'; reverse = '\x16'; reset = '\x0f'
red = '04'

def color(msg: str, foreground: str, background: str = None) -> str:
    return f'\x03{foreground},{background}{msg}{reset}' if background else f'\x03{foreground}{msg}{reset}'

def ssl_ctx(verify=False, cert_path=None, cert_pass=None) -> ssl.SSLContext:
    ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()
    if cert_path:
        ctx.load_cert_chain(cert_path) if not cert_pass else ctx.load_cert_chain(cert_path, cert_pass)
    return ctx

class Bot():







    def __init__(self):
        self.nickname = 'Joker'
        self.username = 'JokerBot'
        self.realname = 'Joker ChatBot'
        self.reader = None
        self.writer = None
        self.last = time.time()
        self.slow = False


    async def action(self, chan, msg):
        await self.sendmsg(chan, f'\x01ACTION {msg}\x01')

    async def raw(self, data):
        self.writer.write(data[:510].encode('utf-8') + b'\r\n')

    async def sendmsg(self, target, msg):
        await self.raw(f'PRIVMSG {target} :{msg}')



    async def connect(self):
        while True:
            try:
                options = {
                    'host': args.server,
                    'port': args.port or (6697 if args.ssl else 6667),
                    'ssl': ssl_ctx() if args.ssl else None,
                    'family': 10 if args.v6 else 2,
                    'local_addr': args.vhost or None
                }
                self.reader, self.writer = await asyncio.wait_for(asyncio.open_connection(**options), 15)

                if args.password:
                    await self.raw('PASS ' + args.password)
                await self.raw(f'USER {self.username} 0 * :{self.realname}')
                await self.raw('NICK ' + self.nickname)

                while not self.reader.at_eof():
                    data = await asyncio.wait_for(self.reader.readuntil(b'\r\n'), 300)
                    await self.handle(data.decode('utf-8').strip())

            except Exception as ex:
                logging.error(f'Connection failed to {args.server}: {ex}')
            finally:
                await asyncio.sleep(30)


    async def eventPRIVMSG(self, data):
        parts = data.split()
        ident = parts[0][1:]
        nick = parts[0].split('!')[0][1:]
        target = parts[2]
        msg = ' '.join(parts[3:])[1:]

        if target == self.nickname:
            cleaned = msg.strip().lower()
            is_punctuation_only = all(char in string.punctuation for char in cleaned)
            is_spam = len(set(cleaned)) == 1 and len(cleaned) > 5
            is_gibberish = not any(char.isalnum() for char in cleaned)
            if len(cleaned) > 400:
                await self.sendmsg(nick, "Whoa!, Thats a bit too much for me to handle in one go. Try breaking it up.")

            elif cleaned == "help":
                await self.sendmsg(nick, "DM Commands: try typing 'joke' or 'who are you?'")
                return
            elif cleaned == "joke":
                await self.sendmsg(nick, "I'm better with jokes in the main channel. - try @joker joke")

            elif cleaned in ["who are you?", "who are you", "who r u", "who r u?"]:
                await self.sendmsg(nick, "I'm JokerBot - joke-telling, message-wrangling IRC assistant!")

            elif "joke" in cleaned:

                jokes_split = [
                    ("Why don’t skeletons fight each other?", "They don’t have the guts."),
                    ("What did the janitor say when he jumped out of the closet?", "Supplies!"),
                    ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
                    ("What do you call fake spaghetti?", "An impasta."),
                    ("Why can't you give Elsa a balloon?", "Because she’ll let it go."),
                    ("I told my wife she was drawing her eyebrows too high...", "She looked surprised."),
                    ("Parallel lines have so much in common...", "It’s a shame they’ll never meet."),
                    ("Why did the coffee file a police report?", "It got mugged."),
                    ("What’s orange and sounds like a parrot?", "A carrot."),
                    ("Why don’t some couples go to the gym?", "Because some relationships don’t work out.")
                ]
                jokes = [
                    {"Setup": "Knock knock", "Response": "Lettuce", "Punchline": "Lettuce in, it’s cold out here!"},
                    {"Setup": "Knock knock", "Response": "Cow says", "Punchline": "Cow says mooo!"},
                    {"Setup": "Knock knock", "Response": "Boo", "Punchline": "Aw, don’t cry—it’s just a joke!"},
                    {"Setup": "Knock knock", "Response": "Tank", "Punchline": "You’re welcome!"},
                    {"Setup": "Knock knock", "Response": "Atch", "Punchline": "Bless you!"},
                    {"Setup": "Knock knock", "Response": "Olive", "Punchline": "Olive you and I miss you!"},
                    {"Setup": "Knock knock", "Response": "Dishes", "Punchline": "Dishes the police—open up!"},
                    {"Setup": "Knock knock", "Response": "Nana", "Punchline": "Nana your business!"},
                    {"Setup": "Knock knock", "Response": "Broken Pencil", "Punchline": "Never mind, it’s pointless."},
                    {"Setup": "Knock knock", "Response": "Ya", "Punchline": "No thanks, I use Google."},
                ]
                randkind = random.randint(0, 1)
                random_number = random.randint(0, 9)
                if randkind == 0:
                    # Convert to a DataFrame
                    jokes_df = pd.DataFrame(jokes)
                    await self.action(nick, jokes_df.iloc[random_number]["Setup"])
                    await self.action(nick, "(who's there)")
                    await asyncio.sleep(4)

                    y = jokes_df.iloc[random_number]["Response"]
                    await self.action(nick, y)
                    await self.action(nick, ("(" + y + " who?)"))
                    await asyncio.sleep(4)

                    await self.action(nick, (jokes_df.iloc[random_number]["Punchline"]))
                # Display the DataFrame
                else:
                    df = pd.DataFrame(jokes_split, columns=["Question", "Answer"])

                    await self.action(nick, df.iloc[random_number]["Question"])
                    await asyncio.sleep(2)
                    await self.action(nick, "...")
                    await asyncio.sleep(2)
                    await self.action(nick, df.iloc[random_number]["Answer"])





            elif cleaned == "":
                await self.sendmsg(nick, "Did you forget to say something?")
            elif 'hey'  in cleaned or 'hi'  in cleaned or 'hello' in cleaned:
                await self.action(nick, "hi!")
            elif "haha" in cleaned or "lol" in cleaned or 'funny' in cleaned:
                await self.sendmsg(nick, "Thanks")
            elif "lol" in cleaned:
                await self.sendmsg(nick, "Thanks")
            elif is_punctuation_only:
                await self.sendmsg(nick, "All punctuation and no words makes Jack a dull bot.")
            elif is_spam:
                await self.sendmsg(nick, "That's a lot of the same thing. You okay?")
            elif is_gibberish:
                await self.sendmsg(nick, "I'm gonna need more than symbols to help you out.")
            else:
                await self.sendmsg(nick, "I'm not sure what you meant. Try !help or ask me for a joke!")


        elif target.startswith('#'):
            if msg.startswith('!'):

                if time.time() - self.last < cmd_flood:
                    if not self.slow:
                        self.slow = True
                        await self.sendmsg(target, color('Slow down nerd!', red))
                else:
                    self.slow = False
                    if msg == '!help':
                        await self.action(target, 'explodes')
                    elif msg == '!ping':
                        await self.sendmsg(target, 'Pong!')
                    elif msg.startswith('!say') and len(msg.split()) > 1:
                        await self.sendmsg(target, ' '.join(msg.split()[1:]))
                    else:
                        await self.sendmsg(target,f"{nick}: That command is not recognized. Try !help for what I can do.")
                    self.last = time.time()


            elif msg.startswith('@joker'):

                cleaned = msg.strip().lower()
                cleaned = cleaned.replace("@joker", "")
                print(cleaned)

                is_punctuation_only = all(char in string.punctuation for char in cleaned)

                is_spam = len(set(cleaned)) == 1 and len(cleaned) > 5

                is_gibberish = not any(char.isalnum() for char in cleaned)

                if len(cleaned) > 400:

                    await self.sendmsg(target,
                                       "Whoa!, Thats a bit too much for me to handle in one go. Try breaking it up.")


                elif cleaned == "help":

                    await self.sendmsg(target, "DM Commands: try typing 'joke' or 'who are you?'")

                    return

                elif cleaned == "joke":

                    await self.sendmsg(target, "I'm better with jokes in the main channel. - try @joker joke")


                elif cleaned in ["who are you?", "who are you", "who r u", "who r u?"]:

                    await self.sendmsg(target, "I'm JokerBot - joke-telling, message-wrangling IRC assistant!")


                elif "joke" in cleaned:

                    jokes_split = [

                        ("Why don’t skeletons fight each other?", "They don’t have the guts."),

                        ("What did the janitor say when he jumped out of the closet?", "Supplies!"),

                        ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),

                        ("What do you call fake spaghetti?", "An impasta."),

                        ("Why can't you give Elsa a balloon?", "Because she’ll let it go."),

                        ("I told my wife she was drawing her eyebrows too high...", "She looked surprised."),

                        ("Parallel lines have so much in common...", "It’s a shame they’ll never meet."),

                        ("Why did the coffee file a police report?", "It got mugged."),

                        ("What’s orange and sounds like a parrot?", "A carrot."),

                        ("Why don’t some couples go to the gym?", "Because some relationships don’t work out.")

                    ]

                    jokes = [

                        {"Setup": "Knock knock", "Response": "Lettuce", "Punchline": "Lettuce in, it’s cold out here!"},

                        {"Setup": "Knock knock", "Response": "Cow says", "Punchline": "Cow says mooo!"},

                        {"Setup": "Knock knock", "Response": "Boo", "Punchline": "Aw, don’t cry—it’s just a joke!"},

                        {"Setup": "Knock knock", "Response": "Tank", "Punchline": "You’re welcome!"},

                        {"Setup": "Knock knock", "Response": "Atch", "Punchline": "Bless you!"},

                        {"Setup": "Knock knock", "Response": "Olive", "Punchline": "Olive you and I miss you!"},

                        {"Setup": "Knock knock", "Response": "Dishes", "Punchline": "Dishes the police—open up!"},

                        {"Setup": "Knock knock", "Response": "Nana", "Punchline": "Nana your business!"},

                        {"Setup": "Knock knock", "Response": "Broken Pencil",
                         "Punchline": "Never mind, it’s pointless."},

                        {"Setup": "Knock knock", "Response": "Ya", "Punchline": "No thanks, I use Google."},

                    ]

                    randkind = random.randint(0, 1)

                    random_number = random.randint(0, 9)

                    if randkind == 0:

                        # Convert to a DataFrame

                        jokes_df = pd.DataFrame(jokes)

                        await self.action(target, jokes_df.iloc[random_number]["Setup"])

                        await self.action(target, "(who's there)")

                        await asyncio.sleep(4)

                        y = jokes_df.iloc[random_number]["Response"]

                        await self.action(target, y)

                        await self.action(target, ("(" + y + " who?)"))

                        await asyncio.sleep(4)

                        await self.action(target, (jokes_df.iloc[random_number]["Punchline"]))

                    # Display the DataFrame

                    else:

                        df = pd.DataFrame(jokes_split, columns=["Question", "Answer"])

                        await self.action(target, df.iloc[random_number]["Question"])

                        await asyncio.sleep(2)

                        await self.action(target, "...")

                        await asyncio.sleep(2)

                        await self.action(target, df.iloc[random_number]["Answer"])






                elif cleaned == "":

                    await self.sendmsg(target, "Did you forget to say something?")

                elif 'hey' in cleaned or 'hi' in cleaned or 'hello' in cleaned:

                    await self.action(target, "hi!")

                elif "haha" in cleaned or "lol" in cleaned or 'funny' in cleaned:

                    await self.sendmsg(target, "Thanks")

                elif "lol" in cleaned:

                    await self.sendmsg(target, "Thanks")

                elif is_punctuation_only:

                    await self.sendmsg(target, "All punctuation and no words makes Jack a dull bot.")

                elif is_spam:

                    await self.sendmsg(target, "That's a lot of the same thing. You okay?")

                elif is_gibberish:

                    await self.sendmsg(target, "I'm gonna need more than symbols to help you out.")

                else:

                    await self.sendmsg(target,
                                       f"{nick}: I'm not sure what you meant - type !help or ask me for a joke.")

    async def handle(self, data):
        logging.info(data)
        try:
            parts = data.split()
            if data.startswith('ERROR :Closing Link:'):
                raise Exception('BANNED')
            if parts[0] == 'PING':
                await self.raw('PONG ' + parts[1])
            elif parts[1] == '001':
                await self.raw(f'MODE {self.nickname} +B')
                # Commented out for now: NickServ and OPER (used in testing)
                # await self.sendmsg('NickServ', f'IDENTIFY {self.nickname} simps0nsfan420')
                # await self.raw('OPER MrSysadmin fartsimps0n1337')
                await asyncio.sleep(10)
                if hasattr(args, 'key') and args.key:
                    await self.raw(f'JOIN {args.channel} {args.key}')
                else:
                    await self.raw(f'JOIN {args.channel}')
                await self.sendmsg(args.channel, "Hello, everyone! Joker is alive.")
                await self.sendmsg(args.channel, f'Ask me for a joke (start line with @{self.nickname} to address me) or ask help for details')

            elif parts[1] == '433':
                self.nickname += '_'
                await self.raw('NICK ' + self.nickname)
            elif parts[1] == 'INVITE':
                target = parts[2]
                chan = parts[3][1:]
                if target == self.nickname:
                    await self.raw(f'JOIN {chan}')
            elif parts[1] == 'KICK':
                chan = parts[2]
                kicked = parts[3]
                if kicked == self.nickname:
                    await asyncio.sleep(3)
                    await self.raw(f'JOIN {chan}')
            elif parts[1] == 'PRIVMSG':
                await self.eventPRIVMSG(data)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        except Exception as ex:
            logging.exception(f'Unknown error occurred! ({ex})')

def setup_logger(log_filename: str, to_file: bool = False):
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)9s | %(message)s', '%I:%M %p'))
    if to_file:
        fh = logging.handlers.RotatingFileHandler(log_filename + '.log', maxBytes=250000, backupCount=3, encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)9s | %(filename)s.%(funcName)s.%(lineno)d | %(message)s', '%Y-%m-%d %I:%M %p'))
        logging.basicConfig(level=logging.NOTSET, handlers=(sh, fh))
    else:
        logging.basicConfig(level=logging.NOTSET, handlers=(sh,))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connect to an IRC server.")
    parser.add_argument("server", help="The IRC server address.")
    parser.add_argument("channel", help="The IRC channel to join.")
    parser.add_argument("--password", help="The password for the IRC server.")
    parser.add_argument("--port", type=int, help="The port number (default: 6667 or 6697 with SSL).")
    parser.add_argument("--ssl", action="store_true", help="Use SSL.")
    parser.add_argument("--v4", action="store_true", help="Use IPv4.")
    parser.add_argument("--v6", action="store_true", help="Use IPv6.")
    parser.add_argument("--key", default="", help="Channel key if required.")
    parser.add_argument("--vhost", help="Bind to a specific local host address.")
    args = parser.parse_args()

    print(f"Connecting to {args.server}:{args.port or ('6697' if args.ssl else '6667')} (SSL: {args.ssl}) and joining {args.channel} (Key: {args.key or 'None'})")

    setup_logger('Joker', to_file=True)
    bot = Bot()
    asyncio.run(bot.connect())
