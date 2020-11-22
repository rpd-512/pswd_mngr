#actual code was from the library stdiomask.
#this was edited just to meet the needs of the main.py
__version__ = '0.0.6'
import sys
STR_TYPE = str
RUNNING_PYTHON_2 = sys.version_info[0] == 2
if RUNNING_PYTHON_2:
    STR_TYPE = unicode
try:
    from typing import List
except ImportError:
    pass
if sys.platform == 'win32':
    from msvcrt import getch
    def getpass(prompt='Password: ', mask='*'):
        if RUNNING_PYTHON_2:
            if isinstance(prompt, str):
                prompt = prompt.decode('utf-8')
            if isinstance(mask, str):
                mask = mask.decode('utf-8')
        if not isinstance(prompt, STR_TYPE):
            raise TypeError('prompt argument must be a str, not %s' % (type(prompt).__name__))
        if not isinstance(mask, STR_TYPE):
            raise TypeError('mask argument must be a zero- or one-character str, not %s' % (type(prompt).__name__))
        if len(mask) > 1:
            raise ValueError('mask argument must be a zero- or one-character str')
        if mask == '' or sys.stdin is not sys.__stdin__:
            import getpass as gp
            return gp.getpass(prompt)
        enteredPassword = []
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = ord(getch())
            if key == 13:
                if RUNNING_PYTHON_2:
                    sys.stdout.write(STR_TYPE('\n'))
                else:
                    sys.stdout.write('\n')
                return ''.join(enteredPassword)
            elif key in (8, 127):
                if len(enteredPassword) > 0:
                    if RUNNING_PYTHON_2:
                        sys.stdout.write(STR_TYPE('\b \b'))
                    else:
                        sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    enteredPassword = enteredPassword[:-1]
            elif 0 <= key <= 31:
                pass
            else:
                char = chr(key)
                sys.stdout.write(mask)
                sys.stdout.flush()
                enteredPassword.append(char)

else:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def getpass(prompt='Password: ', mask='*'):
        if RUNNING_PYTHON_2:
            if isinstance(prompt, str):
                prompt = prompt.decode('utf-8')
            if isinstance(mask, str):
                mask = mask.decode('utf-8')
        if not isinstance(prompt, STR_TYPE):
            raise TypeError('prompt argument must be a str, not %s' % (type(prompt).__name__))
        if not isinstance(mask, STR_TYPE):
            raise TypeError('mask argument must be a zero- or one-character str, not %s' % (type(prompt).__name__))
        if len(mask) > 1:
            raise ValueError('mask argument must be a zero- or one-character str')

        if mask == '' or sys.stdin is not sys.__stdin__:
            import getpass as gp
            return gp.getpass(prompt)
        enteredPassword = []
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = ord(getch())
            if key == 13:
                if RUNNING_PYTHON_2:
                    sys.stdout.write(STR_TYPE('\n'))
                else:
                    sys.stdout.write('\n')
                return ''.join(enteredPassword)
            elif (key == 3):
                raise KeyboardInterrupt

            elif key in (8, 127):
                if len(enteredPassword) > 0:
                    if RUNNING_PYTHON_2:
                        sys.stdout.write(STR_TYPE('\b \b'))
                    else:
                        sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    enteredPassword = enteredPassword[:-1]
            elif 0 <= key <= 31:
                pass
            else:
                char = chr(key)
                sys.stdout.write(mask)
                sys.stdout.flush()
                enteredPassword.append(char)
