from inspect import signature


class Multimap(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, [value])  # call super method to avoid recursion
        else:
            fns = self[key]
            for i, fn in enumerate(fns):
                if arg_num(fn) == arg_num(value):
                    fns[i] = value
                    break
            else:
                self[key].append(value)


class FnMultimap(dict):
    def __init__(self):
        dict.__setitem__(self, '__over_methods__', Multimap())
        super().__init__()

    def real_set(self, key, value):
        dict.__setitem__(self, key, value)  # call super method to avoid recursion

    def __setitem__(self, key, value):
        # if callable(value):
        # print(signature(value), value.__name__)

        if not callable(value) or '__init__' == key:
            dict.__setitem__(self, key, value)  # call super method to avoid recursion
        else:
            self['__over_methods__'][key] = value


def arg_num(fn):
    return len(signature(fn).parameters)


class Meta(type):
    def __prepare__(name, bases, **kwds):
        # print(name, bases, kwds)
        return FnMultimap()

    def __setattr__(self, key, value):
        print('Meta.__setattr__', key, value)
        if callable(value):
            self.__over_methods__[key] = value
        else:
            super().__setattr__(key, value)

    def __new__(mcs, name, bases, attributes):
        print(mcs, name, bases, type(attributes), attributes)

        def find_overloaded_call(self, name):
            if not name in self.__over_methods__:
                raise AttributeError

            fns = self.__over_methods__[name]

            def my_call(*args):
                for fn in fns:
                    # print("looking for fn", name, fn, len(args))
                    if arg_num(fn) == len(args) + 1:
                        return fn(self, *args)
                else:
                    raise AttributeError

            return my_call

        attributes.real_set('__getattr__', find_overloaded_call)

        def instance_set_fn_attr(self, name, value):
            print('set_fn_attr', name, value)

            if callable(value):
                self.__over_methods__[name] = value
            else:
                super(self.__class__, self).__setattr__(name, value)

        attributes.real_set('__setattr__', instance_set_fn_attr)

        return super(Meta, mcs).__new__(mcs, name, bases, attributes)


class Foo(metaclass=Meta):
    print('DEFINE FOO')

    def __init__(self):
        print('Foo.__init__')
        print(self, dir(self))
        self.b = 6
        print(self, dir(self))
        # self.b = 7

    def a(self, a):
        print("one", a)
        return a

    def a(self, a, b):
        print("two", a, b)
        return a * b


Foo.bar = lambda self, a: a * 2
Foo.bar = lambda self, a, b: a * b

# print(Foo)
# print(dir(Foo))

# print(type(Foo))
# print(type(Meta))

f = Foo()
f.f = 5

# print(dir(f))
# print('Foo.__setattr__', Foo.__setattr__)
# print('f.__setattr__', f.__setattr__)

print("foo:", Foo)

print(f.b)
print(f.a(30))
print(f.a(30, 50))

print(f.bar(2, 3))
print(f.bar(2))

# print(Foo.zzz())
# print(f.ABCD)
