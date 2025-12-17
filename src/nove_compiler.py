from nove_parser import OpType, Op

# TODO:
# op DO and IF, does the same thing, basically jumping if condition is false
# perphaps, make JMP_IF_FALSE op and replace if and do with it
# also you could replace some of op's with just JUMP op

class Compiler:
    def __init__(self, ops: list[Op]):
        self.ops = ops
        self.current = 0

        self.writes = {"init": "", "main": ""}
        self.write_mode = None

        self.includes = []
        self.add_include("\"nove_runtime.h\"")

    def add_include(self, include: str):
        if not include in self.includes:
            self.includes.append(include)

    def write(self, code: str, tabs: int = 0):
        self.writes[self.write_mode] += f"{"    " * tabs}{code}"

    def writeln(self, code: str, tabs: int = 0):
        self.writes[self.write_mode] += f"{"    " * tabs}{code}\n"

    def is_at_end(self) -> bool:
        return self.current >= len(self.ops)

    def advance(self) -> tuple[Op, int]:
        idx = self.current
        self.current += 1
        return (self.ops[idx], idx)

    def scan_op(self):
        op, op_idx = self.advance()

        write_goto = True
        self.writeln(f"addr_{op_idx}: %s // {op.type.name}" % "{", 1)

        match op.type:
            case OpType.PUSH_INT:
                self.writeln(f"stack_push(&stack, VAL_INT({op.operand}));", 2)

            case OpType.PUSH_FLOAT:
                self.writeln(f"stack_push(&stack, VAL_FLOAT({op.operand}));", 2)

            case OpType.PLUS:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_add(a, b));", 2)

            case OpType.MINUS:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_sub(a, b));", 2)

            case OpType.MULTIPLY:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_mul(a, b));", 2)

            case OpType.DIVIDE:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_div(a, b));", 2)

            case OpType.EQUALS:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_equals(a, b));", 2)

            case OpType.GREATER:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_greater(a, b));", 2)

            case OpType.LESS:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_less(a, b));", 2)

            case OpType.NOT:
                self.writeln("stack_push(&stack, value_not(stack_pop(&stack)));", 2)

            case OpType.AND:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_and(a, b));", 2)

            case OpType.OR:
                self.writeln("Value b = stack_pop(&stack);", 2)
                self.writeln("Value a = stack_pop(&stack);", 2)
                self.writeln("stack_push(&stack, value_or(a, b));", 2)

            case OpType.TO_INT:
                self.writeln("stack_push(&stack, value_to_int(stack_pop(&stack)));", 2)
            
            case OpType.TO_FLOAT:
                self.writeln("stack_push(&stack, value_to_float(stack_pop(&stack)));", 2)

            case OpType.TO_BOOL:
                self.writeln("stack_push(&stack, value_to_bool(stack_pop(&stack)));", 2)

            case OpType.DROP:
                self.writeln("stack_pop(&stack);", 2)

            case OpType.DUMP:
                self.writeln("value_dump(stack_pop(&stack));", 2)

            case OpType.PICK:
                self.writeln("stack_pick(&stack);", 2)

            case OpType.ROLL:
                self.writeln("stack_roll(&stack);", 2)

            case OpType.WHILE:
                pass

            case OpType.DO:
                self.writeln("Value cond = stack_pop(&stack);", 2)
                self.writeln("if (!IS_BOOL(cond)) error(\"Condition expected to be bool\");", 2)
                self.writeln(f"if (!AS_BOOL(cond)) goto addr_{op.operand};", 2)

            case OpType.ENDWHILE:
                self.writeln(f"goto addr_{op.operand};", 2)

            case OpType.IF:
                self.writeln("Value cond = stack_pop(&stack);", 2)
                self.writeln("if (!IS_BOOL(cond)) error(\"Condition expected to be bool\");", 2)
                self.writeln(f"if (!AS_BOOL(cond)) goto addr_{op.operand};", 2)

            case OpType.ELSE:
                self.writeln(f"goto addr_{op.operand};", 2)

            case OpType.ENDIF:
                pass

            case OpType.EOF:
                write_goto = False
                self.writeln("stack_free(&stack);", 2)
                self.writeln("return 0;", 2)

            case _:
                assert False, f"Unsupported OpType.{op.type.name} in Compiler.scan_op()"

        if write_goto:
            self.writeln(f"goto addr_{op_idx + 1};", 2)
        self.writeln("}", 1)

    def compile(self) -> str:
        self.write_mode = "main"
        while not self.is_at_end():
            self.scan_op()
        
        self.write_mode = "init"
        self.writeln("ValueStack stack;", 1)
        self.writeln("stack_init(&stack);\n", 1)
        self.writeln("goto addr_0;\n", 1)

        output = ""

        if len(self.includes) > 0:
            for include in self.includes:
                output += f"#include {include}\n"
            output += "\n"

        output += "int main() {\n"
        output += self.writes["init"]
        output += self.writes["main"]
        output += "}\n"

        return output