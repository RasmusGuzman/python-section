from __future__ import annotations
from abc import abstractmethod, ABC
import enum
from dataclasses import dataclass
from typing import Callable


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()

@dataclass
class JsonMessage:
    message_type: MessageType
    payload: dict

@dataclass
class ParsedMessage:
    source: MessageType
    text: str
    user_id: str
    chat_id: str
    timestamp: float

class MessageParser(ABC):
    def __init__(self, message: JsonMessage):
        self.message = message

    @abstractmethod
    def parse(self) -> ParsedMessage:
        pass

class ParserFactory:
    def __init__(self):
        self._registry: dict[MessageType, type[MessageParser]] = {}

    def register(self, message_type: MessageType) -> Callable:
        def decorator(cls: type[MessageParser]) -> type[MessageParser]:
            if message_type in self._registry:
                raise ValueError(f"Parser for {message_type} already registered")
            self._registry[message_type] = cls
            return cls
        return decorator

    def get_parser(self, message: JsonMessage) -> MessageParser:
        parser_cls = self._registry.get(message.message_type)
        if not parser_cls:
            raise ValueError(f"No parser found for {message.message_type}")
        return parser_cls(message)

message_factory = ParserFactory()

@message_factory.register(MessageType.TELEGRAM)
class TelegramParser(MessageParser):
    def parse(self) -> ParsedMessage:
        payload = self.message.payload
        return ParsedMessage(
            source=self.message.message_type,
            text=payload['message'],
            user_id=str(payload['from']['id']),
            chat_id=str(payload['chat']['id']),
            timestamp=payload['date']
        )

@message_factory.register(MessageType.MATTERMOST)
class MattermostParser(MessageParser):
    def parse(self) -> ParsedMessage:
        payload = self.message.payload
        return ParsedMessage(
            source=self.message.message_type,
            text=payload['message'],
            user_id=payload['user_id'],
            chat_id=payload['channel_id'],
            timestamp=payload['create_at']
        )

@message_factory.register(MessageType.SLACK)
class SlackParser(MessageParser):
    def parse(self) -> ParsedMessage:
        payload = self.message.payload
        return ParsedMessage(
            source=self.message.message_type,
            text=payload['text'],
            user_id=payload['user'],
            chat_id=payload['channel'],
            timestamp=payload['ts']
        )
