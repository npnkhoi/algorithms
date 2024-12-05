#include <stdio.h>

// Return an index in lst[l:r] whose value equals x
// Return -1 if not found
int ter_search(int lst[], int l, int r, int x) {
    if (l > r) return -1;
    int ml = l + (r-l+1)/3;
    int mr = l + 2*(r-l+1)/3;
    if (lst[ml] > x) {
        return ter_search(lst, l, ml-1, x);
    }
    if (lst[ml] == x) {
        return ml;
    }
    if (lst[mr] > x) {
        return ter_search(lst, ml+1, mr-1, x);
    }
    if (lst[mr] == x) {
        return mr;
    }
    return ter_search(lst, mr+1, r, x);
}

int main() {
    // a sorted list of 15 random numbers
    int lst[20] = {4, 9, 10, 11, 11, 18, 27, 28, 33, 41, 44, 45, 46, 46, 47};
    int n = 15;
    printf("Initial list: ");
    for (int i = 0; i < n; ++ i) printf("%d ", lst[i]);
    printf("\n");

    printf("Enter value to find: ");
    int x;
    scanf("%d", &x);
    int ans = ter_search(lst, 0, n-1, x);
    if (ans == -1) {
        printf("Not found.\n");
    } else {
        printf("Found at index: %d\n", ans);
    }
}