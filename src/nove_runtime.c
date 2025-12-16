#include "nove_runtime.h"

#define error(msg) \
    do { \
        fprintf(stderr, "Error: %s\n", msg); \
        exit(1); \
    } while (0)

// VALUE

Value value_add(Value a, Value b) {
    if (a.type != b.type) {
        if (IS_INT(a) && IS_FLOAT(b))
            return VAL_FLOAT((double)AS_INT(a) + AS_FLOAT(b));

        if (IS_FLOAT(a) && IS_INT(b))
            return VAL_FLOAT(AS_FLOAT(a) + (double)AS_INT(b));
        
        if (IS_PTR(a) && IS_INT(b))
            return VAL_PTR((uint8_t*)AS_PTR(a) + AS_INT(b));

        if (IS_INT(a) && IS_PTR(b))
            return VAL_PTR((uint8_t*)AS_PTR(b) + AS_INT(a));

        error("Type mismatch in value_add");
    }

    switch (a.type) {
    case TYPE_INT:
        return VAL_INT(AS_INT(a) + AS_INT(b));
    case TYPE_FLOAT:
        return VAL_FLOAT(AS_FLOAT(a) + AS_FLOAT(b));
    case TYPE_BOOL:
        error("Cannot add bools");
    case TYPE_PTR:
        error("Cannot add pointers");
    }

    error("Unreachable in value_add");
}

Value value_sub(Value a, Value b) {
    if (a.type != b.type) {
        if (IS_INT(a) && IS_FLOAT(b))
            return VAL_FLOAT((double)AS_INT(a) - AS_FLOAT(b));

        if (IS_FLOAT(a) && IS_INT(b))
            return VAL_FLOAT(AS_FLOAT(a) - (double)AS_INT(b));
        
        if (IS_PTR(a) && IS_INT(b))
            return VAL_PTR((uint8_t*)AS_PTR(a) - AS_INT(b));

        if (IS_INT(a) && IS_PTR(b))
            return VAL_PTR((uint8_t*)AS_PTR(b) - AS_INT(a));

        error("Type mismatch in value_sub");
    }

    switch (a.type) {
    case TYPE_INT:
        return VAL_INT(AS_INT(a) - AS_INT(b));
    case TYPE_FLOAT:
        return VAL_FLOAT(AS_FLOAT(a) - AS_FLOAT(b));
    case TYPE_BOOL:
        error("Cannot subtract bools");
    case TYPE_PTR:
        error("Cannot subtract pointers");
    }

    error("Unreachable in value_sub");
}

Value value_mul(Value a, Value b) {
    if (a.type != b.type) {
        if (IS_INT(a) && IS_FLOAT(b))
            return VAL_FLOAT((double)AS_INT(a) * AS_FLOAT(b));

        if (IS_FLOAT(a) && IS_INT(b))
            return VAL_FLOAT(AS_FLOAT(a) * (double)AS_INT(b));

        error("Type mismatch in value_mul");
    }

    switch (a.type) {
    case TYPE_INT:
        return VAL_INT(AS_INT(a) * AS_INT(b));
    case TYPE_FLOAT:
        return VAL_FLOAT(AS_FLOAT(a) * AS_FLOAT(b));
    case TYPE_BOOL:
        error("Cannot multiply bools");
    case TYPE_PTR:
        error("Cannot multiply pointers");
    }

    error("Unreachable in value_mul");
}

Value value_div(Value a, Value b) {
    if (a.type != b.type) {
        if (IS_INT(a) && IS_FLOAT(b))
            return VAL_FLOAT((double)AS_INT(a) / AS_FLOAT(b));

        if (IS_FLOAT(a) && IS_INT(b))
            return VAL_FLOAT(AS_FLOAT(a) / (double)AS_INT(b));

        error("Type mismatch in value_div");
    }

    switch (a.type) {
    case TYPE_INT:
        return VAL_FLOAT(AS_INT(a) / AS_INT(b));
    case TYPE_FLOAT:
        return VAL_FLOAT(AS_FLOAT(a) / AS_FLOAT(b));
    case TYPE_BOOL:
        error("Cannot divide bools");
    case TYPE_PTR:
        error("Cannot divide pointers");
    }

    error("Unreachable in value_div");
}

Value value_to_int(Value val) {
    switch (val.type) {
    case TYPE_INT:
        return val;
    case TYPE_FLOAT:
        return VAL_INT(AS_FLOAT(val));
    case TYPE_BOOL:
        return VAL_INT(AS_BOOL(val));
    case TYPE_PTR:
        error("Can't convert pointer to int");
    }
}

Value value_to_float(Value val) {
    switch (val.type) {
    case TYPE_INT:
        return VAL_FLOAT(AS_INT(val));
    case TYPE_FLOAT:
        return val;
    case TYPE_BOOL:
        return VAL_FLOAT(AS_BOOL(val));
    case TYPE_PTR:
        error("Can't convert pointer to float");
    }
}

Value value_to_bool(Value val) {
    switch (val.type) {
    case TYPE_INT:
        return VAL_BOOL(AS_INT(val));
    case TYPE_FLOAT:
        return VAL_BOOL(AS_FLOAT(val));
    case TYPE_BOOL:
        return val;
    case TYPE_PTR:
        error("Can't convert pointer to bool");
    }
}

void value_dump(Value v) {
    switch (v.type) {
    case TYPE_INT:
        printf("%" PRId64 "\n", AS_INT(v));
        break;
    case TYPE_FLOAT:
        printf("%g\n", AS_FLOAT(v));
        break;
    case TYPE_BOOL:
        if (AS_BOOL(v))
            printf("true\n");
        else
            printf("false\n");
        break;
    case TYPE_PTR:
        printf("%p\n", AS_PTR(v));
        break;
    }
}

// STACK

void stack_init(ValueStack *s) {
    s->capacity = 8;
    s->size = 0;
    s->data = malloc(sizeof(Value) * s->capacity);

    if (!s->data) {
        error("Failed to allocate memory in stack_init");
    }
}

void stack_free(ValueStack *s) {
    free(s->data);
    s->size = 0;
    s->capacity = 0;
}

void stack_push(ValueStack *s, Value v) {
    if (s->size >= s->capacity) {
        size_t new_cap = s->capacity * 2;
        
        Value *new_data = realloc(s->data, sizeof(Value) * new_cap);
        if (!new_data) {
            error("Failed to reallocate memory in stack_push");
        }

        s->data = new_data;
        s->capacity = new_cap;
    }

    s->data[s->size++] = v;
}

Value stack_pop(ValueStack *s) {
    if (s->size <= 0) {
        error("Stack underflow");
    }
    
    return s->data[--s->size];
}