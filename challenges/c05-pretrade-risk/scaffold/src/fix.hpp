#pragma once
// Parser FIX 4.4 mínimo (tag=valor separados por SOH) à prova de fuzzing.
// Zero alocação: escreve em buffers fixos e nunca lança.
//
// >>> OPCIONAL: estenda para grupos de mensagem, checksum (tag 10) e validação
// semântica. A semântica abaixo é a referência.
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>

constexpr char SOH = '\x01';
constexpr int kMaxTags = 32;
constexpr int kValMax = 64;

struct FixField {
    int tag = 0;
    char value[kValMax] = {0};
};

struct FixMessage {
    FixField fields[kMaxTags];
    int count = 0;

    const char* get(int tag) const {
        for (int i = 0; i < count; ++i) {
            if (fields[i].tag == tag) return fields[i].value;
        }
        return nullptr;
    }

    long get_int(int tag, long fallback = 0) const {
        const char* v = get(tag);
        if (!v || !*v) return fallback;
        char* end = nullptr;
        const long r = std::strtol(v, &end, 10);
        return (end == v) ? fallback : r;
    }

    double get_double(int tag, double fallback = 0.0) const {
        const char* v = get(tag);
        if (!v || !*v) return fallback;
        char* end = nullptr;
        const double r = std::strtod(v, &end);
        return (end == v) ? fallback : r;
    }
};

// Retorna true se parseou; `ok` fica false em mensagens malformadas (sem crash).
inline bool fix_parse(const char* data, std::size_t len, FixMessage& out) {
    out.count = 0;
    if (data == nullptr) return false;
    std::size_t i = 0;
    while (i < len && out.count < kMaxTags) {
        // tag
        int tag = 0;
        bool has_digit = false;
        while (i < len && data[i] != '=' && data[i] != SOH) {
            const char c = data[i];
            if (c < '0' || c > '9') break;
            tag = tag * 10 + (c - '0');
            has_digit = true;
            ++i;
        }
        if (!has_digit || i >= len || data[i] != '=') {
            // pula até o próximo SOH para tentar ressincronizar
            while (i < len && data[i] != SOH) ++i;
            if (i < len) ++i;
            continue;
        }
        ++i;  // consome '='
        FixField& f = out.fields[out.count];
        f.tag = tag;
        int j = 0;
        while (i < len && data[i] != SOH) {
            if (j < kValMax - 1) f.value[j++] = data[i];
            ++i;
        }
        f.value[j] = '\0';
        ++out.count;
        if (i < len && data[i] == SOH) ++i;
    }
    return out.count > 0;
}
