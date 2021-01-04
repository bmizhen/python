import random

AIDENS = """
103
131
121
151
118
12
7
2
90
74
160
58
15
83
153
140
166
1
148
33
165
39
100
135
68
77
25
9
54
94
101
55
141
22
97
35
57
117
102
64
109
114
56
51
125
82
154
142
155
45
75
158
120
5
19
61
34
128
106
88
84
137
96
136
27
6
21
89
69
162
112
127
119
161
38
42
134
20
81
48
73
87
26
95
146
113
76
32
70
8
18
67
124
80
93
29
126
147
28
152
145
159"""

AIDENS = sorted([int(i) for i in AIDENS.split()])
AIDENS = [0, *AIDENS, AIDENS[-1] + 3]
print(AIDENS)


def one_or_three():
    if random.randint(1, 3) == 3:
        return 3
    return 1


def make_adapter_list(count):
    adapters = [0]
    for _ in range(count):
        adapters.append(adapters[-1] + one_or_three())

    adapters.append(adapters[-1] + 3)

    print(adapters)
    return adapters


def count_perms(adapters, largest, index):
    if index == len(adapters) - 1:
        return 1

    key = (largest, index)
    # if key in cache:
    #    return cache[key]

    current = adapters[index]
    if adapters[index + 1] - largest > 3:
        result = count_perms(adapters, current, index + 1)
    else:
        result = count_perms(adapters, largest, index + 1) \
                 + count_perms(adapters, current, index + 1)

    # cache[key] = result
    return result


# for i in range(10000):
#     cache = {}
#
#     if count_perms(make_adapter_list(10), 0, 1) == 13:
#         break
# else:
#     print("NOPE")

cache = {}
print(count_perms(AIDENS, 0, 1))
