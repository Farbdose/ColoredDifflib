from difflib import Differ, IS_CHARACTER_JUNK

from colorama import Fore, Back, Style


def mark_pos(string, pos, add=True, no_space=False):
    if len(pos)>0 and len(string) <= max(pos):
        pad = " "*(max(pos)+len(string)+1)
        string += pad

    new_pos = []

    if len(pos)>0:
        new_pos = [pos.pop(0)]
        expected = new_pos[0]+1
        n = None
        while len(pos)>0:
            n = pos.pop(0)

            if n != expected:
                new_pos.append(expected)
                new_pos.append(n)

            expected = n + 1

        if n is not None:
            new_pos.append(n+1)
        elif len(new_pos) != 0:
            new_pos.append(new_pos[0]+1)

        new_pos = [list(a) for a in zip(new_pos[::2], new_pos[1::2])]

    for p in reversed(new_pos):
        marked = string[p[0]:p[1]]
        layer = Back if marked.strip() == "" and not no_space else Fore
        color = layer.GREEN if add else layer.RED
        string = string[:p[0]] + color + marked + Style.RESET_ALL + string[p[1] if p[1] is None else p[1]:]
    return string

def color_diff(a, b, linejunk=None, charjunk=IS_CHARACTER_JUNK):
    differ = Differ(linejunk, charjunk).compare(a.splitlines(), b.splitlines())
    res = ["\n%s" % row.strip() for row in differ ]

    index = len(res)-1
    pos = []
    while index>=0:
        line = res[index]

        if len(line)>1:
            marker = "-" if line[0] == "$" else line[1]
            no_space = False
            if marker == "?":

                pos = [i for i,k in enumerate(line) if k!=" "][2:]

                res[index] = ""
            elif marker == "+" or marker == "^":
                if marker == "+" and len(pos) == 0 and index>0 and res[index-1][1] == "-":
                    pos = list(range(2,len(line)))
                    res[index-1] = "$"+res[index-1]
                    no_space = True
                res[index] = mark_pos(line, pos, True, no_space=no_space)
                pos = []
            elif marker == "-":
                if line[0] == "$":
                    line = line[1:]
                    pos = list(range(2,len(line)))
                    no_space = True
                res[index] = mark_pos(line, pos, False, no_space=no_space)
                pos = []
            else:
                res[index] = ""

        index-=1

    return "".join([line for line in res if line.strip() != ""]).strip()

if __name__ == "__main__":
    print("".join(color_diff("aba       aba   ",
                             "abbbbba   abbbba")))