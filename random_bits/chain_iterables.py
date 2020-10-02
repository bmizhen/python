a = {1:1,2:2}
b = {3:3,4:4}

def chain_iterables(*iterables):
    for it in iterables:
        yield from it


print(list(chain_iterables(a.items(), b.items())))

