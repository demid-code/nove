#include "nove_runtime.h"

#define error(msg) \
    do { \
        fprintf(stderr, "Error: %s\n", msg); \
        exit(1); \
    } while (0)

// VALUE

void value_dump(Value v) {
    if (IS_INT(v))
        printf("%" PRId64 "\n", AS_INT(v));
    if (IS_FLOAT(v))
        printf("%g\n", AS_FLOAT(v));
    if (IS_BOOL(v)) {
        if (AS_BOOL(v))
            printf("true\n");
        else
            printf("false\n");
    }
    if (IS_PTR(v))
        printf("%p\n", AS_PTR(v));
}

Value value_add(Value a, Value b) {
    if (a.type != b.type) {
        error("Type mismatch in value_add\n");
    }

    switch (a.type) {
    case TYPE_INT:
        return VAL_INT(AS_INT(a) + AS_INT(b));
    case TYPE_FLOAT:
        return VAL_FLOAT(AS_FLOAT(a) + AS_FLOAT(b));
    case TYPE_BOOL:
        error("Cannot add bools\n");
    case TYPE_PTR:
        error("Cannot add pointers\n");
    }
}

// STACK

void stack_init(ValueStack *s) {
    s->capacity = 8;
    s->size = 0;
    s->data = malloc(sizeof(Value) * s->capacity);

    if (!s->data) {
        error("Failed to allocate memory in stack_init\n");
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
            error("Failed to reallocate memory in stack_push\n");
        }

        s->data = new_data;
        s->capacity = new_cap;
    }

    s->data[s->size++] = v;
}

Value stack_pop(ValueStack *s) {
    if (s->size <= 0) {
        error("Stack underflow\n");
    }
    
    return s->data[--s->size];
}