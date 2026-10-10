#pragma once
// Motor de pré-trade risk: valida NewOrderSingle/Cancel contra limites.
//
// >>> OPCIONAL: adicione limites por símbolo, kill-switch e cooldown por
// participante. A semântica abaixo é a referência.
#include <cstdint>
#include <cstring>

#include "fix.hpp"

enum class Verdict { Accept, RejectNotional, RejectCooldown, RejectMalformed, RejectCancel };

struct RiskLimits {
    double max_notional = 1'000'000.0;   // qty * price
    std::uint64_t cooldown_ns = 0;       // 0 = desligado
};

struct RiskDecision {
    Verdict verdict = Verdict::RejectMalformed;
    const char* reason = "malformed";

    bool accepted() const { return verdict == Verdict::Accept; }
};

class RiskEngine {
public:
    explicit RiskEngine(RiskLimits limits = {}) : limits_(limits) {}

    // `now_ns` injetado para testes determinísticos.
    RiskDecision evaluate(const FixMessage& msg, std::uint64_t now_ns) {
        const char* type = msg.get(35);  // MsgType: D=NewOrderSingle, F=Cancel
        if (type == nullptr || (type[0] != 'D' && type[0] != 'F')) {
            return {Verdict::RejectMalformed, "msgtype"};
        }
        if (type[0] == 'F') {  // cancel: checa existência da ordem
            const long ref = msg.get_int(41, -1);  // OrigClOrdID
            if (ref < 0) return {Verdict::RejectCancel, "cancel sem ref"};
            return {Verdict::Accept, "cancel ok"};
        }
        const double qty = msg.get_double(38, -1.0);
        const double price = msg.get_double(44, -1.0);
        if (qty <= 0.0 || price <= 0.0) return {Verdict::RejectMalformed, "preco/qtd"};
        const double notional = qty * price;
        if (notional > limits_.max_notional) return {Verdict::RejectNotional, "notional"};
        if (limits_.cooldown_ns > 0 && last_accept_ns_ != 0 &&
            now_ns - last_accept_ns_ < limits_.cooldown_ns) {
            return {Verdict::RejectCooldown, "cooldown"};
        }
        last_accept_ns_ = now_ns;
        return {Verdict::Accept, "ok"};
    }

private:
    RiskLimits limits_;
    std::uint64_t last_accept_ns_ = 0;
};
