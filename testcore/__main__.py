from . import BR_HISICAM_ROOT, BASE_WORKDIR, DEVICE_LIST, BrHisiCam, hiburn
import os
import argparse
import logging


class make_all:
    @classmethod
    def run(cls, br_hisicam, args):
        br_hisicam.make_all()


class show_params:
    @classmethod
    def run(cls, br_hisicam, args):
        print(br_hisicam.make_board_info())


class deploy:
    """ Deploy firmware on a board
    """

    @classmethod
    def add_args(cls, parser):
        parser.add_argument("--rootfs-image", help=f"RootFS image path (default: <output_dir>/images/rootfs.squashfs", metavar="PATH")
        parser.add_argument("--uimage", help=f"Kernel's uImage path (default: <output_dir>/images/uImage", metavar="PATH")

    @classmethod
    def run(cls, br_hisicam, args):
        if args.rootfs_image is None:
            args.rootfs_image = os.path.join(br_hisicam.output_dir, "images/rootfs.squashfs")
        if args.rootfs_image is None:
            args.rootfs_image = os.path.join(br_hisicam.output_dir, "images/uImage")

        hiburn.boot(
            device_id=br_hisicam.board,
            uimage=os.path.join(br_hisicam.output_dir, "images/uImage"),
            rootfs=args.rootfs_image,
            device_info=br_hisicam.make_board_info(),
            timeout=180
        )


class show_ip:
    @classmethod
    def run(cls, br_hisicam, args):
        print(DEVICE_LIST[br_hisicam.board]["ip_addr"])


# -------------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",          help="Enabel debug logging", action="store_true")
    parser.add_argument("-l", "--list",             help="List available devices", action="store_true")
    parser.add_argument("-b", "--board",            help="Target board ID", metavar="BOARD", type=str)
    parser.add_argument("-o", "--output_dir",       help=f"Output directory (default: {BASE_WORKDIR}/<BOARD>)", type=str)
    parser.add_argument("-t", "--toolchains_dir",   help=f"Toolchains directory (default: {BASE_WORKDIR}/toolchains)", type=str)
    parser.add_argument("-c", "--clean",            help="Clean before building", action="store_true")

    subparsers = parser.add_subparsers(title="Action")
    for action in (
        make_all, deploy, show_params, show_ip
    ):
        action_help = action.__doc__.strip() if action.__doc__ else None
        action_parser = subparsers.add_parser(action.__name__, help=action_help)
        if hasattr(action, "add_args"):
            action.add_args(action_parser)
        action_parser.set_defaults(action=action.run)

    args = parser.parse_args()

    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    if args.list:
        print("\n".join(DEVICE_LIST.keys()))
        exit(0)

    if args.output_dir is None:
        args.output_dir = os.path.join(BASE_WORKDIR, args.board)
    if args.toolchains_dir is None:
        args.toolchains_dir = os.path.join(BASE_WORKDIR, "toolchains")

    br_hisicam = BrHisiCam(
        board=args.board,
        output_dir=args.output_dir,
        toolchains_dir=args.toolchains_dir,
        clean=args.clean
    )

    args.action(br_hisicam, args)


if __name__ == "__main__":
    main()
