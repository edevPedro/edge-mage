// Testes de corretude da fila SPSC: FIFO, capacidade e concorrência.
#include "spsc_ring.hpp"

#include <cassert>
#include <cstdint>
#include <cstdio>
#include <thread>

int main() {
    // FIFO básico + esvaziar.
    {
        SpscRing<int, 8> q;
        assert(q.push(1));
        assert(q.push(2));
        assert(q.push(3));
        int v = 0;
        assert(q.pop(v) && v == 1);
        assert(q.pop(v) && v == 2);
        assert(q.pop(v) && v == 3);
        assert(!q.pop(v));
    }

    // Capacidade: enche até N e recusa o excedente.
    {
        SpscRing<int, 4> q;
        for (int i = 0; i < 4; ++i) assert(q.push(i));
        assert(!q.push(99));
    }

    // Wraparound: enche, esvazia parcialmente, enche de novo.
    {
        SpscRing<int, 4> q;
        int v = 0;
        for (int i = 0; i < 4; ++i) assert(q.push(i));
        assert(q.pop(v) && v == 0);
        assert(q.pop(v) && v == 1);
        assert(q.push(10));
        assert(q.push(11));
        assert(!q.push(12));
        assert(q.pop(v) && v == 2);
        assert(q.pop(v) && v == 3);
        assert(q.pop(v) && v == 10);
        assert(q.pop(v) && v == 11);
    }

    // Produtor/consumidor concorrente: soma = 0+1+...+(total-1).
    {
        SpscRing<int, 1024> q;
        constexpr long total = 200000;
        std::thread prod([&] {
            for (long i = 0; i < total; ++i) {
                while (!q.push(static_cast<int>(i))) {
                }
            }
        });
        std::int64_t sum = 0;
        int v = 0;
        for (long i = 0; i < total; ++i) {
            while (!q.pop(v)) {
            }
            sum += v;
        }
        prod.join();
        const std::int64_t expect = static_cast<std::int64_t>(total - 1) * total / 2;
        assert(sum == expect);
    }

    std::puts("OK");
    return 0;
}
