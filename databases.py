from subprocess import Popen, PIPE, check_output
from sys import argv
import getpass

def main():

    directive = argv[1]

    if directive == 'stop':
        check_output(['docker', 'rm', '-f', 'redis-stack'])
    elif directive == 'start':
        check_output(['docker', 'run', '--name=redis-stack', '-d', '-p', '6379:6379', '-p', '8001:8001', 'redis/redis-stack:latest'])

if __name__ == "__main__":
        main()
