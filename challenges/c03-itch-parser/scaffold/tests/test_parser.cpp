// Testes do parser: Add/Delete/Cancel e fim de buffer.
#include "itch_parser.hpp"

#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

#include "frame_builder.hpp"

int main() {
    std::vector<std::uint8_t> buf;
    add_message(buf, 42, 'B', 100, 12345, "MSFT");
    delete_message(buf, 42);
    cancel_message(buf, 43, 10);

    ItchParser p(buf.data(), buf.size());
    Message m;

    assert(p.next(m));
    assert(m.type == MsgType::Add);
    assert(m.order_ref == 42);
    assert(m.side == 'B');
    assert(m.shares == 100);
    assert(m.price == 12345);
    assert(std::strcmp(m.stock, "MSFT") == 0);

    assert(p.next(m));
    assert(m.type == MsgType::Delete);
    assert(m.order_ref == 42);

    assert(p.next(m));
    assert(m.type == MsgType::Cancel);
    assert(m.order_ref == 43);
    assert(m.shares == 10);

    assert(!p.next(m));  // fim do buffer

    std::puts("OK");
    return 0;
}
