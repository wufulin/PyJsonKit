#encoding=utf-8

__author__ = 'wufulin'
__version__ = '1.0.0'

Inf = float('Inf')
NaN = float('NaN')
encoding = 'utf-8'
WhiteSpace = ' \t\n\r'
DIGIT = '0123456789'

def escape_whitespace(source, start):
    while True:
        ch = source[start:start + 1]
        if ch == ' ' or ch == '\r' or ch == '\n' or ch == '\t':
            start += 1
        else:
            break
    return start


def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return lineno, colno


def errmsg(msg, doc, pos, end=None):
    # Note that this function is called from _json
    lineno, colno = linecol(doc, pos)
    if end is None:
        fmt = '{0}: line {1} column {2} (char {3})'
        return fmt.format(msg, lineno, colno, pos)


#if __name__ == '__main__':
#    start = escape_whitespace("   aa", 0)
#    print(start)