import sys

class shell_colours(object):
    default = '\033[0m'
    rfg_kbg = '\033[91m'
    gfg_kbg = '\033[92m'
    yfg_kbg = '\033[93m'
    mfg_kbg = '\033[95m'
    yfg_bbg = '\033[104;93m'
    bfg_kbg = '\033[34m'
    bold = '\033[1m'


class MsgUser(object):
    __debug = False
    __quiet = False

    @classmethod
    def debugOn(cls):
        cls.__debug = True

    @classmethod
    def debugOff(cls):
        cls.__debug = False

    @classmethod
    def quietOn(cls):
        cls.__quiet = True

    @classmethod
    def quietOff(cls):
        cls.__quiet = False

    @classmethod
    def isquiet(cls):
        return cls.__quiet

    @classmethod
    def isdebug(cls):
        return cls.__debug

    @classmethod
    def debug(cls, message, newline=True):
        if cls.__debug:
            mess = str(message)
            if newline:
                mess += "\n"
            sys.stderr.write(mess)

    @classmethod
    def message(cls, msg):
        if cls.__quiet:
            return
        print(msg)

    @classmethod
    def question(cls, msg):
        print(msg)

    @classmethod
    def skipped(cls, msg):
        if cls.__quiet:
            return
        print ("".join(
            (shell_colours.mfg_kbg, "[Skipped] ", shell_colours.default, msg)))

    @classmethod
    def ok(cls, msg):
        if cls.__quiet:
            return
        print ("".join(
            (shell_colours.gfg_kbg, "[OK] ", shell_colours.default, msg)))

    @classmethod
    def failed(cls, msg):
        print ("".join(
            (shell_colours.rfg_kbg, "[FAILED] ", shell_colours.default, msg)))

    @classmethod
    def bold(cls,msg):
        print ("".join(
            (shell_colours.bold,msg,shell_colours.default)))
        
    @classmethod
    def warning(cls, msg):
        if cls.__quiet:
            return
        print ("".join(
            (shell_colours.bfg_kbg,
             shell_colours.bold,
             "[Warning]",
             shell_colours.default, " ", msg)))


class Progress_bar(object):
    def __init__(self, x=0, y=0, mx=1, numeric=False, percentage=False):
        self.x = x
        self.y = y
        self.width = 50
        self.current = 0
        self.max = mx
        self.numeric = numeric
        self.percentage = percentage

    def update(self, reading):
        if MsgUser.isquiet():
            return
        percent = int(round(reading * 100.0 / self.max))
        cr = '\r'
        if not self.numeric and not self.percentage:
            bar = '#' * int(percent)
        elif self.numeric:
            bar = "/".join(
                (str(reading),
                 str(self.max))) + ' - ' + str(percent) + "%\033[K"
        elif self.percentage:
            bar = "%s%%" % (percent)
        sys.stdout.write(cr)
        sys.stdout.write(bar)
        sys.stdout.flush()
        self.current = percent
        if percent == 100:
            sys.stdout.write(cr)
            if not self.numeric and not self.percentage:
                sys.stdout.write(" " * int(percent))
                sys.stdout.write(cr)
                sys.stdout.flush()
            elif self.numeric:
                sys.stdout.write(" " * (len(str(self.max))*2 + 8))
                sys.stdout.write(cr)
                sys.stdout.flush()
            elif self.percentage:
                sys.stdout.write("100%")
                sys.stdout.write(cr)
                sys.stdout.flush()

