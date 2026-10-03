#include "mini_string.h"
#include <assert.h>
#include <string.h>
int main(void) {
    assert(zs_length("") == 0); assert(zs_length("abc") == 3);
    assert(zs_compare("abc","abc") == 0); assert(zs_compare("abc","abd") < 0); assert(zs_compare("b","a") > 0);
    char buf[4]; assert(zs_copy(buf,sizeof buf,"abc")); assert(strcmp(buf,"abc") == 0);
    char tiny[3] = {'X','Y','\0'}; assert(!zs_copy(tiny,sizeof tiny,"abc")); assert(tiny[0] == 'X');
    assert(zs_find_char("abc",'b') != NULL); assert(zs_find_char("abc",'z') == NULL);
    char rev[]="abcd"; zs_reverse(rev); assert(strcmp(rev,"dcba") == 0);
    return 0;
}
