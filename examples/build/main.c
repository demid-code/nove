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
        stack_push(&stack, VAL_INT(11));
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
    addr_4: { // PUSH_FLOAT
        stack_push(&stack, VAL_FLOAT(10.5));
        goto addr_5;
    }
    addr_5: { // PUSH_FLOAT
        stack_push(&stack, VAL_FLOAT(0.25));
        goto addr_6;
    }
    addr_6: { // PLUS
        Value b = stack_pop(&stack);
        Value a = stack_pop(&stack);
        stack_push(&stack, value_add(a, b));
        goto addr_7;
    }
    addr_7: { // DUMP
        value_dump(stack_pop(&stack));
        goto addr_8;
    }
    addr_8: { // EOF
        stack_free(&stack);
        return 0;
    }
}
