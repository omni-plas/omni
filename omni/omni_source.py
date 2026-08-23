"""Core tokenizer and parser for the textual Omni language.

The grammar is intentionally small but real: declarations, integer/string/
bool literals, identifiers, calls, arithmetic expressions, and return
statements are parsed into a deterministic AST. It is independent of Python
compiler infrastructure and is suitable as the foundation for self-hosting.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OmniSyntaxError(ValueError):
    pass


class TokenKind(str, Enum):
    IDENT = "ident"
    INTEGER = "integer"
    STRING = "string"
    TRUE = "true"
    FALSE = "false"
    FN = "fn"
    LET = "let"
    RETURN = "return"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    EQUAL = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    EOF = "eof"


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    line: int
    column: int


@dataclass(frozen=True)
class Literal:
    value: int | str | bool


@dataclass(frozen=True)
class Name:
    value: str


@dataclass(frozen=True)
class Binary:
    left: object
    operator: TokenKind
    right: object


@dataclass(frozen=True)
class Call:
    callee: str
    arguments: tuple[object, ...]


@dataclass(frozen=True)
class Let:
    name: str
    value: object


@dataclass(frozen=True)
class Return:
    value: object


@dataclass(frozen=True)
class Function:
    name: str
    parameters: tuple[str, ...]
    body: tuple[object, ...]


@dataclass(frozen=True)
class Program:
    functions: tuple[Function, ...]


_KEYWORDS = {
    "fn": TokenKind.FN,
    "let": TokenKind.LET,
    "return": TokenKind.RETURN,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
}


def tokenize(source: str) -> tuple[Token, ...]:
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    tokens: list[Token] = []
    i = 0
    line = column = 1
    while i < len(source):
        ch = source[i]
        if ch in " \t\r":
            i += 1; column += 1; continue
        if ch == "\n":
            i += 1; line += 1; column = 1; continue
        if source.startswith("//", i):
            while i < len(source) and source[i] != "\n":
                i += 1; column += 1
            continue
        start_line, start_column = line, column
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < len(source) and (source[j].isalnum() or source[j] == "_"):
                j += 1
            text = source[i:j]
            tokens.append(Token(_KEYWORDS.get(text, TokenKind.IDENT), text, start_line, start_column))
            column += j - i; i = j; continue
        if ch.isdigit():
            j = i + 1
            while j < len(source) and source[j].isdigit(): j += 1
            tokens.append(Token(TokenKind.INTEGER, source[i:j], start_line, start_column))
            column += j - i; i = j; continue
        if ch == '"':
            j = i + 1
            escaped = False
            while j < len(source):
                if source[j] == '"' and not escaped: break
                if source[j] == "\n" and not escaped:
                    raise OmniSyntaxError(f"unterminated string at {start_line}:{start_column}")
                escaped = source[j] == "\\" and not escaped
                if source[j] != "\\": escaped = False
                j += 1
            if j >= len(source): raise OmniSyntaxError(f"unterminated string at {start_line}:{start_column}")
            raw = source[i:j + 1]
            try:
                import json
                value = json.loads(raw)
            except Exception as exc:
                raise OmniSyntaxError(f"invalid string at {start_line}:{start_column}") from exc
            tokens.append(Token(TokenKind.STRING, value, start_line, start_column))
            column += j + 1 - i; i = j + 1; continue
        punctuation = {
            "(": TokenKind.LPAREN, ")": TokenKind.RPAREN, "{": TokenKind.LBRACE, "}": TokenKind.RBRACE,
            ",": TokenKind.COMMA, ":": TokenKind.COLON, ";": TokenKind.SEMICOLON, "=": TokenKind.EQUAL,
            "+": TokenKind.PLUS, "-": TokenKind.MINUS, "*": TokenKind.STAR, "/": TokenKind.SLASH,
        }
        kind = punctuation.get(ch)
        if kind is None: raise OmniSyntaxError(f"unexpected character {ch!r} at {line}:{column}")
        tokens.append(Token(kind, ch, line, column)); i += 1; column += 1
    tokens.append(Token(TokenKind.EOF, "", line, column))
    return tuple(tokens)


class Parser:
    def __init__(self, tokens: tuple[Token, ...]): self.tokens, self.index = tokens, 0
    def current(self) -> Token: return self.tokens[self.index]
    def take(self, kind: TokenKind) -> Token:
        token = self.current()
        if token.kind != kind: raise OmniSyntaxError(f"expected {kind.value}, got {token.kind.value} at {token.line}:{token.column}")
        self.index += 1; return token
    def accept(self, kind: TokenKind) -> bool:
        if self.current().kind == kind: self.index += 1; return True
        return False
    def parse(self) -> Program:
        functions = []
        while self.current().kind != TokenKind.EOF: functions.append(self.function())
        return Program(tuple(functions))
    def function(self) -> Function:
        self.take(TokenKind.FN); name = self.take(TokenKind.IDENT).text; self.take(TokenKind.LPAREN)
        params = []
        if self.current().kind != TokenKind.RPAREN:
            while True:
                params.append(self.take(TokenKind.IDENT).text)
                if not self.accept(TokenKind.COMMA): break
        self.take(TokenKind.RPAREN); self.take(TokenKind.LBRACE)
        body = []
        while self.current().kind != TokenKind.RBRACE:
            if self.current().kind == TokenKind.LET:
                self.take(TokenKind.LET); var = self.take(TokenKind.IDENT).text; self.take(TokenKind.EQUAL); body.append(Let(var, self.expression())); self.accept(TokenKind.SEMICOLON); continue
            if self.current().kind == TokenKind.RETURN:
                self.take(TokenKind.RETURN); body.append(Return(self.expression())); self.accept(TokenKind.SEMICOLON); continue
            raise OmniSyntaxError(f"expected statement at {self.current().line}:{self.current().column}")
        self.take(TokenKind.RBRACE); return Function(name, tuple(params), tuple(body))
    def expression(self):
        node = self.term()
        while self.current().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self.current().kind; self.index += 1; node = Binary(node, op, self.term())
        return node
    def term(self):
        node = self.primary()
        while self.current().kind in (TokenKind.STAR, TokenKind.SLASH):
            op = self.current().kind; self.index += 1; node = Binary(node, op, self.primary())
        return node
    def primary(self):
        token = self.current()
        if token.kind == TokenKind.INTEGER: self.index += 1; return Literal(int(token.text))
        if token.kind == TokenKind.STRING: self.index += 1; return Literal(token.text)
        if token.kind in (TokenKind.TRUE, TokenKind.FALSE): self.index += 1; return Literal(token.kind == TokenKind.TRUE)
        if token.kind == TokenKind.IDENT:
            self.index += 1
            if self.accept(TokenKind.LPAREN):
                args = []
                if self.current().kind != TokenKind.RPAREN:
                    while True:
                        args.append(self.expression())
                        if not self.accept(TokenKind.COMMA): break
                self.take(TokenKind.RPAREN); return Call(token.text, tuple(args))
            return Name(token.text)
        if self.accept(TokenKind.LPAREN):
            node = self.expression(); self.take(TokenKind.RPAREN); return node
        raise OmniSyntaxError(f"expected expression at {token.line}:{token.column}")


def parse(source: str) -> Program:
    return Parser(tokenize(source)).parse()
