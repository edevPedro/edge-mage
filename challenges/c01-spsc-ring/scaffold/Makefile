CXX ?= c++
CXXFLAGS ?= -O2 -std=c++20 -pthread
BUILD := build

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_ring: tests/test_ring.cpp src/spsc_ring.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/test_ring.cpp -o $@

$(BUILD)/bench_ring: bench/bench_ring.cpp src/spsc_ring.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc bench/bench_ring.cpp -o $@

test: $(BUILD)/test_ring
	./$(BUILD)/test_ring

bench: $(BUILD)/bench_ring
	./$(BUILD)/bench_ring

bench-compare: $(BUILD)/bench_ring
	./$(BUILD)/bench_ring --compare

verify: $(BUILD)/test_ring $(BUILD)/bench_ring
	./$(BUILD)/test_ring
	./$(BUILD)/bench_ring --compare

clean:
	rm -rf $(BUILD)

.PHONY: test bench bench-compare verify clean
