from nove_error import report_error
from nove_ops import OpType, Op

OPS_TO_LINK = {
    # while
    OpType.WHILE,
    OpType.DO,
    OpType.ENDWHILE,
}

class Linker:
    def __init__(self, ops: list[Op]):
        self.ops = ops
        self.current = 0

        self.stack = []

    def push(self, idx: int):
        self.stack.append(idx)

    def pop(self) -> tuple[Op, int]:
        idx = self.stack.pop()
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

                    self.ops[op_idx].operand = do_op.operand + 1
                    self.ops[do_idx].operand = op_idx + 1
                
                case _:
                    assert False, f"Unsupported OpType.{op.type.name} in Linker.scan_op()"

    def link(self) -> list[Op]:
        while not self.is_at_end():
            self.scan_op()

        self.solve_end_stack()

        return self.ops