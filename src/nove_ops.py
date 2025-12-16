from enum import IntEnum, auto
from dataclasses import dataclass

from nove_lexer import Token

class OpType(IntEnum):
    # Push
    PUSH_INT = auto()
    PUSH_FLOAT = auto()

    # Built-ins
    # +, -, *, /
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    # Type conversions
    TO_INT = auto()
    TO_FLOAT = auto()
    TO_BOOL = auto()

    DUMP = auto()

    # Specific
    EOF = auto()

@dataclass
class Op:
    type: OpType
    operand: any
    token: Token

    def __repr__(self) -> str:
        op_str = f"{f" {self.operand}" if self.operand != None else ""}"
        return f"{self.type.name}{op_str}"

WORD_TO_OPTYPE = {
    # Built-ins
    # +, -, *, /
    "+":    OpType.PLUS,
    "-":    OpType.MINUS,
    "*":    OpType.MULTIPLY,
    "/":    OpType.DIVIDE,

    # Type conversions
    "$int":   OpType.TO_INT,
    "$float": OpType.TO_FLOAT,
    "$bool": OpType.TO_BOOL,

    "dump": OpType.DUMP,
}