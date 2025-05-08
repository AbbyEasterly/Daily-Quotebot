# joker_utils.py

import string
import random
import pandas as pd

_KNOCK_KNOCK = [
    {"Setup": "Knock knock", "Response": "Lettuce", "Punchline": "Lettuce in, it’s cold out here!"},
    {"Setup": "Knock knock", "Response": "Cow says", "Punchline": "Cow says mooo!"},
    # … the other 8 entries …
]
_QA_JOKES = [
    ("Why don’t skeletons fight each other?", "They don’t have the guts."),
    ("What did the janitor say when he jumped out of the closet?", "Supplies!"),
    # … the other 8 entries …
]

def parse_privmsg(data: str):
    parts  = data.split()
    ident  = parts[0][1:]
    nick   = ident.split("!",1)[0]
    target = parts[2]
    msg    = " ".join(parts[3:])[1:]
    return ident, nick, target, msg

def clean(msg: str) -> str:
    return msg.strip().lower()

def is_punctuation_only(cleaned: str) -> bool:
    return all(ch in string.punctuation for ch in cleaned)

def is_spam(cleaned: str) -> bool:
    return len(cleaned) > 5 and len(set(cleaned)) == 1

def is_gibberish(cleaned: str) -> bool:
    return not any(ch.isalnum() for ch in cleaned)

def is_help(cleaned: str) -> bool:
    return cleaned == "help"

def is_simple_joke_request(cleaned: str) -> bool:
    return cleaned == "joke"

def is_who_are_you(cleaned: str) -> bool:
    return cleaned in ("who are you?", "who are you", "who r u", "who r u?")

def is_mention_joke(cleaned: str) -> bool:
    return "joke" in cleaned and cleaned != "joke"

def get_joke_sequence(randkind: int, idx: int):
    if randkind == 0:
        e = _KNOCK_KNOCK[idx]
        return [
            e["Setup"],
            "(who's there)",
            e["Response"],
            f"({e['Response']} who?)",
            e["Punchline"],
        ]
    else:
        q,a = _QA_JOKES[idx]
        return [q, "...", a]

def choose_joke():
    return random.randint(0,1), random.randint(0,9)
