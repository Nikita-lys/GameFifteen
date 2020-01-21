"""
Лысенко Никита 4.8 2019

Решение игры "Пятнашки".

Пример работы:

Success!
Total elapsed: 0.101677 secs
123056789ABCDEF4 120356789ABCDEF4 127356089ABCDEF4 127356809ABCDEF4 1273568C9AB0DEF4 1273568C9AB4DEF0 1273568C9AB4DE0F 1273568C9A04DEBF 1273560C9A84DEBF 127356C09A84DEBF 127356C49A80DEBF 127356C49A08DEBF 127356049AC8DEBF 120356749AC8DEBF 123056749AC8DEBF 123456709AC8DEBF 123456789AC0DEBF 123456789A0CDEBF 123456789ABCDE0F 123456789ABCDEF0
Steps: 19

Success!
Total elapsed: 40.4318 secs
2F03716A5CD49E8B 20F3716A5CD49E8B 21F3706A5CD49E8B 21F37C6A50D49E8B 21F37C6A5D049E8B 21F37C6A5D849E0B 21F37C6A5D8490EB 21F37C6A50849DEB 21F3706A5C849DEB 21F3076A5C849DEB 01F3276A5C849DEB 10F3276A5C849DEB 17F3206A5C849DEB 17F3260A5C849DEB 17F326A05C849DEB 17F326A45C809DEB 17F326A45C089DEB 17F326A450C89DEB 17F320A456C89DEB 17F302A456C89DEB 17F352A406C89DEB 17F352A496C80DEB 17F352A496C8D0EB 17F352A496C8DE0B 17F352A49608DECB 17F3520496A8DECB 170352F496A8DECB 107352F496A8DECB 127350F496A8DECB 127356F490A8DECB 127356F49A08DECB 127356049AF8DECB 120356749AF8DECB 123056749AF8DECB 123456709AF8DECB 123456789AF0DECB 123456789AFBDEC0 123456789AFBDE0C 123456789A0BDEFC 123456789AB0DEFC 123456789ABCDEF0
Steps: 40

Success!
Total elapsed: 881.811 secs
51EAFD7B94C83260 51EAFD7B94C83206 51EAFD7B940832C6 51EAFD7B904832C6 51EAF07B9D4832C6 51EA0F7B9D4832C6 51EA9F7B0D4832C6 51EA9F7BD04832C6 51EA9F7BD24830C6 51EA9F7BD24803C6 51EA9F7B0248D3C6 51EA0F7B9248D3C6 01EA5F7B9248D3C6 10EA5F7B9248D3C6 1E0A5F7B9248D3C6 1E7A5F0B9248D3C6 1E7A5F4B9208D3C6 1E7A5F4B9028D3C6 1E7A5F4B9328D0C6 1E7A5F4B9328DC06 1E7A5F4B9328DC60 1E7A5F4B9320DC68 1E7A5F40932BDC68 1E7A5F04932BDC68 1E0A5F74932BDC68 1EA05F74932BDC68 1EA45F70932BDC68 1EA45F07932BDC68 1EA45F27930BDC68 1EA45F27903BDC68 1EA450279F3BDC68 10A45E279F3BDC68 1A045E279F3BDC68 1A245E079F3BDC68 1A245E379F0BDC68 1A245E379F6BDC08 1A245E379F6BD0C8 1A245E37906BDFC8 1A2450379E6BDFC8 10245A379E6BDFC8 12045A379E6BDFC8 12345A079E6BDFC8 12345A679E0BDFC8 12345A679EB0DFC8 12345A679EB8DFC0 12345A679EB8DF0C 12345A679EB8D0FC 12345A6790B8DEFC 123450679AB8DEFC 123456079AB8DEFC 123456709AB8DEFC 123456789AB0DEFC 123456789ABCDEF0
Steps: 52
"""

from timeit import default_timer as timer
from math import *
from heapq import heappush as insert, heappop as extract


class Node:
    def __init__(self, f, value, parent, g, h):
        # priority value for priority queue
        self.f = f
        self.value = value
        self.parent = parent
        # depth
        self.g = g
        # heuristic
        self.h = h

    # comparator for operation <
    def __lt__(self, other):
        if self.f < other.f:
            return True
        return False


def have_a_solve(state: list) -> bool:
    """ is start position have a solve? """
    sum = int(state.index('0') / 4 + 1)
    for i in range(16):
        for j in range(i + 1, 16):
            if state[j] < state[i] and state[j] != '0':
                sum += 1
    return sum % 2 == 0


def manhattan_distance(state: list) -> int:
    """ heuristic - manhattan distance """
    sum = 0
    for i in range(16):
        first = int(to10(state[i])) - 1
        second = i
        if first == -1:
            first = 15
        sum += abs(first % 4 - second % 4) + abs(int(first // 4) - int(second // 4))
    return sum


def get_heuristic(state: list) -> int:
    """ return h value """
    return manhattan_distance(state)


def get_f(g: int, h: int) -> int:
    """ return f value """
    return g + h


def to10(c: str) -> str:
    """ from 16 to 10 number system """
    if c == 'A':
        return '10'
    elif c == 'B':
        return '11'
    elif c == 'C':
        return '12'
    elif c == 'D':
        return '13'
    elif c == 'E':
        return '14'
    elif c == 'F':
        return '15'
    else:
        return c


def swap(state: list, pos1: int, pos2: int) -> str:
    """ swap 2 positions at the str state """
    return state[:pos1] + state[pos2] + state[pos1 + 1:pos2] + state[pos1] + state[pos2 + 1:]


# move up
def up(state):
    index_0 = state.index('0')
    if index_0 > 3:
        return swap(state, index_0 - 4, index_0)
    return False


def right(state):
    """ move right """
    index_0 = state.index('0')
    wrong = [3, 7, 11, 15]
    if index_0 not in wrong:
        return swap(state, index_0, index_0 + 1)
    return False


def down(state):
    """ move down """
    index_0 = state.index('0')
    if index_0 < 12:
        return swap(state, index_0, index_0 + 4)
    return False


def left(state):
    """ move left """
    index_0 = state.index('0')
    wrong = [0, 4, 8, 12]
    if index_0 not in wrong:
        return swap(state, index_0 - 1, index_0)
    return False


def a_star(state):
    """ algorithm A* """
    ideal = '123456789ABCDEF0'
    if not have_a_solve(state):
        print('No solution!')
        return []
    h = get_heuristic(state)
    g = 0
    node = Node(f=get_f(g, h), value=state, parent=None, g=g, h=h)
    pq = []         # priority queue
    insert(pq, node)
    res = list()    # list of result way
    close = set()
    while pq:
        cur = extract(pq)  # extract last node
        if cur.value == ideal:
            print('Success!')
            g = cur.g
            res.append(cur.value)
            while cur.parent:
                res.append(cur.parent.value)
                cur = cur.parent
            res.reverse()
            return res, g

        if cur.value not in close:
            close.add(cur.value)
            # add 4 ways to queue
            ways = [up(cur.value), right(cur.value), down(cur.value), left(cur.value)]
            for way in ways:
                if way:
                    h = get_heuristic(way)
                    g = cur.g + 1
                    node = Node(f=get_f(g, h), value=way, parent=cur, g=g, h=h)
                    insert(pq, node)


if __name__ == '__main__':
    state = '123056789ABCDEF4'

    start_time = timer()

    res, g = a_star(state)

    print("Total elapsed: {:g} secs".format(timer() - start_time))

    for x in res:
        print(x, end=' ')
    print('\nSteps: {}'.format(g))
