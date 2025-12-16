from nove_error import report_error
from nove_lexer import TokenType, Token
from nove_ops import OpType, Op, WORD_TO_OPTYPE

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

        self.ops = []

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)
    
    def advance(self) -> Token:
        self.current += 1
        return self.tokens[self.current - 1]
    
    def add_op(self, op_type: OpType, operand: any, token: Token):
        self.ops.append(Op(op_type, operand, token))

    def make_op(self):
        token = self.advance()

        match token.type:
            case TokenType.INT:
                self.add_op(OpType.PUSH_INT, int(token.text), token)

            case TokenType.FLOAT:
                self.add_op(OpType.PUSH_FLOAT, float(token.text), token)

            case TokenType.CHAR:
                self.add_op(OpType.PUSH_INT, int(ord(token.text[1:-1].encode("utf-8").decode("unicode_escape"))), token)

            case TokenType.WORD:
                if token.text in WORD_TO_OPTYPE:
                    self.add_op(WORD_TO_OPTYPE.get(token.text), None, token)
                else:
                    report_error(f"`{token.text}` is not a built-in", token.loc)

            case _:
                assert False, f"Unsupported TokenType.{token.type.name} in Parser.make_op()"

    def parse(self) -> list[Op]:
        while not self.is_at_end():
            self.make_op()

        self.add_op(OpType.EOF, None, None)
        
        return self.ops