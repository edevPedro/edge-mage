#pragma once
// Harness de latência tick-to-trade em loopback UDP. Baseline: servidor echo em
// thread + cliente medindo RTT com timestamp monotônico.
//
// >>> OPCIONAL: adicione pinning (sched_setaffinity), huge pages (mmap
// MAP_HUGETLB) e isolcpus e compare antes/depois com `make bench-compare`.
// Fora do Linux, marque degraded e explique. A semântica abaixo é a referência.
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <stdexcept>
#include <thread>

class UdpEchoHarness {
public:
    UdpEchoHarness() {
        server_fd_ = ::socket(AF_INET, SOCK_DGRAM, 0);
        if (server_fd_ < 0) throw std::runtime_error("socket");
        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
        addr.sin_port = 0;
        if (::bind(server_fd_, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) < 0)
            throw std::runtime_error("bind");
        socklen_t len = sizeof(addr);
        if (::getsockname(server_fd_, reinterpret_cast<sockaddr*>(&addr), &len) < 0)
            throw std::runtime_error("getsockname");
        port_ = ntohs(addr.sin_port);

        timeval tv{};
        tv.tv_sec = 0;
        tv.tv_usec = 200000;  // 200 ms: deixa o loop ver `running_` no shutdown
        ::setsockopt(server_fd_, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

        client_fd_ = ::socket(AF_INET, SOCK_DGRAM, 0);
        if (client_fd_ < 0) throw std::runtime_error("socket cli");
        cli_addr_ = addr;

        running_.store(true);
        server_ = std::thread([this] { serve(); });
    }

    ~UdpEchoHarness() {
        running_.store(false);
        if (server_.joinable()) server_.join();
        if (server_fd_ >= 0) ::close(server_fd_);
        if (client_fd_ >= 0) ::close(client_fd_);
    }

    UdpEchoHarness(const UdpEchoHarness&) = delete;
    UdpEchoHarness& operator=(const UdpEchoHarness&) = delete;

    // Envia um timestamp monotônico e devolve o RTT observado (nanosegundos).
    double round_trip_ns() {
        const std::uint64_t ts = now_ns();
        if (::sendto(client_fd_, &ts, sizeof(ts), 0,
                     reinterpret_cast<const sockaddr*>(&cli_addr_), sizeof(cli_addr_)) < 0)
            throw std::runtime_error("sendto");
        std::uint64_t back = 0;
        const ssize_t n = ::recvfrom(client_fd_, &back, sizeof(back), 0, nullptr, nullptr);
        const std::uint64_t t1 = now_ns();
        if (n != static_cast<ssize_t>(sizeof(back))) throw std::runtime_error("recvfrom");
        return static_cast<double>(t1 - back);
    }

    std::uint16_t port() const { return port_; }

private:
    static std::uint64_t now_ns() {
        return static_cast<std::uint64_t>(
            std::chrono::duration_cast<std::chrono::nanoseconds>(
                std::chrono::steady_clock::now().time_since_epoch())
                .count());
    }

    void serve() {
        std::uint64_t buf = 0;
        while (running_.load(std::memory_order_relaxed)) {
            sockaddr_in peer{};
            socklen_t plen = sizeof(peer);
            const ssize_t n = ::recvfrom(server_fd_, &buf, sizeof(buf), 0,
                                         reinterpret_cast<sockaddr*>(&peer), &plen);
            if (n != static_cast<ssize_t>(sizeof(buf))) continue;
            ::sendto(server_fd_, &buf, sizeof(buf), 0,
                     reinterpret_cast<sockaddr*>(&peer), plen);
        }
    }

    int server_fd_ = -1;
    int client_fd_ = -1;
    std::uint16_t port_ = 0;
    sockaddr_in cli_addr_{};
    std::atomic<bool> running_{false};
    std::thread server_;
};
