#include <stdio.h>
typedef int (*binary_op)(int,int);
static int add(int a,int b){return a+b;}
static int multiply(int a,int b){return a*b;}
static int apply(binary_op op,int a,int b){return op(a,b);}
int main(void){printf("add=%d multiply=%d\n",apply(add,6,7),apply(multiply,6,7));return 0;}
