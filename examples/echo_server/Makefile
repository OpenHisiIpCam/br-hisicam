OUT_DIR ?= $(CURDIR)/../../output
-include $(OUT_DIR)/toolchain-params.mk

DST := $(CURDIR)/overlay/bin/echo_server


$(DST):
	$(CC) --std=c11 -Os -o $@ ./main.c


build: $(DST)


rootfs-%:
	$(MAKE) -C $(CURDIR)/../.. overlayed-$@ \
	    OUT_DIR=$(abspath $(OUT_DIR)) \
	    ROOTFS_OVERLAYS=$(CURDIR)/overlay


clean:
	rm -f $(DST)
