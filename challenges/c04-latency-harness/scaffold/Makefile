CXX ?= c++
CXXFLAGS ?= -O2 -std=c++20 -pthread
BUILD := build

UNAME := $(shell uname -s)
ifeq ($(UNAME),Linux)
  LDFLAGS +=
endif

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_latency: tests/test_latency.cpp src/latency.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/test_latency.cpp -o $@ $(LDFLAGS)

$(BUILD)/bench_latency: bench/bench_latency.cpp src/latency.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc bench/bench_latency.cpp -o $@ $(LDFLAGS)

test: $(BUILD)/test_latency
	./$(BUILD)/test_latency

bench: $(BUILD)/bench_latency
	./$(BUILD)/bench_latency

bench-compare: $(BUILD)/bench_latency
	./$(BUILD)/bench_latency

verify: $(BUILD)/test_latency $(BUILD)/bench_latency
	./$(BUILD)/test_latency
	./$(BUILD)/bench_latency

clean:
	rm -rf $(BUILD)

.PHONY: test bench bench-compare verify clean
