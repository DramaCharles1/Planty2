import sys
from datetime import datetime
from PlantyLib import PlantyCommands


def main():
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    planty_lib = PlantyCommands("/dev/ttyUSB0")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_argv = ["misc/", "settings.xml", "True", "False", True]
        print("main test")
        main()
        print("End main test")
