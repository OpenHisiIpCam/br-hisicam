ROOT_DIR           := $(CURDIR)
BR_VER             := 2020.02
BR_DIR             := $(ROOT_DIR)/buildroot-$(BR_VER)
BR_EXT_HISICAM_DIR := $(ROOT_DIR)/br-ext-hisicam
SCRIPTS_DIR        := $(ROOT_DIR)/scripts
BOARDS             := $(shell ls -1 $(BR_EXT_HISICAM_DIR)/configs)

.PHONY: usage help prepare install-ubuntu-deps all toolchain toolchain-params run-tests overlayed-rootfs-%

usage help:
	@echo \
	"BR-HisiCam usage:\n\
	- make help|usage - print this help\n\
	- make install-ubuntu-deps - install system deps\n\
	- make prepare - download and unpack buildroot\n\
	- make list-configs - show avalible hardware configs list\n\
	- make BOARD=<BOARD-ID> all - build all needed for a board (toolchain, kernel and rootfs images)\n\
	- make BOARD=<BOARD-ID> board-info - write to stdout information about selected board\n\
	- make overlayed-rootfs-<FS-TYPE> ROOTFS_OVERLAYS=... - create rootfs image that contains original\n\
	  Buildroot target dir overlayed by some custom layers.\n\
	  Example:\n\
	      make overlayed-rootfs-squashfs ROOTFS_OVERLAYS=./examples/echo_server/overlay\n\
	"

$(ROOT_DIR)/buildroot-$(BR_VER).tar.gz:
	wget -O $@ --header="Host: buildroot.org" --no-check-certificate https://140.211.167.122/downloads/buildroot-$(BR_VER).tar.gz

$(BR_DIR): $(ROOT_DIR)/buildroot-$(BR_VER).tar.gz
	tar -C $(ROOT_DIR) -xf buildroot-$(BR_VER).tar.gz

prepare: $(BR_DIR)

install-ubuntu-deps:
	apt-get install wget build-essential make libncurses-dev

%_info:
	@cat $(BR_EXT_HISICAM_DIR)/board/$(subst _info,,$@)/config | grep RAM_LINUX_SIZE
	$(eval VENDOR 	:= $(shell echo $@ | cut -d "_" -f 1))
	$(eval FAMILY 	:= $(shell cat $(BR_EXT_HISICAM_DIR)/board/$(subst _info,,$@)/config | grep FAMILY | cut -d "=" -f 2))
	$(eval CHIP	:= $(shell echo $@ | cut -d "_" -f 3))
	@cat $(BR_EXT_HISICAM_DIR)/board/$(FAMILY)/$(CHIP).config


list-configs:
	@ls -1 $(BR_EXT_HISICAM_DIR)/configs


# -------------------------------------------------------------------------------------------------
BR_MAKE := $(MAKE) -C $(BR_DIR) BR2_EXTERNAL=$(BR_EXT_HISICAM_DIR)
OUT_DIR ?= $(ROOT_DIR)/output

# Buildroot considers relative paths relatively to its' own root directory. So we use absolute paths
# to avoid this ambiguity
override OUT_DIR := $(abspath $(OUT_DIR))
BOARD_MAKE := $(BR_MAKE) O=$(OUT_DIR)

# Try to read BOARD variable from initialized output directory
ifneq ($(realpath $(OUT_DIR)/.board),)
    ifndef BOARD
        $(eval BOARD := $(shell cat $(OUT_DIR)/.board))
        $(info -- Deal with BOARD=$(BOARD))
    endif
endif


# =================================================================================================
# everything below is for defined BOARD variable only
ifdef BOARD

FAMILY := $(shell cat $(BR_EXT_HISICAM_DIR)/board/$(BOARD)/config | grep FAMILY | cut -d "=" -f 2)
BOARD_DEFCONFIG := $(BR_EXT_HISICAM_DIR)/configs/$(BOARD)_defconfig

# -------------------------------------------------------------------------------------------------
# toolchain
ifndef FAMILY
    $(error "FAMILY variable must be defined")
endif

TOOLCHAIN_DEFCONFIG := $(BR_EXT_HISICAM_DIR)/configs/toolchains/$(FAMILY)_defconfig
TOOLCHAINS_DIR ?= $(ROOT_DIR)/toolchains
TOOLCHAIN_DIR := $(TOOLCHAINS_DIR)/$(FAMILY)

$(TOOLCHAIN_DIR): $(TOOLCHAIN_DEFCONFIG)
ifeq ($(USE_TOOLCHAIN_STORAGE),y)
	$(ROOT_DIR)/scripts/make_toolchain.sh --br $(BR_DIR) --td $(TOOLCHAINS_DIR) --family $(FAMILY) --use-storage
else
	$(ROOT_DIR)/scripts/make_toolchain.sh --br $(BR_DIR) --td $(TOOLCHAINS_DIR) --family $(FAMILY) 
endif 

toolchain: $(TOOLCHAIN_DIR)

toolchain-menuconfig:
	rm -rf $(BR_DIR)/output
	$(BR_MAKE) BR2_DEFCONFIG=$(TOOLCHAIN_DEFCONFIG) defconfig menuconfig savedefconfig

define CREATE_TOOLCHAIN_PARAMS
    eval $$($(BOARD_MAKE) -s --no-print-directory VARS=BR2_TOOLCHAIN_EXTERNAL_PREFIX printvars) \
    && $(SCRIPTS_DIR)/create_toolchain_binding.sh $(OUT_DIR)/host/bin $$BR2_TOOLCHAIN_EXTERNAL_PREFIX \
    > $(OUT_DIR)/toolchain-params.mk
endef

# -------------------------------------------------------------------------------------------------
# output directory initialization
$(OUT_DIR)/.config: $(BOARD_DEFCONFIG)
	rm -rf $(@D)
	$(BOARD_MAKE) BR2_DEFCONFIG=$< defconfig
	@echo $(BOARD) >$(@D)/.board


# -------------------------------------------------------------------------------------------------
# build all needed for a board
all: $(OUT_DIR)/.config $(TOOLCHAIN_DIR)
	$(SCRIPTS_DIR)/update_config_with_external_toolchain.sh $< $(TOOLCHAIN_DIR)
	$(BOARD_MAKE) all
	$(CREATE_TOOLCHAIN_PARAMS)


# -------------------------------------------------------------------------------------------------
# re-create params file
toolchain-params:
	$(CREATE_TOOLCHAIN_PARAMS)


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
	@cat $(BR_EXT_HISICAM_DIR)/board/$(BOARD)/config


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

endif  # ifdef BOARD
# =================================================================================================


# util stuff is below
UPPERCASE = $(shell echo $(1) | tr a-z A-Z)
