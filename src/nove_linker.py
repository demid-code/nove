from nove_error import report_error
from nove_ops import OpType, Op

OPS_TO_LINK = {
    # while
    OpType.WHILE,
    OpType.DO,
    OpType.ENDWHILE,
    OpType.BREAK,

    # if/else
    OpType.IF,
    OpType.ELSE,
    OpType.ENDIF,
}

class Linker:
    def __init__(self, ops: list[Op]):
        self.ops = ops
        self.current = 0

        self.stack = []
        self.second_stack = []

    def push(self, idx: int, second: bool = False):
        if second:
            self.second_stack.append(idx)
        else:
            self.stack.append(idx)

    def pop(self, second: bool = False) -> tuple[Op, int]:
        idx = None
        if second: idx = self.second_stack.pop()
        else: idx = self.stack.pop()
        return (self.ops[idx], idx)

    def is_at_end(self) -> bool:
        return self.current >= len(self.ops)
    
    def advance(self) -> tuple[Op, int]:
        idx = self.current
        self.current += 1
        return (self.ops[idx], idx)

    def top_level_err(self, operation_name: str):
        if len(self.stack) <= 0: report_error(f"`{operation_name}` can't be used from top level")

    def solve_end_stack(self):
        for op_idx in self.stack:
            op = self.ops[op_idx]

            match op.type:
                case OpType.WHILE:
                    report_error("`while` was never closed with `do`", op.token.loc)

                case OpType.DO:
                    report_error("`do` was never closed with `endwhile`", op.token.loc)

                case OpType.IF:
                    report_error("`if` was never closed with `endif` or `else`", op.token.loc)

                case OpType.ELSE:
                    report_error("`else` was never closed with `endif`", op.token.loc)

                case _:
                    assert False, f"Unsupported OpType.{op.type.name} in Linker.solve_end_stack()"

    def scan_op(self):
        op, op_idx = self.advance()

        if op.type in OPS_TO_LINK:
            match op.type:
                case OpType.WHILE:
                    self.push(op_idx)

                case OpType.DO:
                    self.top_level_err("do")

                    _, while_idx = self.pop()
                    self.ops[op_idx].operand = while_idx

                    self.push(op_idx)

                case OpType.ENDWHILE:
                    self.top_level_err("endwhile")

                    do_op, do_idx = self.pop()
                    if do_op.type != OpType.DO:
                        report_error("`endwhile` can only close `do`", op.loc)

                    self.ops[op_idx].operand = do_op.operand + 1
                    self.ops[do_idx].operand = op_idx + 1

                    for opp_idx in reversed(self.second_stack):
                        opp = self.ops[opp_idx]

                        if opp.type == OpType.BREAK and opp.operand == do_idx:
                            self.ops[opp_idx].operand = op_idx + 1

                case OpType.BREAK:
                    self.top_level_err("break")

                    found = False
                    for opp_idx in reversed(self.stack):
                        opp = self.ops[opp_idx]

                        if opp.type == OpType.DO:
                            self.ops[op_idx].operand = opp_idx
                            self.push(op_idx, second=True)
                            found = True

                    if not found:
                        report_error("`break` can only be used in `while` loop", op.loc)

                case OpType.IF:
                    self.push(op_idx)

                case OpType.ELSE:
                    self.top_level_err("else")

                    if_op, if_idx = self.pop()
                    if if_op.type != OpType.IF:
                        report_error("`else` can only close `if`", op.loc)

                    self.ops[if_idx].operand = op_idx + 1
                    self.push(op_idx)

                case OpType.ENDIF:
                    self.top_level_err("endif")

                    if_op, if_idx = self.pop()
                    if not if_op.type in (OpType.IF, OpType.ELSE):
                        report_error("`endif` can only close `if` and `else`", op.loc)

                    self.ops[if_idx].operand = op_idx + 1

                case _:
                    assert False, f"Unsupported OpType.{op.type.name} in Linker.scan_op()"

    def link(self) -> list[Op]:
        while not self.is_at_end():
            self.scan_op()

        self.solve_end_stack()

        return self.ops