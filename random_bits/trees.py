from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    data: str
    left: Any = None
    right: Any = None


def in_order_req(node: Node):
    if not node:
        return []
    return in_order_req(node.left) + [node.data] + in_order_req(node.right)


def pre_order_req(node: Node):
    if not node:
        return []
    return [node.data] + pre_order_req(node.left) + pre_order_req(node.right)


def post_order_req(node: Node):
    if not node:
        return []
    return post_order_req(node.left) + post_order_req(node.right) + [node.data]


@dataclass
class Kont:
    data: str
    next: Node

    def apply(self):
        return [self.data] + in_order_req(self.node)


def in_order_iter(node: Node, kont: Kont):
    result = []
    if not node:
        return result

    return in_order_req(node.left) + Kont(node.data, node.right).apply()


if __name__ == "__main__":
    h = Node("H")
    g = Node("G")
    f = Node("F")
    e = Node("E")
    d = Node("D", g, h)
    c = Node("C", f)
    b = Node("B", d, e)
    a = Node("A", b, c)

    print(a)
    print(pre_order_req(a))
    print(post_order_req(a))
    print(in_order_req(a))
    print(in_order_iter(a))
