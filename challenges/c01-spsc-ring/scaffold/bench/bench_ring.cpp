// Benchmark de latência push→pop (ns/op) para SpscRing vs MutexQueue.
// Emite __MAGE_VERIFY__ {json} no stdout (contrato da plataforma) e texto no stderr.
#include "spsc_ring.hpp"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <cstring>
#include <string>
#include <thread>
#include <vector>

using clk = std::chrono::steady_clock;

template <typename Q>
static double ns_per_op(long iters) {
    Q q;
    const auto t0 = clk::now();
    std::thread prod([&] {
        for (long i = 0; i < iters; ++i) {
            while (!q.push(static_cast<int>(i))) {
            }
        }
    });
    int v = 0;
    for (long i = 0; i < iters; ++i) {
        while (!q.pop(v)) {
        }
    }
    prod.join();
    const auto t1 = clk::now();
    const double ns = std::chrono::duration<double, std::nano>(t1 - t0).count();
    return ns / static_cast<double>(iters);
}

static double percentile(std::vector<double> xs, double p) {
    if (xs.empty()) return 0.0;
    std::sort(xs.begin(), xs.end());
    const double idx = (p / 100.0) * static_cast<double>(xs.size() - 1);
    return xs[static_cast<std::size_t>(idx + 0.5)];
}

struct Stats {
    double median, p50, p99, min, max;
    std::size_t samples;
};

static Stats summarize(std::vector<double> xs) {
    Stats s{0, 0, 0, 0, 0, xs.size()};
    if (xs.empty()) return s;
    s.p50 = percentile(xs, 50);
    s.median = s.p50;
    s.p99 = percentile(xs, 99);
    auto mm = std::minmax_element(xs.begin(), xs.end());
    s.min = *mm.first;
    s.max = *mm.second;
    return s;
}

static void emit_metric(std::string& out, const char* name, const Stats& s) {
    char buf[256];
    std::snprintf(buf, sizeof(buf),
                  "\"%s\": {\"median\": %.1f, \"p50\": %.1f, \"p99\": %.1f, "
                  "\"min\": %.1f, \"max\": %.1f, \"samples\": %zu}",
                  name, s.median, s.p50, s.p99, s.min, s.max, s.samples);
    out += buf;
}

int main(int argc, char** argv) {
    const bool compare = (argc > 1 && std::strcmp(argv[1], "--compare") == 0);
    const long iters = 120000;
    const int warmup = 3;
    const int reps = 15;

    std::vector<double> spsc, mutex;
    for (int i = 0; i < warmup; ++i) {
        ns_per_op<SpscRing<int, 4096>>(iters);
        ns_per_op<MutexQueue<int, 4096>>(iters);
    }
    for (int i = 0; i < reps; ++i) {
        spsc.push_back(ns_per_op<SpscRing<int, 4096>>(iters));
        mutex.push_back(ns_per_op<MutexQueue<int, 4096>>(iters));
    }

    const Stats ss = summarize(spsc);
    const Stats sm = summarize(mutex);

    std::fprintf(stderr, "spsc  ns/op: p50=%.1f p99=%.1f (median %.1f, n=%zu)\n",
                 ss.p50, ss.p99, ss.median, ss.samples);
    std::fprintf(stderr, "mutex ns/op: p50=%.1f p99=%.1f (median %.1f, n=%zu)\n",
                 sm.p50, sm.p99, sm.median, sm.samples);
    if (compare) {
        const double ratio = (sm.p99 > 0) ? ss.p99 / sm.p99 : 0.0;
        std::fprintf(stderr, "spsc p99 / mutex p99 = %.2f  (esperado < 1.0)\n", ratio);
    }

    std::string metrics;
    emit_metric(metrics, "spsc_p99_ns", ss);
    metrics += ", ";
    emit_metric(metrics, "mutex_p99_ns", sm);

    std::printf("__MAGE_VERIFY__ {\"ok\": true, \"stage\": \"ok\", "
                "\"message\": \"bench concluído\", \"metrics\": {%s}, "
                "\"runs\": %d, \"warmup\": %d}\n",
                metrics.c_str(), reps, warmup);
    return 0;
}
