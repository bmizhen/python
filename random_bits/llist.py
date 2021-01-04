from dataclasses import dataclass
from typing import Any


@dataclass
class LL:
    val: int
    next: Any = None


def mk_list():
    return LL(5, LL(4, LL(3, LL(2, LL(1)))))


print(mk_list())


def remove_element_rec(head: LL, val: int):
    if head is None:
        return None
    if val == head.val:
        return head.next
    else:
        head.next = remove_element_rec(head.next, val)
        return head


print(remove_element_rec(mk_list(), 3))

print(remove_element_rec(mk_list(), 5))


def remove_element_iter(head: LL, val: int):
    cur = head
    if cur.val == val:
        return cur.next

    while cur.next is not None:
        if cur.next.val == val:
            cur.next = cur.next.next
            return head
        else:
            cur = cur.next

    return head


print(remove_element_iter(mk_list(), 3))

print(remove_element_iter(mk_list(), 5))

print(remove_element_iter(mk_list(), 1))

print(remove_element_iter(mk_list(), 10))


@dataclass()
class l:
    head: LL


def remove_element_iter2(list_handle: l, val: int):
    cur = list_handle

    while cur.next is not None:
        if cur.next.val == val:
            cur.next = cur.next.next
            break
        else:
            cur = cur.next

    return l


print(remove_element_iter2(mk_list(), 3))

print(remove_element_iter2(mk_list(), 5))

print(remove_element_iter2(mk_list(), 1))

print(remove_element_iter2(mk_list(), 10))
