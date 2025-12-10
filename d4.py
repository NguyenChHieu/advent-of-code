"""
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?
"""

# def main():
#     with open("input/4.txt") as f:
#         grid = [list(line.strip()) for line in f.readlines()]
#
#     rows = len(grid)
#     cols = len(grid[0])
#
#     directions = [(-1, -1), (-1, 0), (-1, 1),
#                   (0, -1),          (0, 1),
#                   (1, -1), (1, 0), (1, 1)]
#     ans = 0
#     for r in range(rows):
#         for c in range(cols):
#             if grid[r][c] == ".":
#                 continue
#             cnt = 0
#             for dr, dc in directions:
#                 nr, nc = r + dr, c + dc
#                 if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
#                     cnt += 1
#
#             if cnt < 4:
#                 ans += 1
#     return ans

"""
--- Part Two ---
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts might be able to access more rolls of paper, which they might also be able to remove. How many total rolls of paper could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible, using highlighted @ to indicate that a roll of paper is about to be removed, and using x to indicate that a roll of paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 rolls of paper can be removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves and their forklifts?
"""
from collections import defaultdict, deque


# BFS by layer, process each layer, update neighbors sequentially
def main():
    with open("input/4.txt") as f:
        grid = [list(line.strip()) for line in f.readlines()]
#         test = """..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@."""
#         grid = [list(line.strip()) for line in test.splitlines()]

    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ans = 0
    graph = defaultdict(set)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == ".":
                continue
            graph[(r, c)] = set()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                    graph[(r, c)].add((nr, nc))
                    graph[(nr, nc)].add((r, c))

    q = deque()
    for loc, nbs in graph.items():
        if len(nbs) >= 4: continue
        q.append(loc)

    while q:
        next_turn = deque()
        for loc in q:
            for nb in graph[loc]:
                graph[nb].remove(loc)
            del graph[loc]  # processed
            ans += 1
        for loc, nbs in graph.items():
            if len(nbs) >= 4: continue
            next_turn.append(loc)
        q = next_turn
    return ans


if __name__ == "__main__":
    print(main())
