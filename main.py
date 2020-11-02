import sys
from Commands import Commands


def looping(commander):
    """Enter your interactive mode for you user's input"""

    while True:
        commands = input('> ')
        if not commander.process(commands):
            break
    print("goodBye")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    loop = Commands()
    looping(loop)

