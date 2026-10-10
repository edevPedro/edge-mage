// Testes de propriedade do livro: repouso, cancel, modify e matching preço-tempo.
#include "order_book.hpp"

#include <cassert>
#include <cstdio>
#include <cstring>
#include <vector>

static void test_resting_and_cancel() {
    OrderBook b;
    b.add(1, Side::Buy, 100, 10);
    b.add(2, Side::Buy, 99, 5);
    b.add(3, Side::Sell, 101, 7);
    assert(b.best_bid() == 100);
    assert(b.best_ask() == 101);
    assert(b.cancel(1));
    assert(b.best_bid() == 99);
    assert(!b.cancel(1));  // já cancelado
    assert(b.modify(2, 8));
    assert(b.cancel(3));
    assert(!b.best_ask().has_value());
}

static void test_match_price_time() {
    OrderBook b;
    // dois asks no mesmo preço: prioridade FIFO.
    b.add(10, Side::Sell, 100, 4);
    b.add(11, Side::Sell, 100, 6);
    auto fills = b.add(20, Side::Buy, 100, 5);
    assert(fills.size() == 2);
    assert(fills[0].maker == 10 && fills[0].qty == 4 && fills[0].price == 100);
    assert(fills[1].maker == 11 && fills[1].qty == 1 && fills[1].price == 100);
    assert(b.best_ask() == 100);
    // sobra 5 no ask 11; um buy de 5 casa o resto.
    auto f2 = b.add(21, Side::Buy, 100, 5);
    assert(f2.size() == 1 && f2[0].maker == 11 && f2[0].qty == 5);
    assert(!b.best_ask().has_value());
    // melhores preços: buy não cruza ask acima do limite.
    OrderBook c;
    c.add(1, Side::Sell, 100, 1);
    auto f3 = c.add(2, Side::Buy, 99, 1);
    assert(f3.empty());
    assert(c.best_bid() == 99 && c.best_ask() == 100);
    // match parcial e repouso do restante
    auto f4 = c.add(3, Side::Buy, 100, 2);
    assert(f4.size() == 1 && f4[0].qty == 1);
    assert(c.best_bid() == 100);
}

int main(int argc, char** argv) {
    const bool quick = (argc > 1 && std::strcmp(argv[1], "--quick") == 0);
    const bool match = (argc > 1 && std::strcmp(argv[1], "--match") == 0);
    if (quick || argc == 1) test_resting_and_cancel();
    if (match || argc == 1) test_match_price_time();
    std::puts("OK");
    return 0;
}
