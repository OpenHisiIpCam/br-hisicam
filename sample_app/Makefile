TOOLCHAIN_PARAMS ?= $(abspath $(CURDIR)/../output/jvt_s274h19v-l29_hi3519v101_imx274/toolchain-params.mk)
include $(TOOLCHAIN_PARAMS)

all:
	$(CC) --std=c11 -Os -o ./echo_server ./main.c

clean:
	rm -f ./echo_server
