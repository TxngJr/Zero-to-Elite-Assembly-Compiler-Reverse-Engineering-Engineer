#include <stdio.h>
#include <string.h>
int main(void) {
    const char text[] = "ABC";
    printf("strlen=%zu sizeof=%zu bytes=", strlen(text), sizeof text);
    for (size_t i=0;i<sizeof text;++i) printf("%02X%s", (unsigned char)text[i], i+1==sizeof text?"":" ");
    putchar('\n');
    const char embedded[] = {'A','\0','B','\0'};
    printf("embedded strlen=%zu sizeof=%zu\n", strlen(embedded), sizeof embedded);
    return 0;
}
