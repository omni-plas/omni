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
        return cls(source=source, tokens=tokenize(source))

    def keywords(self) -> tuple[OmniKeyword, ...]:
        values = {keyword.value: keyword for keyword in OmniKeyword}
        return tuple(values[token.text] for token in self.tokens if token.text in values)

    def validate(self) -> None:
        if not self.source.strip():
            raise ValueError("Omni source must not be empty")
