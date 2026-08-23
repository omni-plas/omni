"""Core tokenizer and parser for the textual Omni language."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class OmniSyntaxError(ValueError): pass
class TokenKind(str, Enum):
    IDENT="ident"; INTEGER="integer"; STRING="string"; TRUE="true"; FALSE="false"
    FN="fn"; LET="let"; RETURN="return"; IF="if"; ELSE="else"; WHILE="while"
    LPAREN="("; RPAREN=")"; LBRACE="{"; RBRACE="}"; COMMA=","; COLON=":"; SEMICOLON=";"; EQUAL="="
    PLUS="+"; MINUS="-"; STAR="*"; SLASH="/"; EQEQ="=="; NE="!="; LT="<"; LE="<="; GT=">"; GE=">="; AND="&&"; OR="||"; NOT="!"; EOF="eof"
@dataclass(frozen=True)
class Token: kind:TokenKind; text:str; line:int; column:int
@dataclass(frozen=True)
class Literal: value:int|str|bool
@dataclass(frozen=True)
class Name: value:str
@dataclass(frozen=True)
class Binary: left:object; operator:TokenKind; right:object
@dataclass(frozen=True)
class Unary: operator:TokenKind; operand:object
@dataclass(frozen=True)
class Call: callee:str; arguments:tuple[object,...]
@dataclass(frozen=True)
class Let: name:str; value:object
@dataclass(frozen=True)
class Return: value:object
@dataclass(frozen=True)
class If: condition:object; then_body:tuple[object,...]; else_body:tuple[object,...]
@dataclass(frozen=True)
class While: condition:object; body:tuple[object,...]
@dataclass(frozen=True)
class Function: name:str; parameters:tuple[str,...]; body:tuple[object,...]
@dataclass(frozen=True)
class Program: functions:tuple[Function,...]
_KEYWORDS={"fn":TokenKind.FN,"let":TokenKind.LET,"return":TokenKind.RETURN,"true":TokenKind.TRUE,"false":TokenKind.FALSE,"if":TokenKind.IF,"else":TokenKind.ELSE,"while":TokenKind.WHILE}

def tokenize(source:str)->tuple[Token,...]:
    if not isinstance(source,str): raise TypeError("source must be a string")
    tokens=[]; i=0; line=column=1
    two={"==":TokenKind.EQEQ,"!=":TokenKind.NE,"<=":TokenKind.LE,">=":TokenKind.GE,"&&":TokenKind.AND,"||":TokenKind.OR}
    one={"(":TokenKind.LPAREN,")":TokenKind.RPAREN,"{":TokenKind.LBRACE,"}":TokenKind.RBRACE,",":TokenKind.COMMA,";":TokenKind.SEMICOLON,"=":TokenKind.EQUAL,"+":TokenKind.PLUS,"-":TokenKind.MINUS,"*":TokenKind.STAR,"/":TokenKind.SLASH,"<":TokenKind.LT,">":TokenKind.GT,"!":TokenKind.NOT}
    while i<len(source):
        ch=source[i]
        if ch in " \t\r": i+=1; column+=1; continue
        if ch=="\n": i+=1; line+=1; column=1; continue
        if source.startswith("//",i):
            while i<len(source) and source[i]!="\n": i+=1; column+=1
            continue
        sl,sc=line,column; pair=source[i:i+2]
        if pair in two: tokens.append(Token(two[pair],pair,sl,sc)); i+=2; column+=2; continue
        if ch.isalpha() or ch=="_":
            j=i+1
            while j<len(source) and (source[j].isalnum() or source[j]=="_"): j+=1
            text=source[i:j]; tokens.append(Token(_KEYWORDS.get(text,TokenKind.IDENT),text,sl,sc)); column+=j-i; i=j; continue
        if ch.isdigit():
            j=i+1
            while j<len(source) and source[j].isdigit(): j+=1
            tokens.append(Token(TokenKind.INTEGER,source[i:j],sl,sc)); column+=j-i; i=j; continue
        if ch=='"':
            j=i+1; escaped=False
            while j<len(source):
                if source[j]=='"' and not escaped: break
                if source[j]=='\n' and not escaped: raise OmniSyntaxError(f"unterminated string at {sl}:{sc}")
                escaped=source[j]=='\\' and not escaped
                if source[j]!='\\': escaped=False
                j+=1
            if j>=len(source): raise OmniSyntaxError(f"unterminated string at {sl}:{sc}")
            import json
            try: value=json.loads(source[i:j+1])
            except Exception as exc: raise OmniSyntaxError(f"invalid string at {sl}:{sc}") from exc
            tokens.append(Token(TokenKind.STRING,value,sl,sc)); column+=j+1-i; i=j+1; continue
        kind=one.get(ch)
        if kind is None: raise OmniSyntaxError(f"unexpected character {ch!r} at {line}:{column}")
        tokens.append(Token(kind,ch,line,column)); i+=1; column+=1
    tokens.append(Token(TokenKind.EOF,"",line,column)); return tuple(tokens)

class Parser:
    def __init__(self,tokens): self.tokens,self.index=tokens,0
    def current(self): return self.tokens[self.index]
    def take(self,kind):
        t=self.current()
        if t.kind!=kind: raise OmniSyntaxError(f"expected {kind.value}, got {t.kind.value} at {t.line}:{t.column}")
        self.index+=1; return t
    def accept(self,kind):
        if self.current().kind==kind: self.index+=1; return True
        return False
    def parse(self):
        fs=[]
        while self.current().kind!=TokenKind.EOF: fs.append(self.function())
        return Program(tuple(fs))
    def function(self):
        self.take(TokenKind.FN); name=self.take(TokenKind.IDENT).text; self.take(TokenKind.LPAREN); ps=[]
        if self.current().kind!=TokenKind.RPAREN:
            while True:
                ps.append(self.take(TokenKind.IDENT).text)
                if not self.accept(TokenKind.COMMA): break
        self.take(TokenKind.RPAREN); return Function(name,tuple(ps),self.block())
    def block(self):
        self.take(TokenKind.LBRACE); body=[]
        while self.current().kind!=TokenKind.RBRACE: body.append(self.statement())
        self.take(TokenKind.RBRACE); return tuple(body)
    def statement(self):
        if self.accept(TokenKind.LET):
            name=self.take(TokenKind.IDENT).text; self.take(TokenKind.EQUAL); node=Let(name,self.expression()); self.accept(TokenKind.SEMICOLON); return node
        if self.accept(TokenKind.RETURN):
            node=Return(self.expression()); self.accept(TokenKind.SEMICOLON); return node
        if self.accept(TokenKind.IF):
            self.take(TokenKind.LPAREN); cond=self.expression(); self.take(TokenKind.RPAREN); then=self.block(); other=self.block() if self.accept(TokenKind.ELSE) else (); return If(cond,then,other)
        if self.accept(TokenKind.WHILE):
            self.take(TokenKind.LPAREN); cond=self.expression(); self.take(TokenKind.RPAREN); return While(cond,self.block())
        t=self.current(); raise OmniSyntaxError(f"expected statement at {t.line}:{t.column}")
    def expression(self): return self.logical_or()
    def logical_or(self):
        node=self.logical_and()
        while self.accept(TokenKind.OR): node=Binary(node,TokenKind.OR,self.logical_and())
        return node
    def logical_and(self):
        node=self.comparison()
        while self.accept(TokenKind.AND): node=Binary(node,TokenKind.AND,self.comparison())
        return node
    def comparison(self):
        node=self.term()
        while self.current().kind in (TokenKind.EQEQ,TokenKind.NE,TokenKind.LT,TokenKind.LE,TokenKind.GT,TokenKind.GE):
            op=self.current().kind; self.index+=1; node=Binary(node,op,self.term())
        return node
    def term(self):
        node=self.factor()
        while self.current().kind in (TokenKind.PLUS,TokenKind.MINUS): op=self.current().kind; self.index+=1; node=Binary(node,op,self.factor())
        return node
    def factor(self):
        node=self.primary()
        while self.current().kind in (TokenKind.STAR,TokenKind.SLASH): op=self.current().kind; self.index+=1; node=Binary(node,op,self.primary())
        return node
    def primary(self):
        t=self.current()
        if t.kind==TokenKind.INTEGER: self.index+=1; return Literal(int(t.text))
        if t.kind==TokenKind.STRING: self.index+=1; return Literal(t.text)
        if t.kind in (TokenKind.TRUE,TokenKind.FALSE): self.index+=1; return Literal(t.kind==TokenKind.TRUE)
        if t.kind==TokenKind.NOT: self.index+=1; return Unary(TokenKind.NOT,self.primary())
        if t.kind==TokenKind.IDENT:
            self.index+=1
            if self.accept(TokenKind.LPAREN):
                args=[]
                if self.current().kind!=TokenKind.RPAREN:
                    while True:
                        args.append(self.expression())
                        if not self.accept(TokenKind.COMMA): break
                self.take(TokenKind.RPAREN); return Call(t.text,tuple(args))
            return Name(t.text)
        if self.accept(TokenKind.LPAREN): node=self.expression(); self.take(TokenKind.RPAREN); return node
        raise OmniSyntaxError(f"expected expression at {t.line}:{t.column}")

def parse(source:str)->Program: return Parser(tokenize(source)).parse()
