import sys

def main():
    print("lol")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_argv = ["misc/", "settings.xml", "True", "False", True]
        print("main test")
        main()
        print("End main test")
