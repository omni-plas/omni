"""Small language-neutral lexical layer used by Omni-owned frontends."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("token source span is invalid")
        if self.end == self.start:
            raise ValueError("token source span cannot be empty")


def tokenize(source: str) -> tuple[Token, ...]:
    """Tokenize universal punctuation, identifiers, numbers and strings.

    Language-specific frontends may layer their own keyword and grammar rules
    on these stable source spans; Omni never invokes an external compiler.
    """
    if not isinstance(source, str):
        raise TypeError("source must be text")
    tokens: list[Token] = []
    i = 0
    while i < len(source):
        char = source[i]
        if char.isspace():
            i += 1
            continue
        if char.isalpha() or char == "_":
            start = i
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            tokens.append(Token("identifier", source[start:i], start, i))
            continue
        if char.isdigit():
            start = i
            i += 1
            while i < len(source) and source[i].isdigit():
                i += 1
            tokens.append(Token("number", source[start:i], start, i))
            continue
        if char in "'\"":
            quote = char
            start = i
            i += 1
            while i < len(source) and source[i] != quote:
                if source[i] == "\\" and i + 1 < len(source):
                    i += 2
                else:
                    i += 1
            if i >= len(source):
                raise ValueError(f"unterminated string at {start}")
            i += 1
            tokens.append(Token("string", source[start:i], start, i))
            continue
        tokens.append(Token("punctuation", char, i, i + 1))
        i += 1
    return tuple(tokens)
