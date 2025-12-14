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

#define VAL_INT(x)   ((Value){ .type = TYPE_INT, .as.i = (x) })
#define VAL_FLOAT(x) ((Value){ .type = TYPE_FLOAT, .as.f = (x) })
#define VAL_BOOL(x)  ((Value){ .type = TYPE_BOOL, .as.b = (x) })
#define VAL_PTR(x)   ((Value){ .type = TYPE_PTR, .as.ptr = (x) })

#define IS_INT(v)   ((v).type == TYPE_INT)
#define IS_FLOAT(v) ((v).type == TYPE_FLOAT)
#define IS_BOOL(v)  ((v).type == TYPE_BOOL)
#define IS_PTR(v)   ((v).type == TYPE_PTR)

#define AS_INT(v)   ((v).as.i)
#define AS_FLOAT(v) ((v).as.f)
#define AS_BOOL(v)  ((v).as.b)
#define AS_PTR(v)   ((v).as.ptr)

void value_dump(Value v);
Value value_add(Value a, Value b);
Value value_sub(Value a, Value b);
Value value_mul(Value a, Value b);
Value value_div(Value a, Value b);

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