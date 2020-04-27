<p align="center">
 <img src="images/hisilicon_buildroot300.png" alt="hisilicon_buildroot">
</p>

<h3 align="center">BR-HisiCam</h3>

---

<p align="center">Buildroot based sample firmware with embedded GoHisiCam for HiSilicon`s System-On-a-Chip ip cameras</p>
<p align="center"><em>Part of OpenHisiIpCam project</em></p>

## :pencil: Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deploy](#deploy)
- [Technical notes](#technical_notes)
- [Target hardware](#target_hardware)
- [Futher information](#futher_information)

## :eyeglasses: About <a name="about"></a>

Main task of this repo is to bring ability to run [GoHisiCam](https://github.com/OpenHisiIpCam/gohisicam-releases) application
(*Audio/video core software for HiSilicon`s System-On-a-Chip ip cameras written in Go and C*). 
Also this repo can be used as starting point for ip camera research or some other associated project.

Here term **firmware** means full set of software needed for running embedded device. In our case it is bootloader, Linux kernel, filesystem, 
that contains full software set including system utilities, applications that manage audio/video pipeline, business logic and service functions.

Currently this repo covers just few tasks, it is mostly empty system that runs one application (that itself lacks all needed functionality), 
but we are working on improvement of different aspects of overall functionality.

## :checkered_flag: Getting started <a name="getting_started"></a>
This is quick tutorial how to prepare source tree and build kernel and root file system image.

All these were **developed and tested under Ubuntu 18.04/19.10 GNU/Linux OS**.
Supposed that everything will work on any modern GNU/Linux distro, deb based distros
most probably have same system dependency packages names, on other distros satisfy deps by yourself.

**1.** Clone repo:
```console
foo@bar:~$ git clone --recursive https://github.com/OpenHisiIpCam/br-hisicam --depth 1
```

**2.** Install required system packages:
```console
foo@bar:~$ sudo make install-ubuntu-deps
```
> Let us know if we miss some dependencies!

**3.** Prepare source tree:
```console
foo@bar:~$ make prepare
```
> During this step buidlroot source archive (~7MB) will be downloaded and unpacked.

**4.** List avalible boards/modules:
```console
foo@bar:~$ make list-configs 
jvt_s274h19v-l29_hi3519v101_imx274
unknown_unknown_hi3519v101_unknown
```

**5.** Build kernel and rootfs for choosen module:
```console
foo@bar:~$ make jvt_s274h19v-l29_hi3519v101_imx274_defconfig
```
> During build step, toolchain will be generated from scratch, that takes time and requires all deps sources to be downloaded.
> Download data amount is about 200MB.

:clock1230: Overall build process (dependencies download time not included) can take:
* about 15 minutes on Intel(R) Core(TM) i7-4770 CPU @ 3.40GHz, 16GB RAM
* about 20 minutes on Intel(R) Core(TM) i7-2600K CPU @ 3.40GHz, 16GB RAM
* about 50 minutes on Intel(R) Core(TM) i7-5500U CPU @ 2.40GHz, 8GB RAM
* about 22 minuts on Intel(R) Core(TM) i5-8250U CPU @ 1.6GHz, 8GB RAM

Directory `output/{module-name}/images` contains kernel and rootfs images:
```console
foo@br:~/br-firmware/output/jvt_s274h19v-l29_hi3519v101_imx274/images$ tree .
.
├── rootfs.squashfs	# XZ compressed SquashFS root file system
└── uImage		# U-Boot wrapped XZ compressed kernel image

0 directories, 2 files
```

Now you can deploy software to your camera module!

## :fire: Deploy <a name="deploy"></a>

> This short deploy guide assume that you are familiar with your hardware, 
> you made all wire (power, network and debug UART) connections and so on. 

### Prepare host machine

For developing purpose we recommend upload kernel and rootfs (as initramfs) into the RAM of the device, not writing it to ROM.
In this case your expiriments will not affect normal device operation, after reset/poweroff of the device it will be at same state 
as before, becasue ROM data will still contains factory firmware.

Such way requires access to device`s bootloader (U-Boot in our case) and supposed that it will have tftp, bootm commands 
and avalibity of network operation.

As U-Boot will download kernel and rootfs images via TFTP, you have to install and tune tftp server on your host machine.
In our case it will be `tftpd-hpa`, but you can use any you are familiar with.

```console
foo@bar:~$ sudo apt-get install tftpd-hpa
foo@bar:~$ cat /etc/default/tftpd-hpa 
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/home/foo/br-firmware/tftp" # <--- change path to your actual dir
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure"
```

After changes don`t forget to restart tftpd-hpa
```console
foo@bar:~$ sudo /etc/init.d/tftpd-hpa restart
```

Your test facility will be look like following schema.
<p align="center">
 <img src="images/deploy_schema500.png" alt="Deploy schema">
</p>

> Network configuration is sample, you can use any consistent network settings for your host machine and camera module.

### Upload software via U-Boot

Your USB-TTL adapter will be registered in system as /dev/ttyUSB0 or in some cases as /dev/ttyACM0.
You can use any serial terminal app like `putty`, `miniterm` or even `screen` 
99% of known camera modules have **U-Boot setuped for 115200,8n1 serial communication**.

After camera power on quickly press Ctrl+C (send Ctrl+C to camera trough serial connection) to interrupt normal boot process.
When you will catch U-Boot prompt `hisilicon #` (sometimes `xm #`, `Zview #`, etc) you ready to input commands.

**1.** Setup network settings and ip of tftp server (your host machine ip)
```console
hisilicon # setenv ipaddr 192.168.1.100; setenv netmask 255.255.255.0;  setenv serverip 192.168.1.1;
```

> Next steps will require chip and board specific information!
> **TODO**
> `make jvt_s274h19v-l29_hi3519v101_imx274_info`

**2.** Download kernel and rootfs images from your host machine tftp server
```console
hisilicon # tftp 0x82000000 uImage
hisilicon # tftp 0x82400000 rootfs.squashfs
```

**3.** Setup kernel boot params.
```console
hisilicon # setenv bootargs mem=64M console=ttyAMA0,115200 root=/dev/ram initrd=0x82400000,4M
```

**4.** Finally let U-Boot load Linux kernel
```console
hisilicon # bootm 0x82000000
```

*Deploy to ROM is another story and at the moment it is out of scope this document.*

## :notebook: Technical notes <a name="technical_notes"></a>

All system is built on top of the [Buildroot](https://buildroot.org/) (br for short).
HiSilicon SoCs support made as buildroot external tree (`br-ext-hisicam` dir). 
For some reason we need flexible way of vanilla kernel patching (we wanted to support orderable patches and files overlay apply),
so we made such extension.

### External tree structure
```shell
.	#br-ext-hisicam dir contains following data
├── Config.in
├── board
│   ├── hi3516av100				# hi3516av100 family dir
│   │   ├── hi3516av100.config			# key=value chip specific settings
│   │   ├── hi3516dv100.config			# ---//---
│   │   └── kernel				# patches and files overlay for vanilla kernel
│   │       ├── hi3516av100.generic.config	# kernel default config
│   │       ├── hi3516dv100.generic.config	# kernel default config
│   │       ├── overlay				# kernel files overlay dir
│   │       └── patches				# kernel patches dir
│   ├── hi3516av200				# o
│   ├── hi3516cv100				#  t
│   ├── hi3516cv200				#   h
│   ├── hi3516cv300				#    e
│   ├── hi3516cv500				#     r
│   ├── hi3516ev200				# families, orginized similar way
│   ├── jvt					# JVT modules dir
│   │   └── jvt_s274h19v-l29_hi3519v101_imx274	#
│   │       ├── config				# key=value board specific settings
│   │       └── kernel				# Kernel specific data, like configs, patches overlay
│   ├── ruision					# another module vendor dir
│   ├── ssqvision				# ---//---
│   ├── xm					# ---//---
│   └── generic                                 # generic boards dir
│       ├── unknown_unknown_hi3516av100_unknown # similar to vendor modules dir (jvt, xm, etc)
│       ├── unknown_unknown_hi3516av200_unknown # can be used for initial RnD with new modules
│       ├── ...
│       └── unknown_unknown_hi3519v101_unknown
├── configs					# all generic and board specific buildroot configs 
│   ├── jvt_s274h19v-l29_hi3519v101_imx274_defconfig
│   ├── unknown_unknown_hi3516av100_unknown_defconfig
│   ├── ...
│   └── unknown_unknown_hi3519v101_unknown_defconfig
├── external.desc
├── external.mk
├── linux				# kernel standard br package extension
│   ├── Config.ext.in			# inserts hisi_patcher after vanilla source tree unpack
│   └── linux-ext-hisi_patcher.mk	# see 17.20.2 linux-kernel-extensions (br manual)
└── package
    ├── gohisicam			# GoHisiCam package TODO 
    └── hisi_patcher			# package apply patches and file overlays in orderable way
```

Long story short, when it comes to kernel, after vanilla sources unpack, 
br will apply chip family patches, overlay chip family files, than so same for board specific data.
Exact actions are setuped in BR2_LINUX_KERNEL_EXT_HISI_PATCHER_LIST br config param 
(`cat ./br-ext-hisicam/configs/jvt_s274h19v-l29_hi3519v101_imx274_defconfig | grep BR2_LINUX_KERNEL_EXT_HISI_PATCHER_LIST`).

We recommend you take a look on [Buildroot documentation](https://buildroot.org/docs.html), in case you want detailed understanding externel tree ideology.

## :camera: Target hardware <a name="target_hardware"></a>

This project mostly targetted on HiSilicon based one cmos ip camera modules.

> More information about different ip camera modules in the [catalog](https://github.com/OpenHisiIpCam/modules-catalog).

We name modules according following schema `{vendor}_{model}_{chip}_{cmos}`.

Examples:
* jvt_s226h19v-l29_hi3519v101_imx226
* xm_ipg-83he20py-s_hi3516ev100_imx323
* jvt_s274h19v-l29_hi3519v101_imx274
* xm_ivg-hp201y-se_hi3516cv300_imx323
* ssqvision_on290h16d_hi3516dv100_imx290

Also there are generic profiles:
* unknown_unknown_hi3516dv100_unknown
* unknown_unknown_{chip}_unknown

Generic profile supposed to run on the module based on corresponding chip,
but only debug UART will works, other periphery like network, should be tuned.
Such profiles can be used as starting point for new modules research.

### Hardware structuring

HiSilicon has a lot of chips, not only special ip camera solutions, but also NVR/DVR and even smartphone SoCs.
Unfortunately it is hard to understand their naming policy, it is not random, but there is no strict patterns.
 
We split chips into groups, that we call **families**. Not sure that it is official HiSilicon`s term, 
but anyway such grouping reduce naming mess a bit.

**Family** - chips that have similar CPU architecture, similar audio/video pipeline hardware and shares same SDK.
Software across family is binary compatible. Family name is repeating some chip name from corresponding group, 
usually (but not always) that chip is most powerfull chip across the family.

### Chip families information

| chips                                                 | family        | kernel |
|-------------------------------------------------------|---------------|--------|
| hi3516av100, hi3516dv100                              | hi3516av100   |4.9.37  |
| hi3519v101,  hi3516av200                              | hi3516av200   |3.18.20 |
| hi3516cv100, hi3518cv100, hi3518ev100                 | hi3516cv100   |3.0.8   |
| hi3516cv200, hi3518ev200, hi3518ev201                 | hi3516cv200   |4.9.37  |
| hi3516cv300, hi3516ev100                              | hi3516cv300   |3.18.20 |
| hi3516cv500, hi3516dv300, hi3516av300                 | hi3516cv500   |4.9.37  |
| hi3516ev300, hi3516ev200, hi3516dv200, hi3518ev300    | hi3516ev200   |4.9.37  |
| hi3519av100                                           | hi3519av100   |4.9.37  |
| hi3559av100                                           | hi3559av100   |4.9.37  |

### Tests

At the moment test covers:
* load kernel and rootfs to RAM via uboot/tftp (hiburn test)
* successful linux start with simple network echo server (minimal kernel config test)
* GoHisiProbe **TODO** (kernel and sdk modules consitency, minimal board params test)

|Model                                          |Pass	|
|-----------------------------------------------|-------|
|jvt_s274h19v-l29_hi3519v101_imx274		|OK  	|
|xm_ivg-85hf20pya-s_hi3516ev200_imx307		|OK	|
|xm_53h20-s_hi3516cv100_imx122			|OK	|
|xm_ivg-hp203y-se_hi3516cv300_imx291		|OK	|
|xm_ivg-hp201y-se_hi3516cv300_imx323		|OK     |
|jvt_s323h16xf_hi3516cv300_imx323		|OK	|
|ruision_rs-h622qm-b0_hi3516cv300_imx323	|OK	|
|xm_ivg-85hg50pya-s_hi3516ev300_imx335		|Uboot locked |
|xm_ipg-83h50p-b_hi3516av100_imx178		|OK   	|
|xm_ipg-83he20py-s_hi3516ev100_imx323		|OK	|
|xm_ivg-83h80nv-be_hi3516av200_os08a10		|OK	|
|ssqvision_on335h16d_hi3516dv300_imx335		|OK	|
|jvt_s226h19v-l29_hi3519v101_imx226		|OK	|
|xm_53h20-ae_hi3516cv100_imx222			|OK	|
|xm_83h40pl-b_hi3516av100_ov4689		|OK	|
|ssqvision_unknown_hi3519v101_imx326		|Uboot net is not working |
|ssqvision_on290h16d_hi3516dv100_imx290		|OK	|


## :exclamation: Futher information <a name="futher_information"></a>

Story about full functional ip camera firmware is large topic that requires skills and knowledge from different areas. 
It`s really difficult to cover everything in once, so be patient, progress may not go as fast as you might expect.

Also at the moment we focused on [GoHisiCam](https://github.com/OpenHisiIpCam/gohisicam-releases) development and firmware is background task.

If you are interested in topic, we recommend you read our website and other [resources](https://www.openhisiipcam.org/resources/) 
(there are links to other websites and discussion groups about the topics).

