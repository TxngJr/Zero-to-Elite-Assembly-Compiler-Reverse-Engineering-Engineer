#include <assert.h>
#include <stdio.h>
#include <string.h>

typedef enum { NODE_DIR, NODE_FILE } NodeType;

typedef struct Node Node;
struct Node {
    const char *name;
    NodeType type;
    const char *content;
    Node *children;
    size_t child_count;
};

static Node *child_named(Node *dir, const char *name, size_t len) {
    if (dir->type != NODE_DIR) return NULL;
    for (size_t i = 0; i < dir->child_count; ++i) {
        Node *child = &dir->children[i];
        if (strlen(child->name) == len && strncmp(child->name, name, len) == 0) {
            return child;
        }
    }
    return NULL;
}

static Node *lookup(Node *root, const char *path) {
    if (path[0] != '/') return NULL;
    if (path[1] == '\0') return root;

    Node *cur = root;
    const char *p = path + 1;

    while (*p != '\0') {
        const char *slash = strchr(p, '/');
        size_t len = slash ? (size_t)(slash - p) : strlen(p);
        if (len == 0) return NULL;

        cur = child_named(cur, p, len);
        if (!cur) return NULL;

        if (!slash) break;
        p = slash + 1;
    }
    return cur;
}

int main(void) {
    Node etc_children[] = {
        {"motd", NODE_FILE, "Welcome to EliteOS\n", NULL, 0},
        {"version", NODE_FILE, "15\n", NULL, 0},
    };
    Node root_children[] = {
        {"etc", NODE_DIR, NULL, etc_children, 2},
        {"hello.txt", NODE_FILE, "hello vfs\n", NULL, 0},
    };
    Node root = {"/", NODE_DIR, NULL, root_children, 2};

    Node *motd = lookup(&root, "/etc/motd");
    assert(motd && motd->type == NODE_FILE);
    assert(strcmp(motd->content, "Welcome to EliteOS\n") == 0);
    assert(lookup(&root, "/missing") == NULL);

    printf("/etc/motd: %s", motd->content);
    puts("vfs-sim: OK");
    return 0;
}
