# main.py
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  : Audrey DAMIBA, Melissa LACHEB
# Created Date: 2024-03-29
# ---------------------------------------------------------------------------

""" This  as for objective to do somes operations to automata 
    Operations availables are:
        -Reading a constraint table
        -build a graph from the constraint table
        -compute the earliest date calendar
        -compute the latest date calendar
        -compute the floats 
        -compute 

    The module is composed of 3 classes:
       
    The module is also composed of one global constants:
        
    This project is a part of the course SM601I - Graph Theory (L3-INT - 2324S6)
        
        """

def read_constraint_table(file_name):

    '''read_constraint_table function takes as a parameter a .txt file and store a constraint table in memory '''

    constraint_table = {}

    with open(file_name, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split()
                vertex_number = int(parts[0])
                duration = int(parts[1])
                predecessors = [int(p) for p in parts[2:]]
                constraint_table[vertex_number] = {'duration': duration, 'predecessors': predecessors}
    return constraint_table

def get_successors(graph):
    successors = {vertex: [] for vertex in graph}

    for vertex, data in graph.items():
        predecessors = data['predecessors']
        for predecessor in predecessors:
            successors[predecessor].append(vertex)

    return successors


'''def has_cycle(graph):
    removed_vertices = []

    while True:
        # Find source vertices (vertices with no predecessors)
        source_vertices = [vertex for vertex, neighbors in graph.items() if not neighbors]

        # If there are no source vertices, exit the loop
        if not source_vertices:
            break

        # Remove source vertices and their outgoing edges from the graph
        for vertex in source_vertices:
            removed_vertices.append(vertex)
        
        # Update the graph to remove the source vertices and their outgoing edges
        graph = {vertex: predecessor - removed_vertices for vertex, neighbors in graph.items() if vertex not in removed_vertices}

    # If there are still remaining vertices in the graph, it has a cycle
    return bool(graph)'''


'''def compute_ranks(constraints):
    ranks = {}  # Dictionary to store ranks of vertices
    topological_order = []  # List to store the topological order of vertices

    # Find source vertex
    source_vertex = None
    for vertex in constraints:
        if not constraints[vertex]:  # If the vertex has no predecessors
            source_vertex = vertex
            break

    if source_vertex is None:
        print("Graph contains cycles")

    # Assign rank 0 to the source vertex
    ranks[source_vertex] = 0
    topological_order.append(source_vertex)

    # Compute ranks for other vertices
    for vertex in constraints:
        if vertex != source_vertex:
            ranks[vertex] = compute_rank(vertex, constraints, ranks)

    # Perform topological sort based on ranks
    sorted_vertices = sorted(ranks.keys(), key=lambda x: ranks[x])

    return ranks, sorted_vertices

def compute_rank(vertex, constraints, ranks):
    # Compute rank recursively for predecessors
    max_predecessor_rank = 0
    for predecessor in constraints[vertex]:
        predecessor_rank = ranks[predecessor]
        max_predecessor_rank = max(max_predecessor_rank, predecessor_rank)

    # Set rank for current vertex
    rank = max_predecessor_rank + 1
    return rank

'''


def main():
    file_name = 'CO1.txt'
    graph1 = read_constraint_table(file_name)
    graph2 =read_constraint_table('CO2.txt')
    graph3 = read_constraint_table('CO3.txt')
    graph4 = read_constraint_table ('CO4.txt')
    print("Constraints:")
    print(get_successors(graph2))


    for vertex_number, data in graph3.items():
        print(f"Vertex {vertex_number}: Duration {data['duration']}, Predecessors {data['predecessors']}") 
    '''print(compute_ranks(constraints))

    ranks = compute_ranks(constraints)
    for vertex, rank in ranks.items():
        print(f"Vertex {vertex}: Rank {rank}")
    ranks, topological_order = compute_ranks(constraints)
    for vertex, rank in ranks.items():
        print(f"Vertex {vertex}: Rank {rank}")
    print("Topological order:", topological_order)'''



if __name__ == "__main__":
    main()


