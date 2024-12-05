/*
b. Write a program to do BFS topological sort . your program must be able to catch the loop.
Run the program on the attached graphs.
submit screen shots of execution results.
submit the code
*/

#include <stdio.h>
#include <vector>
#include <set>
#include <queue>

using namespace std;

const int N = 1000;

vector<char> adj[N];
int n, indegree[N];
set<int> nodes;
bool cycle = false;

int main() {
    // Input
    int u, v;
    freopen("g2.txt", "r", stdin);
    while (scanf("%d %d", &u, &v) != EOF) {
        adj[u].push_back(v);
        nodes.insert(u);
        nodes.insert(v);
        indegree[v]++;
    }
    n = nodes.size();

    // BFS
    vector<int> order;
    queue<int> q;
    for (int i : nodes) {
        if (indegree[i] == 0) q.push(i);
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int i = 0; i < adj[u].size(); i++) {
            int v = adj[u][i];
            indegree[v]--;
            if (indegree[v] == 0) q.push(v);
        }
    }

    // Output
    if (order.size() != n) printf("Cycle detected\n");
    else {
        printf("Topological order: ");
        for (int i : order) printf("%d ", i);
        printf("\n");
    }
}