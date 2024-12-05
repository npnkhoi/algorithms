#include <iostream>
using namespace std;

// Define singly linked node
struct Node {
    int val;
    Node* nxt;
};

void traverse(Node *head) {
    while (head != NULL) {
        printf("%d ", head -> val);
        head = head -> nxt;
    }
    printf("\n");
}

// Bring the smallest value to head of list
// Without double linking, we need to manually keep track of
// the node right before some node
pair<Node*, Node*> put_min_first(Node *head_pre, Node *head) {
    Node *ptr = head, *ptr_pre = head_pre;
    Node *min_node = ptr, *min_node_pre = ptr_pre;
    // get min node
    while (ptr != NULL) {
        if (ptr->val < min_node->val) {
            min_node = ptr;
            min_node_pre = ptr_pre;
        }
        ptr_pre = ptr;
        ptr = ptr->nxt;
    }
    // unlink and link to swap min_node and head
    if (head_pre != NULL) {
        head_pre->nxt = min_node;
    }
    if (min_node_pre != NULL) {
        min_node_pre->nxt = head;
    }
    swap(min_node->nxt, head->nxt); // only swaping the pointers
    
    return make_pair(min_node_pre, min_node);
}

// inplace sort, O(N^2)
Node* selection_sort(Node *head) {
    Node *ptr = head, *ptr_pre = NULL;
    head = NULL;
    while (ptr != NULL) {
        pair<Node*, Node*> res = put_min_first(ptr_pre, ptr);
        ptr_pre = res.first;
        ptr = res.second;
        if (head == NULL) head = ptr;
        
        ptr_pre = ptr;
        ptr = ptr->nxt;
    }
    return head;
}

int main() {
    // Initialize the list
    int values[20] = {46, 40, 29, 13, 4, 46, 37, 30, 7, 50, 8, 8, 27, 25, 24, 1, 12};
    int n = 17;
    printf("%d\n", values[n-1]);
    
    Node *head = new Node();
    head -> val = values[n-1];
    for (int i = n-2; i >= 0; --i) {
        // create new node
        Node *newNode = new Node();
        newNode -> val = values[i];
        // link
        newNode -> nxt = head;
        head = newNode;
    }
    
    traverse(head);

    // sort it!
    head = selection_sort(head);
    traverse(head);
}