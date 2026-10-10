#pragma once
// Livro de ofertas com prioridade preço-tempo. Baseline com std::map.
// >>> OPCIONAL: implemente um layout plano (array de níveis + ring de ordens)
// e compare ns/op com `make bench`. A semântica abaixo é a referência.
#include <algorithm>
#include <cstdint>
#include <deque>
#include <functional>
#include <map>
#include <optional>
#include <unordered_map>
#include <vector>

enum class Side { Buy, Sell };

struct Fill {
    std::uint64_t maker;
    std::uint64_t taker;
    std::int64_t price;
    std::uint32_t qty;
};

class OrderBook {
public:
    std::vector<Fill> add(std::uint64_t id, Side side, std::int64_t price, std::uint32_t qty) {
        std::vector<Fill> fills;
        if (side == Side::Buy) {
            match(fills, id, qty, price, asks_, true);
            if (qty > 0) {
                bids_[price].push_back(Order{id, qty});
                loc_[id] = {Side::Buy, price};
            }
        } else {
            match(fills, id, qty, price, bids_, false);
            if (qty > 0) {
                asks_[price].push_back(Order{id, qty});
                loc_[id] = {Side::Sell, price};
            }
        }
        return fills;
    }

    bool cancel(std::uint64_t id) {
        auto it = loc_.find(id);
        if (it == loc_.end()) return false;
        const Loc l = it->second;
        loc_.erase(it);
        if (l.side == Side::Buy) {
            erase_from(bids_, l.price, id);
        } else {
            erase_from(asks_, l.price, id);
        }
        return true;
    }

    bool modify(std::uint64_t id, std::uint32_t new_qty) {
        auto it = loc_.find(id);
        if (it == loc_.end()) return false;
        if (new_qty == 0) return cancel(id);
        const Loc l = it->second;
        if (l.side == Side::Buy) {
            set_qty(bids_, l.price, id, new_qty);
        } else {
            set_qty(asks_, l.price, id, new_qty);
        }
        return true;
    }

    std::optional<std::int64_t> best_bid() const {
        if (bids_.empty()) return std::nullopt;
        return bids_.begin()->first;
    }
    std::optional<std::int64_t> best_ask() const {
        if (asks_.empty()) return std::nullopt;
        return asks_.begin()->first;
    }

    std::size_t bid_levels() const { return bids_.size(); }
    std::size_t ask_levels() const { return asks_.size(); }

private:
    struct Order {
        std::uint64_t id;
        std::uint32_t qty;
    };
    struct Loc {
        Side side;
        std::int64_t price;
    };

    template <typename Book>
    void match(std::vector<Fill>& fills, std::uint64_t taker, std::uint32_t& qty,
               std::int64_t limit, Book& book, bool buy) {
        while (qty > 0 && !book.empty()) {
            auto it = book.begin();
            const std::int64_t price = it->first;
            if (buy ? (price > limit) : (price < limit)) break;
            auto& dq = it->second;
            while (qty > 0 && !dq.empty()) {
                Order& maker = dq.front();
                const std::uint32_t traded = std::min(qty, maker.qty);
                fills.push_back(Fill{maker.id, taker, price, traded});
                qty -= traded;
                maker.qty -= traded;
                if (maker.qty == 0) {
                    loc_.erase(maker.id);
                    dq.pop_front();
                }
            }
            if (dq.empty()) book.erase(it);
        }
    }

    template <typename Book>
    void erase_from(Book& book, std::int64_t price, std::uint64_t id) {
        auto lv = book.find(price);
        if (lv == book.end()) return;
        auto& dq = lv->second;
        for (auto d = dq.begin(); d != dq.end(); ++d) {
            if (d->id == id) {
                dq.erase(d);
                break;
            }
        }
        if (dq.empty()) book.erase(lv);
    }

    template <typename Book>
    void set_qty(Book& book, std::int64_t price, std::uint64_t id, std::uint32_t qty) {
        auto lv = book.find(price);
        if (lv == book.end()) return;
        for (auto& o : lv->second) {
            if (o.id == id) {
                o.qty = qty;
                return;
            }
        }
    }

    std::map<std::int64_t, std::deque<Order>, std::greater<std::int64_t>> bids_;
    std::map<std::int64_t, std::deque<Order>, std::less<std::int64_t>> asks_;
    std::unordered_map<std::uint64_t, Loc> loc_;
};
