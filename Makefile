BR_EXT_HISICAM := br-ext-hisicam
BR_VER := 2020.02
BOARDS := $(shell ls -1 $(BR_EXT_HISICAM)/configs)


.PHONY: toolchain-params.mk all run-tests usage help prepare


usage help:
	@echo "BR-HisiCam usage:"
	@echo "\t- make install-ubuntu-deps - install system deps"
	@echo "\t- make prepare - download and unpack buildroot"
	@echo "\t- make list-configs - show avalible hardware configs list"
	@echo "\t- make <board>_defconfig (example: make jvt_s274h19v-l29_hi3519v101_imx274_defconfig) - build software for choosen board"


buildroot-$(BR_VER).tar.gz:
	wget https://buildroot.org/downloads/buildroot-$(BR_VER).tar.gz

buildroot-$(BR_VER): buildroot-$(BR_VER).tar.gz
	tar -xf buildroot-$(BR_VER).tar.gz

prepare: buildroot-$(BR_VER)


%_info:
	@cat $(BR_EXT_HISICAM)/board/$(subst _info,,$@)/config | grep RAM_LINUX_SIZE
	$(eval VENDOR 	:= $(shell echo $@ | cut -d "_" -f 1))
	$(eval FAMILY 	:= $(shell cat $(BR_EXT_HISICAM)/board/$(subst _info,,$@)/config | grep FAMILY | cut -d "=" -f 2))
	$(eval CHIP	:= $(shell echo $@ | cut -d "_" -f 3))
	@cat $(BR_EXT_HISICAM)/board/$(FAMILY)/$(CHIP).config


list-configs:
	@ls -1 $(BR_EXT_HISICAM)/configs


%_defconfig:
	make -C buildroot-$(BR_VER) \
		O=../output/$(subst _defconfig,,$@) \
		BR2_EXTERNAL=../$(BR_EXT_HISICAM) \
		BR2_DEFCONFIG=../$(BR_EXT_HISICAM)/configs/$@ defconfig
	make -C output/$(subst _defconfig,,$@)
	ln -sf output/$(subst _defconfig,,$@)/images tftp

install-ubuntu-deps:
	apt-get install wget build-essential make libncurses-dev


# -------------------------------------------------------------------------------------------------
ROOT_DIR           := $(CURDIR)
BR_EXT_HISICAM_DIR := $(ROOT_DIR)/$(BR_EXT_HISICAM)
SCRIPTS_DIR        := $(BR_EXT_HISICAM_DIR)/scripts

OUT_DIR ?= $(ROOT_DIR)/output/$(BOARD)
# Buildroot considers relative paths relatively to its' root directory. So we use absolute paths
# to avoid ambiguity
override OUT_DIR := $(abspath $(OUT_DIR))


BOARD_MAKE := $(MAKE) -C buildroot-$(BR_VER) $\
    BR2_EXTERNAL=$(BR_EXT_HISICAM_DIR) $\
    BR2_DEFCONFIG=$(BR_EXT_HISICAM_DIR)/configs/$(BOARD)_defconfig $\
    O=$(OUT_DIR)


$(OUT_DIR)/.config:
	$(BOARD_MAKE) defconfig

$(OUT_DIR)/toolchain-params.mk: $(OUT_DIR)/.config
	eval $$($(BOARD_MAKE) -s VARS=GNU_TARGET_NAME printvars) \
		&& $(SCRIPTS_DIR)/create_toolchain_binding.sh $(OUT_DIR)/host/bin $$GNU_TARGET_NAME > $@

# create `toolchain-params.mk` that defines toolchain parameters for out-of-project builds
toolchain-params.mk: $(OUT_DIR)/toolchain-params.mk
	@echo Toolchain variables are defined in $(O)/toolchain-params.mk

# build all needed for a board
all: $(OUT_DIR)/.config params.mk
	$(BOARD_MAKE) all

# such targets (with trimmed `br-` prefix) are passed to Buildroot's Makefile
br-%: $(OUT_DIR)/.config
	$(BOARD_MAKE) $(subst br-,,$@)

run-tests:
	$(MAKE) -C tests





# there are some extra targets of specific packages
include $(sort $(wildcard $(ROOT_DIR)/targets/*.mk))
