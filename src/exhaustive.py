from itertools import permutations


def exhaustive(t):
    """ computes the brute force salesman problem with time constraints

    :param t: task to solve
    :return: dictionary of pairs <path>: <cost>
    """
    # helper funcs
    _get_travel_time = lambda e: curr_time + t.C[curr_node][e]
    _get_curr_time = lambda o: max(_get_travel_time(o), t.openTime[o])

    _start_node, _end_node = 0, 0
    # get the permutations only on the nodes, which position is not
    # pre-determined
    _perm = set(range(len(t.openTime))) - {_start_node, _end_node}
    # path: cost
    res = {}
    assert len(_perm) < 12, "Way too many nodes, it'll take one forever to compute!"
    for comb in permutations(_perm, len(_perm)):
        curr_time = 0
        curr_node = _start_node
        for node_num in comb:
            # if salesman can visit until the node closes
            if _get_travel_time(node_num) <= t.closeTime[node_num]:
                curr_time = _get_curr_time(node_num)
            else:
                break
            curr_node = node_num
        # if the `break` wasn't fired
        else:
            res[(_start_node, *comb, _end_node)] = _get_curr_time(_end_node)
    return res
