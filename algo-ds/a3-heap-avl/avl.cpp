#include <stdio.h>
#include <stdlib.h>

struct Node {
    int val;
    int ht;
    Node *l;
    Node *r;
    Node *p;
};

int get_left_ht(Node *v) {
    if (v->l == NULL) {
        return 0;
    }
    return v->l->ht; // check precedence
}

int get_right_ht(Node *v) {
    if (v->r == NULL) {
        return 0;
    }
    return v->r->ht; // check precedence
}

Node *bst_insert(Node *root, int val) {
    // FIXME
}

Node *avl_insert(Node *root, int val) {
    Node *node = bst_insert(root, val);
    Node *p = node -> p;
    while (p != NULL) {
        int left_height = get_left_ht(p) + 1;
        // FIXME: continue ...
    }
}

Node *get_child_longer(Node *v) {
    int lh = get_left_ht(v);
    int rh = get_right_ht(v);
    if (lh > rh) return v->l;
    return v->r;
}

void avl_bal_left_str(Node *n1, Node *n2, Node *n3) {
    Node *p = n1 -> p;
    // TODO: handle 'n1 is root'

    if (p != NULL) {
        if (n1 == p->l) p->l = n2;
        else p->r = n2;
    }

    // n1
    n1 -> p = n2;
    n1 -> l = n2 -> r;

    // n2
    n2 -> p = p;
    Node *n2r = n2 -> r; // backup
    n2 -> r = n1;

    // n2r
    if (n2r != NULL) n2r -> p = n1;
}

void avl_bal_right_str(Node *n1, Node *n2, Node *n3) {
    
}

void avl_balance(Node *n1) {
    Node *n2 = get_child_longer(n1);
    Node *n3 = get_child_longer(n2);

    if (n2 == n1->l && n3 == n2->l) {
        avl_bal_left_str(n1, n2, n3);
    }
    if (n2 == n1->r && n3 == n2->r) {
        avl_bal_right_str(n1, n2, n3);
    }
}

int  main() {

}