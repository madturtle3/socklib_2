import enum
import dataclasses

PORT = 10643


class InfoTypes(enum.Enum):
    connections = 0
    past_messages = 1


"""
This is the momma class for all the messages.
Now you might be thinking: Mason??? Doing inheritance???? I thought he hates inheritance?
I do. However, it seemed really nice to have it here, especially cuz the Message structure
is a hierarchy of information by nature. So it fits. BUT I AM VERY WARY ABOUT IT!!!!!
"""


@dataclasses.dataclass
class Message:
    pass


@dataclasses.dataclass
class ChatMsg(Message):
    dest: str | None
    msg: str
    src: str = ""
    """Set by the server, will be overriden if set on client side."""


@dataclasses.dataclass
class InitMsg(Message):
    username: str


@dataclasses.dataclass
class InfoMsg(Message):
    information_to_get: InfoTypes
