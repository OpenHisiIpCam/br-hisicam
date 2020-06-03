```
16dv300 # printenv
arch=arm
baudrate=115200
board=hi3516dv300
board_name=hi3516dv300
bootargs=mem=512M console=ttyAMA0,115200 flashsize=8192M chiptype=25 AuthSerial=003E000000 DevVersion=0 UartConfig=1 rootwait root=/dev/mmcblk0p3 rootfstype=squashfs coherent_pool=2M blkdevparts=mmcblk0:1M@0(boot)ro,4M@1M(Kernel)ro,16M@5M(Rootfs)ro,128M@25M(AppLocal)ro,384M@153M(AppExt)ro,16M@737M(SysParaCusPara),1M@753M(SysStatus),2048M(data1),-(data2)
bootcmd=mmc read 0 0x82000000 0x800 0x2000;bootm 0x82000000
bootdelay=1
cpu=armv7
ethact=eth0
ipaddr=192.168.54.234
netmask=255.255.248.0
serverip=192.168.54.19
soc=hi3516dv300
stderr=serial
stdin=serial
stdout=serial
vendor=hisilicon
verify=n

Environment size: 703/262140 bytes
```
