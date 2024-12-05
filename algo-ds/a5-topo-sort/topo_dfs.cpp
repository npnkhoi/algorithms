/*
a. Write a program to do DFS topological sort . your program must be able to catch the loop.
Run the program on the attached graphs.
submit screen shots of execution results.
submit the code
*/

#include <stdio.h>
#include <iostream>
#include <vector>
#include <set>
#include <stack>

using namespace std;

const int N = 1000;

vector<char> adj[N];
int visited[N];
int n;
set<int> nodes;
bool cycle = false;
stack<int> order;

void dfs(int u) {
    visited[u] = 1;
    for (int i = 0; i < adj[u].size(); i++) {
        int v = adj[u][i];
        if (visited[v] == 0) dfs(v);
        if (visited[v] == 1) {
            cycle = true;
            return;
        }
    }
    order.push(u);
    visited[u] = 2;
}

int main() {
    // Input
    char u, v;
    string line;
    freopen("g1.txt", "r", stdin);
    while (cin >> u >> v) {
        // cout << u << ' ' << v << endl;
        adj[u].push_back(v);
        nodes.insert(u);
        nodes.insert(v);
    }
    n = nodes.size();

    // DFS
    for (int i : nodes) {
        if (visited[i] == 0) dfs(i);
        if (cycle) break;
    }

    // Output
    if (cycle) printf("Cycle detected\n");
    else {
        printf("Topological order: ");
        while (!order.empty()) {
            printf("%c ", order.top());
            order.pop();
        }
        printf("\n");
    }
}