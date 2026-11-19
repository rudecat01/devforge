#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>
#include "../../tools/cpp/benchmark_runner.hpp"

void test_benchmark_suite() {
    devforge::BenchmarkSuite suite("Unit Test Suite");
    volatile double dummy = 0.0;
    suite.register_benchmark("Math Computation", [&]() {
        for (int i = 0; i < 500; ++i) {
            dummy += std::sin(i * 0.1);
        }
    }, 2, 10);

    const auto& results = suite.get_results();
    assert(results.size() == 1);
    assert(results[0].name == "Math Computation");
    assert(results[0].iterations == 10);
    assert(results[0].mean_ns >= 0.0);
    assert(results[0].min_ns <= results[0].max_ns);
    std::cout << "✓ test_benchmark_suite passed\n";
}

int main() {
    std::cout << "Running C++ tool tests...\n";
    test_benchmark_suite();
    std::cout << "All C++ tests passed!\n";
    return 0;
}
