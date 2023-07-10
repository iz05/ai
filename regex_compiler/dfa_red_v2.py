import sys

def display_dict(dfa, alphabet):
    row0 = "*\t\t"
    for char in alphabet:
        row0 += char + "\t\t"
    print(row0)
    for state in dfa:
        row = ""
        state_dict = dfa[state]
        row += str(state) + "\t\t"
        for char in alphabet:
            if char in state_dict:
                row += str(state_dict[char]) + "\t\t"
            else:
                row += "_\t\t"
        print(row)

def display_dict_epsilon(dfa, alphabet):
    row0 = "*\t\teps\t\t"
    for char in alphabet:
        row0 += char + "\t\t"
    print(row0)
    for state in dfa:
        row = ""
        state_dict = dfa[state]
        row += str(state) + "\t\t"
        if len(state_dict["eps"]) > 0:
            row += str(state_dict["eps"]) + "\t\t"
        else:
            row += "_\t\t"
        for char in alphabet:
            if len(state_dict[char]) > 0:
                row += str(state_dict[char]) + "\t\t"
            else:
                row += "_\t\t"
        print(row)

def display_dict_nfa(dfa, alphabet):
    row0 = "*\t\t"
    for char in alphabet:
        row0 += char + "\t\t"
    print(row0)
    for state in dfa:
        row = ""
        state_dict = dfa[state]
        row += str(state) + "\t\t"
        for char in alphabet:
            if len(state_dict[char]) > 0:
                row += str(state_dict[char]) + "\t\t"
            else:
                row += "_\t\t"
        print(row)

def fhoo(regex): # find highest order operation
    while len(regex) != 0 and regex[0] == "(" and regex[-1] == ")":
        regex = regex[1 : -1]
    elements = []
    cur_element = ""
    l_count = 0 # parentheses counters
    r_count = 0
    operations = ["*", "?", "+"]
    i = 0
    while i < len(regex):
        cur_element += regex[i]
        if regex[i] != "(" and regex[i] != ")" and regex[i] != "|":
            i += 1
            if i < len(regex) and regex[i] in operations:
                cur_element += regex[i]
                i += 1
        elif regex[i] == "(":
            l_count += 1
            i += 1
        elif regex[i] == ")":
            r_count += 1
            i += 1
            if i < len(regex) and regex[i] in operations:
                cur_element += regex[i]
                i += 1
        elif regex[i] == "|":
            if l_count == r_count:
                return ("|", [regex[ : i], regex[i + 1 : ]])
            else:
                i += 1
        else:
            print("Character not supported.")
        
        if l_count == r_count:
            elements.append(cur_element)
            cur_element = ""
    
    if len(elements) > 1:
        return ("s", elements)
    elif len(elements) == 1:
        if elements[0][-1] in operations:
            return (elements[0][-1], elements[0][ : -1])
        else:
            return ("done", )
    else:
        print("Empty")

def next(graph, alphabet): # returns the first non-reduced regex if there exists one, otherwise returns -1
    for key in graph:
        for i in range(0, len(graph[key])):
            tup = graph[key][i]
            if not(len(tup[1]) == 1 and tup[1] in alphabet or tup[1] == "eps"):
                return (key, i)
    return -1

def NFAepsilon(regex, alphabet):
    graph = {}
    final_nodes = set()
    graph[0] = [(1, regex)]
    graph[1] = []
    final_nodes.add(1)
    next_node = 2
    while(True):
        data = next(graph, alphabet)
        if data == -1:
            break
        else:
            key, index = data
            start = key
            end = graph[key][index][0]
            data2 = fhoo(graph[key][index][1])
            del graph[start][index]
            if data2[0] == "|":
                r1 = data2[1][0]
                r2 = data2[1][1]
                graph[start].append((end, r1))
                graph[start].append((end, r2))
            elif data2[0] == "s":
                r = data2[1]
                nodes = [start, ]
                while len(nodes) < len(r):
                    nodes.append(next_node)
                    next_node += 1
                nodes.append(end)
                for i in range(0, len(nodes) - 1):
                    if nodes[i] not in graph:
                        graph[nodes[i]] = []
                    graph[nodes[i]].append((nodes[i + 1], r[i]))
            elif data2[0] == "*":
                middle = next_node
                next_node += 1
                graph[start].append((middle, "eps"))
                graph[middle] = []
                graph[middle].append((middle, data2[1]))
                graph[middle].append((end, "eps"))
            elif data2[0] == "?":
                graph[start].append((end, "eps"))
                graph[start].append((end, data2[1]))
            elif data2[0] == "+":
                middle = next_node
                next_node += 1
                graph[start].append((middle, data2[1]))
                graph[middle] = []
                graph[middle].append((middle, data2[1]))
                graph[middle].append((end, "eps"))
            elif data2[0] == "done":
                print("Error, should not return 'done'.")
            else:
                print("Error, unhandled case.")
    nfa = {}
    for node in graph:
        nfa[node] = {}
        nfa[node]["eps"] = ()
        for char in alphabet:
            nfa[node][char] = ()
        for data in graph[node]:
            n, c = data
            nfa[node][c] = nfa[node][c] + (n, )
    
    return (nfa, final_nodes, alphabet)

def reachable(node, nfa, s): # returns the set of all nodes reachable by epsilon from node, MAY HAVE INFINITE RECURSION
    for n in nfa[node]["eps"]:
        s.add(n)
        for r in reachable(n, nfa, s):
            s.add(r)
    return s

def NFA(nfa):
    nfa, final_nodes, alphabet = nfa
    nfa2 = {}
    final_nodes2 = final_nodes.copy()
    for node in nfa:
        nfa2[node] = {}
        for char in alphabet:
            nfa2[node][char] = nfa[node][char]
    for node in nfa:
        for node2 in reachable(node, nfa, set()):
            # node inherits all properties of node2
            if node2 in final_nodes: # check for final node property
                final_nodes2.add(node)
            for char in alphabet:
                for node3 in nfa[node2][char]:
                    if node3 not in nfa2[node][char]:
                        nfa2[node][char] = nfa2[node][char] + (node3, )
    return (nfa2, final_nodes2, alphabet) 

def get_first_hybrid(nfa, alphabet):
    hybrid = -1
    for node in nfa:
        for char in alphabet:
            if len(nfa[node][char]) > 1:
                hybrid = frozenset(nfa[node][char])
                return hybrid
    return -1

def hybrid(nfa, alphabet, h):
    nodes = set()
    for node in nfa:
        for char in alphabet:
            if h.issubset(set(nfa[node][char])):
                nodes.add((node, char))
    return (nodes, h)
                
def reachable_with_char(char, s, nfa, final_nodes):
    output = set()
    final = False
    for node in s:
        if node in final_nodes:
            final = True
        output = output.union(set(nfa[node][char]))
    return (frozenset(output), final)

def copy(nfa, alphabet):
    nfa2 = {}
    for node in nfa:
        nfa2[node] = {}
        for char in alphabet:
            nfa2[node][char] = nfa[node][char]
    return nfa2

def make_hybrid(nfa, nfa_old, final_nodes, alphabet, set_of_nodes, hybrids_tracker):
    hybrid_node = len(nfa)
    hybrids_tracker[set_of_nodes] = hybrid_node
    # find all connections to exactly set_of_nodes and delete them
    for node in nfa:
        for char in alphabet:
            if char in nfa[node] and frozenset(nfa[node][char]) == set_of_nodes:
                nfa[node][char] = (hybrid_node, )

    nfa[hybrid_node] = {}
    
    # make a new hybrid if necessary
    for char in alphabet:
        r, final = reachable_with_char(char, set_of_nodes, nfa_old, final_nodes)
        if final:
            final_nodes.add(hybrid_node)
        if len(r) <= 1:
            nfa[hybrid_node][char] = tuple(r)
        else:
            if r in hybrids_tracker:
                nfa[hybrid_node][char] = (hybrids_tracker[r], )
            else:
                nfa[hybrid_node][char] = tuple(r)

    return hybrid_node

def DFA(nfa):
    nfa, final_nodes, alphabet = nfa
    nfa_old = copy(nfa, alphabet)
    hybrids_tracker = {}

    while True:
        s = get_first_hybrid(nfa, alphabet)
        if s == -1:
            return (nfa, final_nodes, alphabet)
        make_hybrid(nfa, nfa_old, final_nodes, alphabet, s, hybrids_tracker)

def reachable_from(node, dfa, nodes, alphabet):
    if node in nodes:
        return nodes
    nodes.add(node)
    for char in alphabet:
        if char in dfa[node]:
            for r in reachable_from(dfa[node][char], dfa, nodes, alphabet):
                nodes.add(r)
    return nodes

def duplicate_node(dfa, alphabet, final_nodes):
    for node in dfa:
        for node2 in dfa:
            flag = True
            if node != node2 and (node in final_nodes and node2 in final_nodes or node not in final_nodes and node2 not in final_nodes):
                for char in alphabet:
                    if char in dfa[node] and char in dfa[node2]:
                        if dfa[node][char] != dfa[node2][char]:
                            flag = False
                    elif not(char not in dfa[node] and char not in dfa[node2]):
                        flag = False
                if flag == True:
                    return (node, node2)
    return -1
    
def optimize(dfa):
    dfa, final_nodes, alphabet = dfa
    for node in dfa:
        for char in alphabet:
            if len(dfa[node][char]) == 0:
                del dfa[node][char]
            else:
                dfa[node][char] = dfa[node][char][0]
    span = reachable_from(0, dfa, set(), alphabet)
    delete = set()
    for node in dfa:
        if node not in span:
            delete.add((node, -1))
        else:
            for char in alphabet:
                if char in dfa[node]:
                    if dfa[node][char] not in span:
                        delete.add((node, char))
    for node, char in delete:
        if char == -1:
            if node in final_nodes:
                final_nodes.remove(node)
            del dfa[node]
        else:
            del dfa[node][char]

    while(True):
        pair = duplicate_node(dfa, alphabet, final_nodes)
        if pair == -1:
            return (dfa, final_nodes, alphabet)
        node, node2 = pair
        keep = min(node, node2)
        erase = max(node, node2)
        if erase in final_nodes:
            final_nodes.remove(erase)
        del dfa[erase]
        for node in dfa:
            for char in alphabet:
                if char in dfa[node]:
                    if dfa[node][char] == erase:
                        dfa[node][char] = keep

def emulate(dfa, final_states, puzzle):
    state = 0
    for char in puzzle:
        if char in dfa[state]:
            state = dfa[state][char]
        else:
            return False
    if state in final_states:
        return True
    return False

alphabet = sys.argv[1]
regex = sys.argv[2]
puzzles = open(sys.argv[3], "r").read().split("\n")
nfa_epsilon = NFAepsilon(regex, alphabet)
# display_dict_epsilon(nfa_epsilon[0], nfa_epsilon[2])
# print("Final nodes: " + str(nfa_epsilon[1]))
# print()
nfa = NFA(nfa_epsilon)
# display_dict_nfa(nfa[0], nfa[2])
# print("Final nodes: " + str(nfa[1]))
# print()
dfa = DFA(nfa)
# display_dict_nfa(dfa[0], dfa[2])
# print("Final nodes: " + str(dfa[1]))
# print()
dfa = optimize(dfa)
display_dict(dfa[0], dfa[2])
print("Final nodes: " + str(dfa[1]))
num_of_spaces = {
    True : 2,
    False : 1
}
for puzzle in puzzles:
    result = emulate(dfa[0], dfa[1], puzzle)
    print(str(result) + " " * num_of_spaces[result] + puzzle)