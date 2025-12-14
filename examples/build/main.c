#include "nove_runtime.h"

int main() {
    ValueStack stack;
    stack_init(&stack);

    goto addr_0;

    addr_0: { // PUSH_INT
        stack_push(&stack, VAL_INT(10));
        goto addr_1;
    }
    addr_1: { // PUSH_INT
        stack_push(&stack, VAL_INT(20));
        goto addr_2;
    }
    addr_2: { // PLUS
        Value b = stack_pop(&stack);
        Value a = stack_pop(&stack);
        stack_push(&stack, value_add(a, b));
        goto addr_3;
    }
    addr_3: { // DUMP
        value_dump(stack_pop(&stack));
        goto addr_4;
    }
    addr_4: { // PUSH_INT
        stack_push(&stack, VAL_INT(120));
        goto addr_5;
    }
    addr_5: { // PUSH_INT
        stack_push(&stack, VAL_INT(60));
        goto addr_6;
    }
    addr_6: { // MINUS
        Value b = stack_pop(&stack);
        Value a = stack_pop(&stack);
        stack_push(&stack, value_sub(a, b));
        goto addr_7;
    }
    addr_7: { // DUMP
        value_dump(stack_pop(&stack));
        goto addr_8;
    }
    addr_8: { // PUSH_INT
        stack_push(&stack, VAL_INT(60));
        goto addr_9;
    }
    addr_9: { // PUSH_INT
        stack_push(&stack, VAL_INT(2));
        goto addr_10;
    }
    addr_10: { // MULTIPLY
        Value b = stack_pop(&stack);
        Value a = stack_pop(&stack);
        stack_push(&stack, value_mul(a, b));
        goto addr_11;
    }
    addr_11: { // DUMP
        value_dump(stack_pop(&stack));
        goto addr_12;
    }
    addr_12: { // PUSH_INT
        stack_push(&stack, VAL_INT(480));
        goto addr_13;
    }
    addr_13: { // PUSH_INT
        stack_push(&stack, VAL_INT(2));
        goto addr_14;
    }
    addr_14: { // DIVIDE
        Value b = stack_pop(&stack);
        Value a = stack_pop(&stack);
        stack_push(&stack, value_div(a, b));
        goto addr_15;
    }
    addr_15: { // DUMP
        value_dump(stack_pop(&stack));
        goto addr_16;
    }
    addr_16: { // EOF
        stack_free(&stack);
        return 0;
    }
}
