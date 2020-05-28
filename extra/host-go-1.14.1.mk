host-go: $(OUT_DIR)/.config
	@echo "Build host-go 1.14.1" 
	$(BOARD_MAKE) \
		GO_BOOTSTRAP_VERSION=1.14.1 HOST_GO_BOOTSTRAP_HASH_FILE=$(ROOT_DIR)/targets/go-bootstrap.hash \
		GO_VERSION=1.14.1 HOST_GO_HASH_FILE=$(ROOT_DIR)/targets/go.hash \
		host-go
