ROOT_DIR           := $(CURDIR)
BR_VER             := 2020.02
BR_DIR             := $(ROOT_DIR)/buildroot-$(BR_VER)
BR_EXT_HISICAM_DIR := $(ROOT_DIR)/br-ext-hisicam
SCRIPTS_DIR        := $(ROOT_DIR)/scripts
BOARDS             := $(shell ls -1 $(BR_EXT_HISICAM_DIR)/configs)

.PHONY: usage help prepare install-ubuntu-deps all run-tests overlayed-rootfs-%

usage help:
	@echo \
	"BR-HisiCam usage:\n\
	- make help|usage - print this help\n\
	- make install-ubuntu-deps - install system deps\n\
	- make prepare - download and unpack buildroot\n\
	- make list-configs - show avalible hardware configs list\n\
	- make BOARD=<BOARD-ID> all - build all needed for a board (toolchain, kernel and rootfs images)\n\
	- make overlayed-rootfs-<FS-TYPE> ROOTFS_OVERLAYS=... - create rootfs image that contains original Buildroot target dir\n\
	  overlayed by some custom layers. Example: make overlayed-rootfs-squashfs ROOTFS_OVERLAYS=./examples/echo_server/overlay"

$(ROOT_DIR)/buildroot-$(BR_VER).tar.gz:
	wget -O $@ https://buildroot.org/downloads/buildroot-$(BR_VER).tar.gz

$(BR_DIR): $(ROOT_DIR)/buildroot-$(BR_VER).tar.gz
	tar -C $(ROOT_DIR) -xf buildroot-$(BR_VER).tar.gz

prepare: $(BR_DIR)

install-ubuntu-deps:
	apt-get install wget build-essential make libncurses-dev

%_info:
	@cat $(BR_EXT_HISICAM)/board/$(subst _info,,$@)/config | grep RAM_LINUX_SIZE
	$(eval VENDOR 	:= $(shell echo $@ | cut -d "_" -f 1))
	$(eval FAMILY 	:= $(shell cat $(BR_EXT_HISICAM)/board/$(subst _info,,$@)/config | grep FAMILY | cut -d "=" -f 2))
	$(eval CHIP	:= $(shell echo $@ | cut -d "_" -f 3))
	@cat $(BR_EXT_HISICAM)/board/$(FAMILY)/$(CHIP).config


list-configs:
	@ls -1 $(BR_EXT_HISICAM_DIR)/configs


# -------------------------------------------------------------------------------------------------
OUT_DIR ?= $(ROOT_DIR)/output

# Buildroot considers relative paths relatively to its' own root directory. So we use absolute paths
# to avoid ambiguity
override OUT_DIR := $(abspath $(OUT_DIR))
BOARD_MAKE := $(MAKE) -C $(BR_DIR) BR2_EXTERNAL=$(BR_EXT_HISICAM_DIR) O=$(OUT_DIR)


$(OUT_DIR)/.config:
ifndef BOARD
	@echo "Variable BOARD must be defined to initialize output directory" >&2 && exit 1
endif
	$(BOARD_MAKE) BR2_DEFCONFIG=$(BR_EXT_HISICAM_DIR)/configs/$(BOARD)_defconfig defconfig


$(OUT_DIR)/toolchain-params.mk: $(OUT_DIR)/.config
	eval $$($(BOARD_MAKE) -s --no-print-directory VARS=GNU_TARGET_NAME printvars) \
		&& $(SCRIPTS_DIR)/create_toolchain_binding.sh $(OUT_DIR)/host/bin $$GNU_TARGET_NAME > $@


# -------------------------------------------------------------------------------------------------
# build all needed for a board
all: $(OUT_DIR)/.config $(OUT_DIR)/toolchain-params.mk
	$(BOARD_MAKE) all


# -------------------------------------------------------------------------------------------------
# create rootfs image that contains original Buildroot target dir overlayed by some custom layers
# space-separated list of overlays
ROOTFS_OVERLAYS ?=
# overlayed rootfs directory
ROOTFS_OVERLAYED_DIR ?= $(OUT_DIR)/target-overlayed
# overlayed rootfs image's name (without prefix)
ROOTFS_OVERLAYED_IMAGE ?= rootfs-overlayed

overlayed-rootfs-%: $(OUT_DIR)/.config
	$(SCRIPTS_DIR)/create_overlayed_rootfs.sh $(ROOTFS_OVERLAYED_DIR) $(OUT_DIR)/target $(ROOTFS_OVERLAYS)
	$(BOARD_MAKE) $(subst overlayed-,,$@) \
	    BASE_TARGET_DIR=$(abspath $(ROOTFS_OVERLAYED_DIR)) \
	    ROOTFS_$(call UPPERCASE,$(subst overlayed-rootfs-,,$@))_FINAL_IMAGE_NAME=$(ROOTFS_OVERLAYED_IMAGE).$(subst overlayed-rootfs-,,$@)


# -------------------------------------------------------------------------------------------------
board-info:
	@cat $(BR_EXT_HISICAM_DIR)/board/$(BOARD)/config | grep RAM_LINUX_SIZE
	$(eval VENDOR 	:= $(shell echo $(BOARD) | cut -d "_" -f 1))
	$(eval FAMILY 	:= $(shell cat $(BR_EXT_HISICAM_DIR)/board/$(BOARD)/config | grep FAMILY | cut -d "=" -f 2))
	$(eval CHIP	:= $(shell echo $(BOARD) | cut -d "_" -f 3))
	@cat $(BR_EXT_HISICAM_DIR)/board/$(FAMILY)/$(CHIP).config


# -------------------------------------------------------------------------------------------------
# such targets (with trimmed `br-` prefix) are passed to Buildroot's Makefile
br-%: $(OUT_DIR)/.config
	$(BOARD_MAKE) $(subst br-,,$@)


# -------------------------------------------------------------------------------------------------
run-tests:
	$(MAKE) -C $(ROOT_DIR)/tests


# -------------------------------------------------------------------------------------------------
# there are some extra targets of specific packages
include $(sort $(wildcard $(ROOT_DIR)/extra/*.mk))


# -------------------------------------------------------------------------------------------------
# util stuff is below
UPPERCASE = $(shell echo $(1) | tr a-z A-Z)
