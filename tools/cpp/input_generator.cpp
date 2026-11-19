/**
 * DevForge Input Generator
 * Generates structured random test cases (arrays, trees, strings, graphs) for competitive programming and fuzz testing.
 */

#include <iostream>
#include <vector>
#include <random>
#include <string>
#include <numeric>
#include <algorithm>

class InputGenerator {
public:
    explicit InputGenerator(uint64_t seed = 1337) : rng_(seed) {}

    int64_t random_int(int64_t min_val, int64_t max_val) {
        std::uniform_int_distribution<int64_t> dist(min_val, max_val);
        return dist(rng_);
    }

    std::vector<int64_t> random_array(size_t n, int64_t min_val, int64_t max_val) {
        std::vector<int64_t> arr(n);
        for (size_t i = 0; i < n; ++i) {
            arr[i] = random_int(min_val, max_val);
        }
        return arr;
    }

    std::vector<int64_t> permutation(size_t n, int64_t start = 1) {
        std::vector<int64_t> p(n);
        std::iota(p.begin(), p.end(), start);
        std::shuffle(p.begin(), p.end(), rng_);
        return p;
    }

    std::string random_string(size_t len, const std::string& charset = "abcdefghijklmnopqrstuvwxyz") {
        std::string s;
        s.reserve(len);
        for (size_t i = 0; i < len; ++i) {
            s += charset[random_int(0, charset.size() - 1)];
        }
        return s;
    }

    // Generates a random connected tree with N nodes as pairs of (u, v) (1-indexed)
    std::vector<std::pair<int, int>> random_tree(int n) {
        std::vector<std::pair<int, int>> edges;
        if (n <= 1) return edges;

        std::vector<int> p(n);
        std::iota(p.begin(), p.end(), 1);
        std::shuffle(p.begin(), p.end(), rng_);

        for (int i = 1; i < n; ++i) {
            int parent_idx = random_int(0, i - 1);
            edges.emplace_back(p[i], p[parent_idx]);
        }
        return edges;
    }

private:
    std::mt19937_64 rng_;
};

int main(int argc, char* argv[]) {
    std::string mode = "array";
    size_t count = 10;
    int64_t min_v = 1;
    int64_t max_v = 100;
    uint64_t seed = 42;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--mode" && i + 1 < argc) mode = argv[++i];
        else if (arg == "--count" && i + 1 < argc) count = std::stoull(argv[++i]);
        else if (arg == "--min" && i + 1 < argc) min_v = std::stoll(argv[++i]);
        else if (arg == "--max" && i + 1 < argc) max_v = std::stoll(argv[++i]);
        else if (arg == "--seed" && i + 1 < argc) seed = std::stoull(argv[++i]);
    }

    InputGenerator gen(seed);

    if (mode == "array") {
        auto arr = gen.random_array(count, min_v, max_v);
        std::cout << count << "\n";
        for (size_t i = 0; i < arr.size(); ++i) {
            std::cout << arr[i] << (i + 1 == arr.size() ? "" : " ");
        }
        std::cout << "\n";
    } else if (mode == "perm") {
        auto p = gen.permutation(count, min_v);
        std::cout << count << "\n";
        for (size_t i = 0; i < p.size(); ++i) {
            std::cout << p[i] << (i + 1 == p.size() ? "" : " ");
        }
        std::cout << "\n";
    } else if (mode == "string") {
        std::cout << gen.random_string(count) << "\n";
    } else if (mode == "tree") {
        auto edges = gen.random_tree(static_cast<int>(count));
        std::cout << count << "\n";
        for (const auto& e : edges) {
            std::cout << e.first << " " << e.second << "\n";
        }
    } else {
        std::cerr << "Unknown mode: " << mode << "\n";
        return 1;
    }

    return 0;
}
