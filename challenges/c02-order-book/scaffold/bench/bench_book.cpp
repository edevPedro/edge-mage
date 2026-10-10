// Benchmark do livro: ns/op para add+cancel (baseline std::map).
// Emite __MAGE_VERIFY__ {json} no stdout.
#include "order_book.hpp"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <vector>

using clk = std::chrono::steady_clock;

static double run_once(long ops) {
    OrderBook book;
    std::uint64_t id = 1;
    const auto t0 = clk::now();
    for (long i = 0; i < ops; ++i) {
        const std::int64_t price = 100 + (i % 50);
        const Side side = (i % 2 == 0) ? Side::Buy : Side::Sell;
        book.add(id, side, price, 10);
        book.cancel(id);
        ++id;
    }
    const auto t1 = clk::now();
    const double ns = std::chrono::duration<double, std::nano>(t1 - t0).count();
    return ns / static_cast<double>(ops);
}

static double percentile(std::vector<double> xs, double p) {
    if (xs.empty()) return 0.0;
    std::sort(xs.begin(), xs.end());
    const double idx = (p / 100.0) * static_cast<double>(xs.size() - 1);
    return xs[static_cast<std::size_t>(idx + 0.5)];
}

int main() {
    const long ops = 200000;
    const int warmup = 3;
    const int reps = 15;
    std::vector<double> v;
    for (int i = 0; i < warmup; ++i) run_once(ops);
    for (int i = 0; i < reps; ++i) v.push_back(run_once(ops));

    const double p50 = percentile(v, 50);
    const double p99 = percentile(v, 99);
    const auto mm = std::minmax_element(v.begin(), v.end());
    std::fprintf(stderr, "map ns/op: p50=%.1f p99=%.1f (n=%d)\n", p50, p99, reps);
    std::printf("__MAGE_VERIFY__ {\"ok\": true, \"stage\": \"ok\", "
                "\"message\": \"bench do livro\", \"metrics\": {\"map_ns_per_op\": "
                "{\"median\": %.1f, \"p50\": %.1f, \"p99\": %.1f, \"min\": %.1f, "
                "\"max\": %.1f, \"samples\": %d}}, \"runs\": %d, \"warmup\": %d}\n",
                p50, p50, p99, *mm.first, *mm.second, reps, reps, warmup);
    return 0;
}
