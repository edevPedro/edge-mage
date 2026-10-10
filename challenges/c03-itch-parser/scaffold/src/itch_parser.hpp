#pragma once
// Parser de feed binário estilo ITCH, zero-copy. Baseline com memcpy sem
// alocação. >>> OPCIONAL: elimine cópias com reinterpret_cast/unions e trate
// endianness; a semântica abaixo é a referência.
#include <cstdint>
#include <cstring>

enum class MsgType : std::uint8_t { Add = 'A', Delete = 'D', Cancel = 'X' };

struct Message {
    MsgType type = MsgType::Add;
    std::uint64_t order_ref = 0;
    char side = '?';
    std::uint32_t shares = 0;
    std::uint64_t price = 0;
    char stock[9] = {0};
};

class ItchParser {
public:
    ItchParser(const std::uint8_t* data, std::size_t len) : p_(data), end_(data + len) {}

    bool next(Message& out) {
        if (p_ + 2 > end_) return false;
        std::uint16_t mlen = 0;
        std::memcpy(&mlen, p_, 2);
        if (p_ + 2 + mlen > end_) return false;
        const std::uint8_t* q = p_ + 2;
        out = Message{};
        out.type = static_cast<MsgType>(q[0]);
        q += 1;
        switch (out.type) {
            case MsgType::Add:
                std::memcpy(&out.order_ref, q, 8); q += 8;
                out.side = static_cast<char>(*q); q += 1;
                std::memcpy(&out.shares, q, 4); q += 4;
                std::memcpy(&out.price, q, 8); q += 8;
                std::memcpy(out.stock, q, 8); out.stock[8] = 0;
                break;
            case MsgType::Delete:
                std::memcpy(&out.order_ref, q, 8); q += 8;
                break;
            case MsgType::Cancel:
                std::memcpy(&out.order_ref, q, 8); q += 8;
                std::memcpy(&out.shares, q, 4); q += 4;
                break;
            default:
                break;
        }
        p_ += 2 + mlen;
        return true;
    }

private:
    const std::uint8_t* p_;
    const std::uint8_t* end_;
};
