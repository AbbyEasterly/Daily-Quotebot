
#!/usr/bin/env python3
import argparse
import asyncio
import logging
import logging.handlers
import ssl
import time

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
        self.nickname = 'skeleton'
        self.username = 'skelly'
        self.realname = 'Development Bot'
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
            await self.sendmsg(nick, 'Do NOT message me!')
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
                    self.last = time.time()

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

    setup_logger('skeleton', to_file=True)
    bot = Bot()
    asyncio.run(bot.connect())
