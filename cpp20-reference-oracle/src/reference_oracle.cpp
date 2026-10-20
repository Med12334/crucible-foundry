#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>
#include <cassert>

// Layers 27-31: C++20 High-Speed Ground-Truth Reference Oracle
// Provides O(V + E) Kahn Topological Cycle Detection and O(N * M) Levenshtein Edit Distance
// to benchmark AI-generated algorithmic solutions against exact reference outputs.
namespace crucible::foundry::oracle {

    class GraphAndDpReferenceOracle {
    public:
        // Returns true if directed dependency graph is a valid DAG (no cycles)
        static bool is_valid_dag_kahn(int num_nodes, const std::vector<std::pair<int, int>>& directed_edges) {
            std::vector<int> in_degree(num_nodes, 0);
            std::vector<std::vector<int>> adj(num_nodes);

            for (const auto& edge : directed_edges) {
                adj[edge.first].push_back(edge.second);
                in_degree[edge.second]++;
            }

            std::queue<int> zero_in;
            for (int i = 0; i < num_nodes; ++i) {
                if (in_degree[i] == 0) {
                    zero_in.push(i);
                }
            }

            int visited_count = 0;
            while (!zero_in.empty()) {
                int u = zero_in.front();
                zero_in.pop();
                visited_count++;

                for (int v : adj[u]) {
                    if (--in_degree[v] == 0) {
                        zero_in.push(v);
                    }
                }
            }
            return visited_count == num_nodes;
        }

        // Exact dynamic programming Levenshtein distance for code-patch diff grading
        static int compute_patch_edit_distance(const std::string& a, const std::string& b) {
            const size_t n = a.size();
            const size_t m = b.size();
            std::vector<int> prev(m + 1, 0), curr(m + 1, 0);

            for (size_t j = 0; j <= m; ++j) prev[j] = static_cast<int>(j);

            for (size_t i = 1; i <= n; ++i) {
                curr[0] = static_cast<int>(i);
                for (size_t j = 1; j <= m; ++j) {
                    int cost = (a[i - 1] == b[j - 1]) ? 0 : 1;
                    curr[j] = std::min({prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost});
                }
                prev = curr;
            }
            return prev[m];
        }
    };
}

int main() {
    using namespace crucible::foundry::oracle;

    std::vector<std::pair<int, int>> valid_dag = {{0, 1}, {1, 2}, {0, 3}, {3, 2}};
    std::vector<std::pair<int, int>> cyclic_graph = {{0, 1}, {1, 2}, {2, 0}};

    assert(GraphAndDpReferenceOracle::is_valid_dag_kahn(4, valid_dag) == true);
    assert(GraphAndDpReferenceOracle::is_valid_dag_kahn(3, cyclic_graph) == false);

    assert(GraphAndDpReferenceOracle::compute_patch_edit_distance("return a < b", "return a <= b") == 1);

    std::cout << "[LAYERS 27-31 C++20 REFERENCE ORACLE] DAG Cycle Detector & DP Patch Grader Verified!\n";
    return 0;
}
