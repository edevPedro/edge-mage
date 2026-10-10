#pragma once
// Constrói um buffer binário estilo ITCH para testes e benchmark.
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

inline void put_u16(std::vector<std::uint8_t>& b, std::uint16_t v) {
    std::uint8_t tmp[2];
    std::memcpy(tmp, &v, 2);
    b.insert(b.end(), tmp, tmp + 2);
}
inline void put_u32(std::vector<std::uint8_t>& b, std::uint32_t v) {
    std::uint8_t tmp[4];
    std::memcpy(tmp, &v, 4);
    b.insert(b.end(), tmp, tmp + 4);
}
inline void put_u64(std::vector<std::uint8_t>& b, std::uint64_t v) {
    std::uint8_t tmp[8];
    std::memcpy(tmp, &v, 8);
    b.insert(b.end(), tmp, tmp + 8);
}

inline void add_message(std::vector<std::uint8_t>& b, std::uint64_t ref, char side,
                        std::uint32_t shares, std::uint64_t price, const char* stock) {
    put_u16(b, 30);
    b.push_back('A');
    put_u64(b, ref);
    b.push_back(static_cast<std::uint8_t>(side));
    put_u32(b, shares);
    put_u64(b, price);
    char s[8] = {0};
    std::strncpy(s, stock, 8);
    b.insert(b.end(), s, s + 8);
}

inline void delete_message(std::vector<std::uint8_t>& b, std::uint64_t ref) {
    put_u16(b, 9);
    b.push_back('D');
    put_u64(b, ref);
}

inline void cancel_message(std::vector<std::uint8_t>& b, std::uint64_t ref, std::uint32_t shares) {
    put_u16(b, 13);
    b.push_back('X');
    put_u64(b, ref);
    put_u32(b, shares);
}

inline std::vector<std::uint8_t> build_mixed(std::size_t n) {
    std::vector<std::uint8_t> b;
    b.reserve(n * 30);
    for (std::size_t i = 0; i < n; ++i) {
        switch (i % 3) {
            case 0:
                add_message(b, 1000 + i, (i % 2) ? 'B' : 'S', 100,
                            500000 + static_cast<std::uint64_t>(i), "AAPL");
                break;
            case 1:
                delete_message(b, 1000 + i);
                break;
            default:
                cancel_message(b, 1000 + i, 50);
                break;
        }
    }
    return b;
}
