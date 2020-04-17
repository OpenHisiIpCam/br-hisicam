BR_VER := 2020.02
BR_EXT_HISICAM := br-ext-hisicam
BOARDS := $(shell ls -1 $(BR_EXT_HISICAM)/configs)


usage:
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

run-tests:
	make -C tests

install-ubuntu-deps:
	apt-get install wget build-essential make libncurses-dev
