/*
We have discussed Binary Search Trees.(BST)
Write a program to implement a delete operation from BST.
You will have to write the program to insert nodes in the BST also 
(we already did the algorithm in detail in the class for insert).
    Insert the following nodes in the order mentioned here.
    40, 60, 20, 80, 50, 10, 30, 15, 5, 35, 25, 45, 55, 70, 90, 32, 33, 48, 46
    Do an inorder traversal.  
    make screen shot
    Now delete 40 (you decide predecessor or successor).
    Do inorder traversal again.
    Make screen shot
    Now delete 20
    Do inroder traversal
    make screen shot.
    Submit the code.
    Submit the screen shots.
*/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct Node {
    int val;
    Node *p;
    Node *ch[2]; // making the children to array for clean code
};

class BST {

private:
    /**
     * Add a new child with value `val` to the side `side`
     * of node `p`.
     * Returns: the newly created node
    */
    Node *add_child(Node *p, int val, int side) {
        Node* child = new Node();
        child->val = val;
        child->p = p;
        p->ch[side] = child;
        return child;
    }
    /**
     * insert a node 
     * Returns a pointer to it
    */
    
    Node *insert(Node *p, int val) {
        assert(p != NULL);
        
        int flag = -1;
        if (val <= p->val) {
            if  (p->ch[0] == NULL) {
                return add_child(p, val, 0);
            } 
            return insert(p->ch[0], val);
        } 
        if (p->ch[1] == NULL) {
            return add_child(p, val, 1);
        }
        return insert(p->ch[1], val);
    }

    /**
     * In order traversal.
     * Prints the node values to stdout.
    */
    void in_traverse(Node *v) {
        if (v == NULL) return;
        in_traverse(v->ch[0]);
        printf("%d ", v->val);
        in_traverse(v->ch[1]);
    }

    /**
     * Find a node by value.
     * Returns a *Node if found, NULL otherwise.
    */
    Node *find(Node *v, int val) {
        if (v == NULL) return NULL;
        if (v->val == val) return v;

        Node *tmp = this->find(v->ch[0], val);
        if (tmp != NULL) return tmp;
        return this->find(v->ch[1], val);
    }

    /**
     * Returns predecessor/successor if available
     * Otherwise, returns NULL
     * dir=0 means predecessor, 1 means successor
    */
    Node *find_closest_child(Node *v, int dir) {
        assert(v != NULL);
        if (v->ch[dir] == NULL) return NULL;
        Node *u = v->ch[dir];
        while (u->ch[dir^1] != NULL) {
            u = u->ch[dir^1];
        }
        return u;
    }

public:
    Node *root; // Initially, the tree has no nodes.

    /**
     * Inserts a node with value `val`
     * Returns that *Node.
    */
    Node *insert(int val) {
        if (this->root == NULL) {
            this->root = new Node();
            this->root->val = val;
            return this->root;
        }
        return this->insert(this->root, val);
    }

    /**
     * In-orderly traverses the whole tree.
    */
    void in_traverse() {
        in_traverse(this->root);
        printf("\n");
    }
    
    /**
     * Removes the first node with value `val`
     * Returns true if found, false otherwise.
    */
    bool remove(int val) {
        // find such a node
        Node *v = this->find(this->root, val);
        if (v == NULL) return false;

        // find predecessor or successor
        int dir = 0;
        Node *u = this->find_closest_child(v, dir);
        if (u == NULL) {
            dir = 1;
            u = this->find_closest_child(v, dir);
        }

        Node *p = v->p;

        if (u == NULL) { // v if a leaf node, just delete it
            if (p != NULL) {
                if (p->ch[0] == v) p->ch[0] = NULL;
                else p->ch[1] = NULL;
            } else {
                this->root = NULL; // deleting the only node
            }
            return true;
        }

        // v has children
        v->val = u->val; // replace v by u
        // delete u
        (u->p)->ch[dir^1] = u->ch[dir];
        if (u->ch[dir] != NULL) {
            (u->ch[dir])->p = u->p;
        }
        
        return true;
    }
} tree;


int main() {
    int values[20] = {40, 60, 20, 80, 50, 10, 30, 15, 5, 35, 25, 45, 55, 70, 90, 32, 33, 48, 46};
    int n = 19;
    for (int i = 0; i < n; ++ i) {
        tree.insert(values[i]);
    }
    
    printf("Initial tree:\n");
    tree.in_traverse();

    printf("Removing 40\n");
    tree.remove(40);
    tree.in_traverse();

    printf("Removing 20\n");
    tree.remove(20);
    tree.in_traverse();
}