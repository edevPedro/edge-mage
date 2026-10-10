CXX ?= c++
CXXFLAGS ?= -O2 -std=c++20 -pthread
BUILD := build

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_parser: tests/test_parser.cpp src/itch_parser.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/test_parser.cpp -o $@

$(BUILD)/bench_parser: bench/bench_parser.cpp src/itch_parser.hpp tests/frame_builder.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc -Itests bench/bench_parser.cpp -o $@

$(BUILD)/alloc_probe: tests/alloc_probe.cpp src/itch_parser.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/alloc_probe.cpp -o $@

test: $(BUILD)/test_parser
	./$(BUILD)/test_parser

test-alloc: $(BUILD)/alloc_probe
	./$(BUILD)/alloc_probe

bench: $(BUILD)/bench_parser
	./$(BUILD)/bench_parser

verify: $(BUILD)/test_parser $(BUILD)/bench_parser
	./$(BUILD)/test_parser
	./$(BUILD)/bench_parser

clean:
	rm -rf $(BUILD)

.PHONY: test test-alloc bench verify clean
