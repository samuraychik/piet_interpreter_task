import argparse
import sys


def log_error(message):
    print("<ERROR>: " + message)
    sys.exit(1)


try:
    from piet_vitvit import piet_interpreter
except Exception as e:
    log_error(f"Couldn't find Piet interpreter module - {e}")


parser = argparse.ArgumentParser(
    description="Executes a program, written in Piet language")

parser.add_argument("filename", metavar="PATH", type=str,
                    help="path to your image with Piet code\n \
                    supported formats: .jpeg .png")
parser.add_argument("-s", "--size", type=int, default=1,
                    help="size of a single square codel in provided image \
                        (default: 1)")
parser.add_argument("-l", "--limit", type=int, default=10000,
                    help="maximum steps the interpreter will go through \
                        (default: 10000)")
parser.add_argument("-din", "--debuginter", action="store_true",
                    help="display debug messages from interpreter \
                        during code execution")
parser.add_argument("-dvm", "--debugvm", action="store_true",
                    help="display debug messages from virtual machine \
                        during code execution")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.size <= 0:
        log_error("Invalid codel size (must be non-negative)")
    if args.limit <= 0:
        log_error("Invalid steps limit (must be non-negative)")

    try:
        interpreter = piet_interpreter.PietInterpreter(args.filename,
                                                       args.size,
                                                       args.debuginter,
                                                       args.debugvm)
    except FileNotFoundError:
        log_error(f"Couldn't find Piet code image at PATH provided")

    try:
        for i in range(args.limit):
            interpreter.piet_step()
    except RecursionError:
        log_error(f"Provided Piet code has an overly deep recursion "
                  "(or a block with too many codels)")
    else:
        print("Steps limit reached")
