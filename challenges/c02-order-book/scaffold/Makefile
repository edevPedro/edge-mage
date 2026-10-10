CXX ?= c++
CXXFLAGS ?= -O2 -std=c++20 -pthread
BUILD := build

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_book: tests/test_book.cpp src/order_book.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/test_book.cpp -o $@

$(BUILD)/bench_book: bench/bench_book.cpp src/order_book.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc bench/bench_book.cpp -o $@

test: $(BUILD)/test_book
	./$(BUILD)/test_book --quick

test-match: $(BUILD)/test_book
	./$(BUILD)/test_book --match

bench: $(BUILD)/bench_book
	./$(BUILD)/bench_book

bench-compare: $(BUILD)/bench_book
	./$(BUILD)/bench_book

verify: $(BUILD)/test_book $(BUILD)/bench_book
	./$(BUILD)/test_book
	./$(BUILD)/bench_book

clean:
	rm -rf $(BUILD)

.PHONY: test test-match bench bench-compare verify clean
