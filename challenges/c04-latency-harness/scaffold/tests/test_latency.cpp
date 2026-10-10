// Teste de corretude: o round-trip é consistente e os valores são válidos.
#include "latency.hpp"

#include <algorithm>
#include <cassert>
#include <cstdio>
#include <vector>

int main() {
    UdpEchoHarness h;
    assert(h.port() != 0);
    std::vector<double> rtts;
    for (int i = 0; i < 200; ++i) rtts.push_back(h.round_trip_ns());
    assert(rtts.size() == 200);
    const auto mm = std::minmax_element(rtts.begin(), rtts.end());
    assert(*mm.first > 0.0 && *mm.second > 0.0);
    assert(*mm.first <= *mm.second);
    std::fprintf(stderr, "rtt us: min=%.2f max=%.2f\n", *mm.first / 1000.0, *mm.second / 1000.0);
    std::puts("OK");
    return 0;
}
