#include "sum.hpp"

#include <cassert>
#include <cstdint>
#include <cstdio>

int main() {
    const std::int64_t xs[] = {1, 2, 3, 4, 5};
    assert(mage_sum(xs, 5) == 15);

    // n == 0 com ponteiro nulo deve ser seguro
    assert(mage_sum(nullptr, 0) == 0);

    const std::int64_t neg[] = {-10, 20, -30};
    assert(mage_sum(neg, 3) == -20);

    std::puts("OK");
    return 0;
}
