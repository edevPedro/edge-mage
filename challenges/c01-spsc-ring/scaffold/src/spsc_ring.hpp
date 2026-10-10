#pragma once
// Fila SPSC. O objetivo é implementar a SpscRing de verdade; o stub abaixo é
// apenas uma delegação à fila com mutex (correta, porém NÃO lock-free). Comece
// fazendo `make test` passar e depois substitua por head/tail atômicos com
// padding de cache line, comparando com `make bench`.

#include <cstddef>
#include <deque>
#include <mutex>
#include <new>
#include <utility>

// Baseline de comparação: fila protegida por mutex.
template <typename T, std::size_t N>
class MutexQueue {
public:
    bool push(const T& v) {
        std::lock_guard<std::mutex> g(m_);
        if (q_.size() >= N) return false;
        q_.push_back(v);
        return true;
    }
    bool pop(T& out) {
        std::lock_guard<std::mutex> g(m_);
        if (q_.empty()) return false;
        out = std::move(q_.front());
        q_.pop_front();
        return true;
    }

private:
    std::deque<T> q_;
    std::mutex m_;
};

// >>> IMPLEMENTE: ring buffer SPSC lock-free.
// Dicas: índices head_ (produtor) e tail_ (consumidor) em std::atomic<std::size_t>,
// load/store com memory_order_acquire/release, capacidade potência de 2 e
// alignas(64) para evitar false sharing. Enquanto isso, delegue ao mutex.
template <typename T, std::size_t N>
class SpscRing {
public:
    bool push(const T& v) { return fallback_.push(v); }
    bool pop(T& out) { return fallback_.pop(out); }

private:
    MutexQueue<T, N> fallback_;
};
