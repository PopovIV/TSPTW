import warnings
from collections import defaultdict

MAX_EXHAUSTIVE = 10


def _matrix_to_dict(mat, op):
    """ converts matrix to the adjacency list

    :param mat: matrix to convert
    :return: adjacency list
    """
    # <node>: <nodes one can visit>
    # the nodes are sorted in ascending costs, the path from the node to itself is removed
    return {i: sorted(range(len(op)), key=op.__getitem__) for i, _ in enumerate(mat)}


def backtrack(t, *, start=0, end=0, search_all=True):
    """ find the hamiltonian cycle using the nearest neighbor and backtracking

    :param t: task
    :param start: start node
    :param end: end node
    :param search_all: bool, whether to find all the paths, or to return the first found
    :return: dict of <path>: <time>
    """
    if search_all and len(t.closeTime) > MAX_EXHAUSTIVE:
        warnings.warn("search_all is switched to `False` as the computation will take forever")
        search_all = False

    _start_node, _end_node = start, end

    # helper funcs
    _get_travel_time = lambda e: times[~0] + t.C[curr_node][e]
    _add_curr_time = lambda o: times + [max(_get_travel_time(o), t.openTime[o])]

    # <path>: <cost>
    res = {}
    # <node>: {<restricted nodes from the node>}
    prohibited = defaultdict(set)
    graph = _matrix_to_dict(t.C, t.closeTime)

    # setting initial state
    path = [_start_node]
    visited = {_start_node}
    times = [0]
    curr_node = _start_node
    while True:
        # try choosing the closest to the current node
        for node in graph[curr_node]:
            # check if the path to the node is a valid one
            if node not in visited and node not in prohibited[curr_node] and _get_travel_time(node) <= t.closeTime[node]:
                path.append(node)
                times = _add_curr_time(node)
                curr_node = node
                visited.add(node)
                break
        else:  # no node was chosen
            # some path was found
            if len(path) == len(graph):
                if search_all:
                    # add the curr result to the global result
                    res[(*path, _end_node)] = _add_curr_time(_end_node)[~0]
                else:  # return the first found
                    return (*path, _end_node), _add_curr_time(_end_node)[~0]
            # hopefully the condition to exit
            if len(path) == 1 and len(prohibited[path[0]]) == len(graph) - 1:
                return res
            # remove the last node, which didn't get us to the solution
            *path, to_remove = path
            curr_node = path[~0]
            visited -= {to_remove}
            times = times[:~0]
            # remove, because the path through these nodes might lie, though not in the current
            # order of the nodes
            # [0, 1, 3] -> not the solution
            # [0. 2, 1, 3, 4] -> solution
            prohibited.pop(to_remove, None)
            # prohibit the path from the `curr_node` to the `to_remove`
            # as the path doesn't move us toward the solution
            prohibited[curr_node].add(to_remove)
