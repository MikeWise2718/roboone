import argparse
import time
from palut import r1, c1, c2, c3, c4, c5, rst


def get_args():
    parser = argparse.ArgumentParser(description="Build PAL Layer ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # General Settings
    parser.add_argument("-v", "--verbosity", action='store', type=int, default=2,
                        help="0=Errors, 1=Quiet, 2=Normal, 3=Info, 4=Debug")
    parser.add_argument("-a", "--action", action='store',
                        required=False, help="build robot or br", default="br")

    # Output Files
    parser.add_argument("-og", "--outGraphFile", action='store',
                        required=False, help="Output Graph File", default="")

    # Animation Settings
    parser.add_argument("-tmax", "--tmax", action='store', type=int,
                        required=False, help="Animation Time - default zero is no animation", default=0)
    parser.add_argument("-fps", "--fps", action='store', type=int,
                        required=False, help="Frames (time clips) per second", default=12)

    args = parser.parse_args()
    return args


def main():
    startTime = time.time()

    args = get_args()

    print(f"{c1}PAL Layer Builder{rst}")
    if args.verbosity > 2:
        print(f"{c2}Action: {args.action}{rst}")

    actionarr = args.action
    sar = actionarr.split(",")
    for action in sar:

        if action == "l":
            action = "list"
        elif action == "br":
            action = "build_robot"
        else:
            print(f"{r1}Error: Invalid action {action}{rst}")
            exit(1)

    elapTime = time.time() - startTime
    print(f"{c1}Execution took {c2}{elapTime:.3f}{rst} secs ")


if __name__ == "__main__":
    main()
