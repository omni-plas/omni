"""Core model for the independent Omni language."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .lexer import Token, tokenize


class OmniKeyword(str, Enum):
    ENTITY = "entity"
    FUNCTION = "function"
    RETURN = "return"
    LET = "let"


@dataclass(frozen=True)
class OmniProgram:
    source: str
    tokens: tuple[Token, ...]

    @classmethod
    def parse(cls, source: str) -> "OmniProgram":
        if not isinstance(source, str):
            raise TypeError("Omni source must be text")
        return cls(source=source, tokens=tokenize(source))

    def keywords(self) -> tuple[OmniKeyword, ...]:
        values = {keyword.value: keyword for keyword in OmniKeyword}
        return tuple(values[token.text] for token in self.tokens if token.text in values)

    def identifiers(self) -> tuple[str, ...]:
        return tuple(token.text for token in self.tokens if token.kind == "identifier")

    def validate(self) -> None:
        if not self.source.strip():
            raise ValueError("Omni source must not be empty")
        if not self.tokens:
            raise ValueError("Omni source produced no tokens")

    def token_at(self, offset: int) -> Token:
        if not isinstance(offset, int) or isinstance(offset, bool):
            raise TypeError("offset must be an integer")
        for token in self.tokens:
            if token.start <= offset < token.end:
                return token
        raise IndexError(f"no token at source offset {offset}")
