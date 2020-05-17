### Example of developing process
Buildroot encourages to create things as "packages". But we think that sometimes it's not the most convinient way to develop an app. Here is an example of alternative way.

This is an elementary TCP echo server. To build it for particular board you should use appropriate toolchain. Hence the Makefile includes `toolchain-params.mk` (resides in the output directory) that defines such tools like compiler, linker etc., but you may specify them on your own. When the app is built you will obviously want to deliver it to the board. The most common case is to put the application onto target's rootfs. Here we offers "overlay" for original Buildroot's target directory.

So, do this:
`make build`
to build the app and put it into `overlay/bin`. It'll try to include `<OUT_DIR>/toolchain-params.mk`
Then:
`make rootfs-squashfs`
to perform "overlaying" and create filesystem squashfs image. You may replace `squashfs` with your desired filesystem type. By default overlayed target dir is `<OUT_DIR>/target-overlayed/`, its' image is `<OUT_DIR>/images/rootfs-overlayed.squashfs`
