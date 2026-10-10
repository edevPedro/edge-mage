// Benchmark de latência: RTT em loopback UDP com warmup e percentis.
// Emite __MAGE_VERIFY__ {json} no stdout. p99 em microssegundos.
#include "latency.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdio>
#include <vector>

static double percentile(std::vector<double> xs, double p) {
    if (xs.empty()) return 0.0;
    std::sort(xs.begin(), xs.end());
    const double idx = (p / 100.0) * static_cast<double>(xs.size() - 1);
    return xs[static_cast<std::size_t>(idx + 0.5)];
}

int main() {
    UdpEchoHarness h;
    const int warmup = 2000;
    const int iters = 20000;
    for (int i = 0; i < warmup; ++i) h.round_trip_ns();
    std::vector<double> us;
    us.reserve(iters);
    for (int i = 0; i < iters; ++i) us.push_back(h.round_trip_ns() / 1000.0);

    const double p50 = percentile(us, 50);
    const double p99 = percentile(us, 99);
    const auto mm = std::minmax_element(us.begin(), us.end());
    std::fprintf(stderr, "rtt us: p50=%.2f p99=%.2f (n=%d)\n", p50, p99, iters);
    std::printf("__MAGE_VERIFY__ {\"ok\": true, \"stage\": \"ok\", \"degraded\": false, "
                "\"message\": \"latência loopback UDP\", \"metrics\": {\"rtt_p99_us\": "
                "{\"median\": %.3f, \"p50\": %.3f, \"p99\": %.3f, \"min\": %.3f, "
                "\"max\": %.3f, \"samples\": %d}}, \"runs\": %d, \"warmup\": %d}\n",
                p99, p50, p99, *mm.first, *mm.second, iters, iters, warmup);
    return 0;
}
