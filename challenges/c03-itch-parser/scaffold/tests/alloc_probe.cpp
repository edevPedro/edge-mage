// Prova que o hot path do parser não aloca: instrumenta operator new/delete.
#include "itch_parser.hpp"

#include <atomic>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <new>

#include "frame_builder.hpp"

static std::atomic<long> g_allocs{0};

void* operator new(std::size_t n) {
    g_allocs.fetch_add(1, std::memory_order_relaxed);
    if (void* p = std::malloc(n)) return p;
    throw std::bad_alloc();
}
void* operator new[](std::size_t n) {
    g_allocs.fetch_add(1, std::memory_order_relaxed);
    if (void* p = std::malloc(n)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }

int main() {
    // Construa o buffer FORA da medição de alocação.
    std::vector<std::uint8_t> buf = build_mixed(100000);
    long parsed = 0;
    g_allocs.store(0, std::memory_order_relaxed);
    {
        ItchParser p(buf.data(), buf.size());
        Message m;
        while (p.next(m)) ++parsed;
    }
    const long allocs = g_allocs.load(std::memory_order_relaxed);
    std::printf("parsed=%ld allocs=%ld\n", parsed, allocs);
    assert(parsed > 0);
    assert(allocs == 0 && "hot path alocou memória");
    std::puts("OK");
    return 0;
}
