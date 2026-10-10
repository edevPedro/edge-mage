// Testes: parse FIX, limites de notional e cooldown.
#include "fix.hpp"
#include "risk.hpp"

#include <cassert>
#include <cstdio>
#include <cstring>
#include <string>

static std::string no(const char* sym, int qty, const char* px) {
    std::string s = "8=FIX.4.4";
    s += SOH;
    s += "35=D";
    s += SOH;
    s += "55=";
    s += sym;
    s += SOH;
    s += "54=1";
    s += SOH;
    s += "38=" + std::to_string(qty);
    s += SOH;
    s += "44=";
    s += px;
    s += SOH;
    return s;
}

int main() {
    FixMessage m;
    const std::string msg = no("MSFT", 100, "150.00");
    assert(fix_parse(msg.data(), msg.size(), m));
    assert(std::strcmp(m.get(55), "MSFT") == 0);
    assert(m.get_int(38) == 100);
    assert(m.get_double(44) == 150.0);
    assert(std::strcmp(m.get(35), "D") == 0);

    RiskLimits lim{};
    lim.max_notional = 20000.0;  // 100*150 = 15000 ok
    RiskEngine eng(lim);
    assert(eng.evaluate(m, 1'000'000'000).accepted());

    // excede notional
    FixMessage big;
    const std::string msg2 = no("AAPL", 100, "500.00");  // 50000 > 20000
    assert(fix_parse(msg2.data(), msg2.size(), big));
    assert(eng.evaluate(big, 2'000'000'000).verdict == Verdict::RejectNotional);

    // cooldown
    RiskLimits lim2{};
    lim2.max_notional = 1e9;
    lim2.cooldown_ns = 1'000'000'000ULL;  // 1s
    RiskEngine eng2(lim2);
    FixMessage ok;
    const std::string msg3 = no("MSFT", 10, "10.00");
    assert(fix_parse(msg3.data(), msg3.size(), ok));
    assert(eng2.evaluate(ok, 5'000'000'000ULL).accepted());
    assert(eng2.evaluate(ok, 5'500'000'000ULL).verdict == Verdict::RejectCooldown);
    assert(eng2.evaluate(ok, 6'500'000'000ULL).accepted());

    // malformada não crasha
    FixMessage bad;
    const char* junk = "garbage without separators";
    fix_parse(junk, std::strlen(junk), bad);
    assert(eng.evaluate(bad, 0).verdict == Verdict::RejectMalformed);

    std::puts("OK");
    return 0;
}
