/*
    Implement heap sort.
    1. Make an array of 15 numbers. 
    Make sure the array is not sorted AND the numbers do not make a heap.
    You may hard code this array in your main program.
    
    2. Convert the array into a heap, using Floyd's algorithm.  
    Print the new array
    
    3. Sort the array into descending order using heap sort method. 
    Print the array.
*/

#include <stdio.h>
using namespace std;

int get_left(int i) {
    return i * 2;
}

int get_right(int i) {
    return get_left(i) + 1;
}

void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/**
 * Check if a node is bigger than the children. If not, recursively swap it with the bigger children.
*/
void percolate(int a[], int i) {
    int l = get_left(i), r = get_right(i);
    if (l > a[0]) return;
    if (r > a[0]) { // (i) only has left child (which is a leaf node)
        if (a[i] < a[l]) {
            swap(a+i, a+l);
        }
        return;
    }

    int c = (a[l] > a[r] ? l : r);
    if (a[c] > a[i]) {
        swap(a+c, a+i);
        percolate(a, c);
    }
}

void floyd(int a[]) {
    int n = a[0];
    for (int i = n/2; i >= 1; --i) {
        percolate(a, i);
    }
}

/**
 * Assumes the array is already a heap.
*/
void heapsort(int a[]) {
    for (int i = a[0]; i >= 1; --i) {
        swap(a+i, a+1);
        a[0] --;
        percolate(a, 1);
    }
}

int main() {
    int n = 15;
    int a[20] = {n, 48, 88, 82, 26, 73, 65, 60, 62, 61, 19, 79, 16, 88, 20, 70};

    printf("Original array:\n");
    for (int i = 1; i <= n; ++ i) printf("%d ", a[i]);
    printf("\n");

    floyd(a);
    printf("Into a heap (including a[0]):\n");
    for (int i = 0; i <= n; ++ i) printf("%d ", a[i]);
    printf("\n");

    heapsort(a);
    printf("Sorted:\n");
    for (int i = 1; i <= n; ++ i) printf("%d ", a[i]);
    printf("\n");
}