from collections import defaultdict


class Pathfinder:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, weight):
        self.graph[u].update({v: weight})

    def dfs_paths(self, start, goal):
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            for next_path in self.graph[vertex].keys() - set(path):
                if next_path == goal:
                    yield path + [next_path]
                else:
                    stack.append((next_path, path + [next_path]))

    def get_paths(self, start, goal):
        return list(self.dfs_paths(start, goal))

    def path_len(self, path):
        result = 0
        for i in range(len(path)-1):
            result += self.graph[path[i]][path[i+1]]
        return result


all_paths = [[2, 1], [1, 2], [1, 4], [4, 1], [1, 5], [5, 1], [4, 5], [5, 4], [5, 7], [7, 5], [4, 7], [7, 4], [3, 5], [5, 3], [3, 6], [6, 3], [7, 6], [6, 7], [8, 6], [6, 8]]


def find_route(green_routes, start, goal):
    f = Pathfinder()
    for route in all_paths:
        if route in green_routes:
            f.add_edge(route[0], route[1], 1)
        else:
            f.add_edge(route[0], route[1], 10)

    found_paths = f.get_paths(start, goal)
    found_paths.sort(key=f.path_len)
    return found_paths[0]

