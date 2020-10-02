from collections import defaultdict

def multymap(pairs):
    result = defaultdict(list)
    for k, v in pairs:
        result[k].append(v)
    return result


def compress(query):
    """
    input: “foo=1&foo=2&foo=3&blah=a&blah=b”
    output: “foo=1,2,3&blah=a,b”
    """

    mmap = multymap(term.split('=') for term in query.split('&'))
    return '&'.join(f'{k}={",".join(v)}' for k, v in mmap.items())


print(compress('foo=1&foo=2&foo=3&blah=a&blah=b&baz=&baz='))
