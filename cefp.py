# -*- coding: utf-8 -*-

import functools


class CEFParser(object):
    TOKEN_BACKSLASH = '\\'
    TOKEN_PIPE = '|'
    TOKEN_SPACE = ' '
    TOKEN_EQUAL = '='
    TOKEN_ESCAPE = {
        'r': '\r',
        'n': '\n',
    }

    def _listify(func):
        @functools.wraps(func)
        def _(*args, **kwargs):
            return list(func(*args, **kwargs))
        return _

    def _dictify(func):
        @functools.wraps(func)
        def _(*args, **kwargs):
            return dict(zip(*[iter(func(*args, **kwargs))] * 2))
        return _

    @classmethod
    @_listify
    def split(cls, data, maxsplit=7):
        if not data.startswith('CEF:'):
            raise ValueError('invalid data')

        count = 0
        escape = False
        buf = []

        for idx, ch in enumerate(data):
            if count >= maxsplit:
                buf[:] = data[idx:]
                break

            if escape:
                # Multi-line only allowed in extension
                buf.append(ch)
                escape = False
                continue

            if ch == cls.TOKEN_BACKSLASH:
                escape = True
                continue

            if ch == cls.TOKEN_PIPE:
                yield ''.join(buf)
                buf[:] = []
                count += 1
                continue

            buf.append(ch)

        yield ''.join(buf)

    @classmethod
    @_dictify
    @_listify
    def splitext(cls, data):
        space = 0
        escape = False
        buf = []

        for ch in data:
            if escape:
                if ch in cls.TOKEN_ESCAPE:
                    ch = cls.TOKEN_ESCAPE[ch]

                buf.append(ch)
                escape = False
                continue

            if ch == cls.TOKEN_BACKSLASH:
                escape = True
                continue

            if ch == cls.TOKEN_SPACE:
                buf.append(ch)
                space = len(buf)
                continue

            if ch == cls.TOKEN_EQUAL:
                if space:
                    yield ''.join(buf[:space - 1])
                    buf[:space] = []

                yield ''.join(buf)
                buf[:] = []
                continue

            buf.append(ch)

        yield ''.join(buf)

    @classmethod
    def parse(cls, data):
        fields = cls.split(data)

        if len(fields) != 8:
            raise ValueError('invalid data')

        return {
            'version':   fields[0][4:],
            'device':    {
                'vendor':         fields[1],
                'product':        fields[2],
                'version':        fields[3],
                'event_class_id': fields[4],
            },
            'name':      fields[5],
            'severity':  fields[6],
            'extension': cls.splitext(fields[7].lstrip()),
        }


parse = CEFParser.parse


def main():
    import sys
    import json
    import select

    def dump(data):
        json.dump(parse(data), sys.stdout, indent=4)
        sys.stdout.write('\n')

    def dumpfp(fp):
        for data in iter(fp.readline, ''):
            dump(data.rstrip())

    rlist, _, _ = select.select([sys.stdin.fileno()], [], [], 0)
    if rlist or not sys.argv[1:]:
        dumpfp(sys.stdin)

    for data in sys.argv[1:]:
        dump(data)


if __name__ == '__main__':
    main()
