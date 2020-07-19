host-go: $(OUT_DIR)/.config
	@echo "Build host-go 1.14.1" 
	$(BOARD_MAKE) \
		GO_VERSION=1.14.1 HOST_GO_HASH_FILE=$(ROOT_DIR)/extra/go.hash \
		GO_BOOTSTRAP_VERSION=1.14.1 HOST_GO_BOOTSTRAP_HASH_FILE=$(ROOT_DIR)/extra/go-bootstrap.hash \
		host-go
