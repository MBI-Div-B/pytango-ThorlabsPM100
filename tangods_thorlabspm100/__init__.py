from .ThorlabsPM100Tango import ThorlabsPM100


def main():
    import sys
    import tango.server

    args = ["ThorlabsPM100"] + sys.argv[1:]
    tango.server.run((ThorlabsPM100,), args=args)
