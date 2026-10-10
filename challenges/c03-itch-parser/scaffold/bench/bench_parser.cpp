// Throughput do parser: msgs/s. Emite __MAGE_VERIFY__ {json} no stdout.
#include "itch_parser.hpp"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <vector>

#include "frame_builder.hpp"

using clk = std::chrono::steady_clock;

static double msgs_per_s(const std::vector<std::uint8_t>& buf, std::uint64_t& sink) {
    const auto t0 = clk::now();
    ItchParser p(buf.data(), buf.size());
    Message m;
    std::uint64_t acc = 0;
    std::size_t n = 0;
    while (p.next(m)) {
        acc += m.order_ref + m.price + m.shares;
        ++n;
    }
    const auto t1 = clk::now();
    sink += acc;
    const double secs = std::chrono::duration<double>(t1 - t0).count();
    return static_cast<double>(n) / secs;
}

static double percentile(std::vector<double> xs, double p) {
    if (xs.empty()) return 0.0;
    std::sort(xs.begin(), xs.end());
    const double idx = (p / 100.0) * static_cast<double>(xs.size() - 1);
    return xs[static_cast<std::size_t>(idx + 0.5)];
}

int main() {
    const std::vector<std::uint8_t> buf = build_mixed(1000000);
    const int warmup = 2;
    const int reps = 11;
    std::uint64_t sink = 0;
    std::vector<double> v;
    for (int i = 0; i < warmup; ++i) msgs_per_s(buf, sink);
    for (int i = 0; i < reps; ++i) v.push_back(msgs_per_s(buf, sink));

    const double p50 = percentile(v, 50);
    const double p99 = percentile(v, 99);
    std::fprintf(stderr, "msgs/s: p50=%.3g p99=%.3g (n=%d)\n", p50, p99, reps);
    std::printf("__MAGE_VERIFY__ {\"ok\": true, \"stage\": \"ok\", "
                "\"message\": \"bench do parser\", \"metrics\": {\"msgs_per_s\": "
                "{\"median\": %.6g, \"p50\": %.6g, \"p99\": %.6g, \"samples\": %d}}, "
                "\"runs\": %d, \"warmup\": %d}\n",
                p50, p50, p99, reps, reps, warmup);
    return 0;
}
