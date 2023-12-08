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
                    help="path to your image with Piet code\n"
                    "supported formats: .jpeg .png")

parser.add_argument("-s", "--size", type=int, default=1,
                    help="size of a single square codel in provided image"
                    "(default: 1)")

parser.add_argument("-l", "--limit", type=int, default=10000,
                    help="maximum steps the interpreter will go through"
                    "(default: 10000)")

parser.add_argument("-d", "--debug", action="store_true",
                    help="run the code in debug mode")

parser.add_argument("-bp", "--breakpoint", type=int, default=1,
                    help="step, from which the interpreter will"
                    "start running in debug mode if enabled (default: 1)")


def run(inter: piet_interpreter.PietInterpreter, debug: bool, bp: int):
    if debug:
        log_debug_mode_on(debug, bp)
    try:
        for step in range(1, args.limit):
            if debug and step == bp:
                inter.start_debug()
            interpreter.piet_step()
    except RecursionError as e:
        log_error(f"Provided Piet code has an overly deep recursion "
                  f"(or a block with too many codels) - {e}")
    else:
        print("Steps limit reached")


def log_debug_mode_on(debug, bp):
    print("[SYS] DEBUG MODE")
    print(f"[SYS] Starting from breakpoint (STEP {bp}), the program\n"
            "[SYS] will be executed step by step, awaiting your input\n"
            "[SYS] before moving forward.")


if __name__ == "__main__":
    print()
    args = parser.parse_args()
    if args.size <= 0:
        log_error("Invalid codel size (must be positive)")
    if args.limit <= 0:
        log_error("Invalid steps limit (must be positive)")
    if args.breakpoint <= 0:
        log_error("Invalid breakpoint (must be positive)")

    try:
        interpreter = piet_interpreter.PietInterpreter(args.filename,
                                                       args.size)
    except FileNotFoundError:
        log_error(f"Couldn't find Piet code image at PATH provided")

    run(interpreter, args.debug, args.breakpoint)
