#include "mage_bench.hpp"
#include "sum.hpp"

#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

int main() {
    constexpr std::size_t N = 1u << 20;  // 1 Mi elementos
    std::vector<std::int64_t> xs(N);
    std::int64_t expected = 0;
    for (std::size_t i = 0; i < N; ++i) {
        xs[i] = static_cast<std::int64_t>(i % 7) - 3;
        expected += xs[i];
    }

    // Correção rápida (o bench não substitui os testes, mas evita número bonito
    // sobre código errado).
    if (mage_sum(xs.data(), xs.size()) != expected) {
        std::printf("resultado incorreto\n");
        return 1;
    }

    constexpr int REPS = 2000;
    std::int64_t acc = 0;
    for (int r = 0; r < 100; ++r) {  // warmup interno
        acc += mage_sum(xs.data(), xs.size());
        mage::keep(acc);
    }

    std::vector<std::uint64_t> samples;
    samples.reserve(REPS);
    std::uint64_t total_ns = 0;
    for (int r = 0; r < REPS; ++r) {
        const std::uint64_t t0 = mage::now_ns();
        acc += mage_sum(xs.data(), xs.size());
        const std::uint64_t t1 = mage::now_ns();
        const std::uint64_t dt = t1 - t0;
        samples.push_back(dt);
        total_ns += dt;
    }
    mage::keep(acc);

    const double p50 = mage::percentile_ns(samples, 50);
    const double p99 = mage::percentile_ns(samples, 99);
    const double p999 = mage::percentile_ns(samples, 99.9);
    const double ops = static_cast<double>(REPS) * static_cast<double>(N);
    const double throughput = total_ns > 0 ? ops / (static_cast<double>(total_ns) / 1e9) : 0.0;

    std::string json = "{\"correct\":1,\"ops\":" + std::to_string(REPS * static_cast<long long>(N)) +
                       ",\"latency_ns\":{\"p50\":" + std::to_string(p50) +
                       ",\"p99\":" + std::to_string(p99) +
                       ",\"p999\":" + std::to_string(p999) +
                       "},\"throughput_ops_s\":" + std::to_string(throughput) + "}";
    mage::emit_bench(json);
    return 0;
}
