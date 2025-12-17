#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <inttypes.h>

// VALUE

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_BOOL,
    TYPE_PTR,
} ValueType;

typedef struct {
    ValueType type;
    union {
        int64_t i;
        double f;
        bool b;
        void *ptr;
    } as;
} Value;

#define VAL_INT(x)   ((Value){ .type = TYPE_INT, .as.i = (int64_t)(x) })
#define VAL_FLOAT(x) ((Value){ .type = TYPE_FLOAT, .as.f = (double)(x) })
#define VAL_BOOL(x)  ((Value){ .type = TYPE_BOOL, .as.b = (bool)(x) })
#define VAL_PTR(x)   ((Value){ .type = TYPE_PTR, .as.ptr = (void*)(x) })

#define IS_INT(v)   ((v).type == TYPE_INT)
#define IS_FLOAT(v) ((v).type == TYPE_FLOAT)
#define IS_BOOL(v)  ((v).type == TYPE_BOOL)
#define IS_PTR(v)   ((v).type == TYPE_PTR)

#define AS_INT(v)   ((v).as.i)
#define AS_FLOAT(v) ((v).as.f)
#define AS_BOOL(v)  ((v).as.b)
#define AS_PTR(v)   ((v).as.ptr)

Value value_add(Value a, Value b);
Value value_sub(Value a, Value b);
Value value_mul(Value a, Value b);
Value value_div(Value a, Value b);

Value value_equals(Value a, Value b);
Value value_greater(Value a, Value b);
Value value_less(Value a, Value b);

Value value_not(Value val);
Value value_and(Value a, Value b);
Value value_or(Value a, Value b);

// NOTE: i think we shouldn't be able to convert anything on stack to ptr
// because stack elements dynamically change and pointing to them will be dangerous
Value value_to_int(Value val);
Value value_to_float(Value val);
Value value_to_bool(Value val);

void value_dump(Value v);

// STACK

typedef struct {
    Value *data;
    size_t size;
    size_t capacity;
} ValueStack;

void stack_init(ValueStack *s);
void stack_free(ValueStack *s);
void stack_push(ValueStack *s, Value v);
Value stack_pop(ValueStack *s);
void stack_pick(ValueStack *s);
void stack_roll(ValueStack *s);