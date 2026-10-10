// mage_bench.hpp — utilitários de medição para labs do e-mage.
//
// Uso (bench.cpp):
//   #include "mage_bench.hpp"
//   ...
//   mage::emit_bench("{\"correct\":1,\"latency_ns\":{\"p50\":..,\"p99\":..,\"p999\":..},"
//                    "\"throughput_ops_s\":..,\"ops\":..}");
//
// O runner roda o binário N vezes e agrega as métricas entre execuções; o
// benchmark deve reportar métricas por execução (com warmup interno).
#pragma once

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

namespace mage {

inline std::uint64_t now_ns() {
    using clock = std::chrono::steady_clock;
    return static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::nanoseconds>(
            clock::now().time_since_epoch())
            .count());
}

// Percentil com interpolação linear (q em 0..100).
inline double percentile_ns(std::vector<std::uint64_t> samples, double q) {
    if (samples.empty()) return 0.0;
    std::sort(samples.begin(), samples.end());
    const double rank = (q / 100.0) * static_cast<double>(samples.size() - 1);
    const std::size_t lo = static_cast<std::size_t>(rank);
    const std::size_t hi = (lo + 1 < samples.size()) ? lo + 1 : lo;
    const double frac = rank - static_cast<double>(lo);
    return static_cast<double>(samples[lo]) +
           (static_cast<double>(samples[hi]) - static_cast<double>(samples[lo])) * frac;
}

inline void emit_bench(const std::string& json) {
    std::printf("__MAGE_BENCH__ %s\n", json.c_str());
}

// Evita que o compilador elimine um valor observado.
template <typename T>
inline void keep(const T& value) {
    asm volatile("" : : "r,m"(value) : "memory");
}

}  // namespace mage
