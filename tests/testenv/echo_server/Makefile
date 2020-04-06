ifndef BR_HOST_DIR
    $(error BR_HOST_DIR variable MUST be defined)
endif

TOOLCHAIN_NAME := arm-buildroot-linux-uclibcgnueabi

CC := $(BR_HOST_DIR)/bin/$(TOOLCHAIN_NAME)-gcc

build:
	$(CC) --std=c11 -Os -o ./echo_server ./main.c
