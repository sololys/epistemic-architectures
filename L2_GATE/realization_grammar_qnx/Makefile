CC      ?= gcc
CFLAGS  := -std=c11 -O2 -Wall -Wextra -Werror -pedantic -Wconversion -Wsign-conversion -Iinclude
ARCH    ?= x86_64

QNX_TARGET_x86_64    := gcc_ntox86_64
QNX_TARGET_aarch64le := gcc_ntoaarch64le
QNX_VARIANT          := $(QNX_TARGET_$(ARCH))
QNX_BUILD_DIR        := build/qnx_$(ARCH)

.PHONY: test verify qnx clean

test:
	mkdir -p build/host
	$(CC) $(CFLAGS) -o build/host/test_rg_invariants tests/test_rg_invariants.c src/rg_grammar.c
	./build/host/test_rg_invariants

verify: test

qnx:
	mkdir -p $(QNX_BUILD_DIR)
	qcc -V$(QNX_VARIANT) -std=gnu11 -O2 -Wall -Wextra -Werror -Iinclude \
		-o $(QNX_BUILD_DIR)/rg_qnx_resmgr src/qnx/rg_qnx_resmgr.c src/rg_grammar.c

clean:
	rm -rf build
