#pragma once

#include <cstddef>
#include <cstdint>

inline std::int64_t mage_sum(const std::int64_t* xs, std::size_t n) {
    std::int64_t total = 0;
    for (std::size_t i = 0; i < n; ++i) {
        total += xs[i];
    }
    return total;
}
