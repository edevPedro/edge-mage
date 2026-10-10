// Fuzzing determinístico: alimenta bytes aleatórios ao parser + risk engine.
// Prova que entradas malformadas nunca causam crash. Emite __MAGE_VERIFY__.
#include "fix.hpp"
#include "risk.hpp"

#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

int main() {
    std::mt19937_64 rng(0xC0FFEEULL);
    std::uniform_int_distribution<int> len_d(0, 512);
    std::uniform_int_distribution<int> byte_d(0, 255);
    const int iterations = 200000;
    RiskEngine eng;
    long parsed_ok = 0;
    for (int i = 0; i < iterations; ++i) {
        const int n = len_d(rng);
        std::vector<char> buf(static_cast<std::size_t>(n) + 1, 0);
        for (int j = 0; j < n; ++j) buf[static_cast<std::size_t>(j)] = static_cast<char>(byte_d(rng));
        FixMessage m;
        if (fix_parse(buf.data(), static_cast<std::size_t>(n), m)) {
            ++parsed_ok;
            eng.evaluate(m, static_cast<std::uint64_t>(i));
        }
    }
    std::fprintf(stderr, "fuzz: %d iterações, %ld parseadas sem crash\n", iterations, parsed_ok);
    std::printf("__MAGE_VERIFY__ {\"ok\": true, \"stage\": \"ok\", "
                "\"message\": \"fuzz sem crash\", \"metrics\": {\"fuzz_crashes\": "
                "{\"median\": 0, \"p50\": 0, \"p99\": 0, \"samples\": %d}}, "
                "\"runs\": %d, \"warmup\": 0}\n",
                iterations, iterations);
    return 0;
}
