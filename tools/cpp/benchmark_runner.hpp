#ifndef DEVFORGE_BENCHMARK_RUNNER_HPP
#define DEVFORGE_BENCHMARK_RUNNER_HPP

#include <iostream>
#include <vector>
#include <chrono>
#include <functional>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <string>
#include <iomanip>

namespace devforge {

struct BenchmarkResult {
    std::string name;
    size_t iterations;
    double mean_ns;
    double median_ns;
    double min_ns;
    double max_ns;
    double stddev_ns;
};

class BenchmarkSuite {
public:
    explicit BenchmarkSuite(std::string suite_name) : suite_name_(std::move(suite_name)) {}

    void register_benchmark(const std::string& name, std::function<void()> func, size_t warmup = 5, size_t iterations = 50) {
        // Warmup runs
        for (size_t i = 0; i < warmup; ++i) {
            func();
        }

        std::vector<double> timings;
        timings.reserve(iterations);

        for (size_t i = 0; i < iterations; ++i) {
            auto start = std::chrono::high_resolution_clock::now();
            func();
            auto end = std::chrono::high_resolution_clock::now();
            double duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
            timings.push_back(duration);
        }

        std::sort(timings.begin(), timings.end());

        double sum = std::accumulate(timings.begin(), timings.end(), 0.0);
        double mean = sum / iterations;
        double median = (iterations % 2 == 0)
            ? (timings[iterations / 2 - 1] + timings[iterations / 2]) / 2.0
            : timings[iterations / 2];

        double sq_sum = 0.0;
        for (double t : timings) {
            sq_sum += (t - mean) * (t - mean);
        }
        double stddev = std::sqrt(sq_sum / iterations);

        results_.push_back({
            name,
            iterations,
            mean,
            median,
            timings.front(),
            timings.back(),
            stddev
        });
    }

    void print_summary() const {
        std::cout << "\n=======================================================\n";
        std::cout << " DevForge Benchmark Suite: " << suite_name_ << "\n";
        std::cout << "=======================================================\n";
        std::cout << std::left << std::setw(25) << "Benchmark"
                  << std::right << std::setw(12) << "Iterations"
                  << std::setw(15) << "Mean (ns)"
                  << std::setw(15) << "Median (ns)"
                  << std::setw(15) << "Min (ns)"
                  << std::setw(15) << "Max (ns)"
                  << std::setw(15) << "StdDev (ns)"
                  << "\n";
        std::cout << std::string(112, '-') << "\n";

        for (const auto& r : results_) {
            std::cout << std::left << std::setw(25) << r.name
                      << std::right << std::setw(12) << r.iterations
                      << std::fixed << std::setprecision(1)
                      << std::setw(15) << r.mean_ns
                      << std::setw(15) << r.median_ns
                      << std::setw(15) << r.min_ns
                      << std::setw(15) << r.max_ns
                      << std::setw(15) << r.stddev_ns
                      << "\n";
        }
        std::cout << "=======================================================\n\n";
    }

    const std::vector<BenchmarkResult>& get_results() const {
        return results_;
    }

private:
    std::string suite_name_;
    std::vector<BenchmarkResult> results_;
};

} // namespace devforge

#endif // DEVFORGE_BENCHMARK_RUNNER_HPP
