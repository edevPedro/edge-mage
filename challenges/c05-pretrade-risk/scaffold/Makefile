CXX ?= c++
CXXFLAGS ?= -O2 -std=c++20 -pthread
BUILD := build

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_risk: tests/test_risk.cpp src/fix.hpp src/risk.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/test_risk.cpp -o $@

$(BUILD)/fuzz_risk: tests/fuzz_risk.cpp src/fix.hpp src/risk.hpp | $(BUILD)
	$(CXX) $(CXXFLAGS) -Isrc tests/fuzz_risk.cpp -o $@

test: $(BUILD)/test_risk
	./$(BUILD)/test_risk

test-risk: $(BUILD)/test_risk
	./$(BUILD)/test_risk

fuzz: $(BUILD)/fuzz_risk
	./$(BUILD)/fuzz_risk

verify: $(BUILD)/test_risk $(BUILD)/fuzz_risk
	./$(BUILD)/test_risk
	./$(BUILD)/fuzz_risk

clean:
	rm -rf $(BUILD)

.PHONY: test test-risk fuzz verify clean
