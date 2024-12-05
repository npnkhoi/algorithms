/*
Author: Khoi Nguyen

Implement Dijkstra's algorithm.
Your graph must have at least 10 vertices and 20 edges.
Print out the graph - list of vertices and edges(pair of vertices)
Run dijkstra's algorithm.
Print the tree that results - list of vertices in the tree (same as above) and list of edges that make up the tree.
You may use heap library. That is the only library you an use.
Submit the code and screen shots of execution results
*/

#include <stdio.h>
#include <vector>
#include <queue>
using namespace std;

const int V = 100, INF = 1e9;

vector<pair<int, int> > adj[V]; // Adjacency list
pair<int, int> dist[V]; // distance from source and the parent of each node
int v, e, s;
priority_queue< pair<int, int>, vector< pair<int, int> >, greater< pair<int, int> > > heap; // a min heap

/**
 * Dijkstra algorithm with heap
*/
void dijkstra(int s) {
    // Initialize distances from source
    for (int i = 0; i < v; ++ i) {
        dist[i] = make_pair(INF, -1);
    }
    dist[s].first = 0;

    // Initialize the heap
    heap.push(make_pair(0, s));

    // Keep getting the closest node from source to update others
    while (!heap.empty()) {
        pair<int, int> t = heap.top();
        heap.pop();
        int n1 = t.second, d = t.first;
        if (d != dist[n1].first) continue; // outdated value in the heap
        for (pair<int, int> edge : adj[n1]) {
            int n2 = edge.first, w = edge.second;
            if (d + w < dist[n2].first) {
                dist[n2] = make_pair(d + w, n1);
                heap.push(make_pair(dist[n2].first, n2));
            }
        }
    }
}

int main() {
    // Load the graph
    freopen("graph.txt", "r", stdin);
    scanf("%d %d %d", &v, &e, &s);
    for (int i = 0; i < e; ++ i) {
        int u, v, w;
        scanf("%d %d %d", &u, &v, &w);
        adj[u].push_back(make_pair(v, w));
        adj[v].push_back(make_pair(u, w)); // bidirectional edge
    }


    printf("--- The graph --- \n");
    printf("Vertices:\n");
    for (int i = 0; i < v; ++ i) {
        printf("%d ", i);
    }
    printf("\n");
    printf("Edges:\n");
    for (int u = 0; u < v; ++ u) {
        for (int j = 0; j < adj[u].size(); j++) {
            if (adj[u][j].first < u) continue;
            printf("%d %d %d\n", u, adj[u][j].first, adj[u][j].second);
        }
    }
    
    printf("--- Dijkstra result ---\n");
    printf("Nodes in the tree:\n");
    for (int i = 0; i < v; ++ i) {
        printf("%d ", i);
    }
    dijkstra(s);
    printf("\nEdges in the tree:\n");
    for (int i = 0; i < v; ++ i) {
        if (i == s || dist[i].first == INF) continue;
        printf("%d %d\n", dist[i].second, i);
    }
}