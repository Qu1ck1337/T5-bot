import datetime

from tools.bcolors import bcolors


def console(pcolor: bcolors = bcolors.ENDC, *args):
    print(datetime.datetime.now().strftime("[%H:%M:%S] "), pcolor, *args, bcolors.ENDC, sep="")