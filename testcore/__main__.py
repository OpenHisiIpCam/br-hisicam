from . import BR_HISICAM_ROOT, BASE_WORKDIR, DEVICE_LIST, BrHisiCam, hiburn
import os
import argparse
import logging


def make_all(br_hisicam):
    br_hisicam.make_all()


def show_params(br_hisicam):
    print(br_hisicam.make_board_info())


def deploy(br_hisicam):
    hiburn.boot(
        device_id=br_hisicam.board,
        uimage=os.path.join(br_hisicam.output_dir, "images/uImage"),
        rootfs=os.path.join(br_hisicam.output_dir, "images/rootfs.squashfs"),
        device_info=br_hisicam.make_board_info(),
        timeout=180
    )


# -------------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",      help="Enabel debug logging", action="store_true")
    parser.add_argument("-l", "--list",         help="List available devices", action="store_true")
    parser.add_argument("-b", "--board",        help="Target board ID", metavar="BOARD", type=str)
    parser.add_argument("-o", "--output_dir",   help=f"Output directory (default: {BASE_WORKDIR}/<BOARD>)", type=str)
    parser.add_argument("-c", "--clean",        help="Clean before building", action="store_true")

    subparsers = parser.add_subparsers(title="Action")
    for action in (
        make_all, deploy, show_params
    ):
        action_parser = subparsers.add_parser(action.__name__,
            help=action.__doc__.strip() if action.__doc__ else None
        )
        action_parser.set_defaults(action=action)

    args = parser.parse_args()

    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    if args.list:
        print("\n".join(DEVICE_LIST.keys()))
        exit(0)

    if args.output_dir is None:
        args.output_dir = os.path.join(BASE_WORKDIR, args.board)

    br_hisicam = BrHisiCam(
        board=args.board,
        output_dir=args.output_dir,
        clean=args.clean
    )

    args.action(br_hisicam)


if __name__ == "__main__":
    main()
