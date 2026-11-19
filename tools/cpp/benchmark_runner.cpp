#include "benchmark_runner.hpp"
#include <vector>
#include <algorithm>
#include <random>

int main() {
    devforge::BenchmarkSuite suite("Standard Library Operations");

    std::vector<int> sample_data(10000);
    std::mt19937 rng(42);
    for (auto& x : sample_data) {
        x = rng() % 100000;
    }

    suite.register_benchmark("Vector std::sort (10k)", [&]() {
        auto copy = sample_data;
        std::sort(copy.begin(), copy.end());
    }, 5, 20);

    suite.register_benchmark("Vector std::stable_sort (10k)", [&]() {
        auto copy = sample_data;
        std::stable_sort(copy.begin(), copy.end());
    }, 5, 20);

    suite.register_benchmark("Vector Linear Find", [&]() {
        auto it = std::find(sample_data.begin(), sample_data.end(), -999);
        (void)it;
    }, 10, 100);

    suite.print_summary();
    return 0;
}
