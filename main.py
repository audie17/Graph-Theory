from typing import Dict, List
# main.py
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  : Audrey DAMIBA, Melissa LACHEB, Timéo GOGOLACHVILI , Thomas MASSELLES, Zoé LE MAIGUET
# Created Date: 2024-03-29
# ---------------------------------------------------------------------------

""" This program will perform this perform on graphs representing constraint tables
    Operations availables are:

        -Read a constraint table
        -Display a graph from the constraint table as matrix
        -build a graph from the constraint table
        -compute the earliest date calendar
        -compute the latest date calendar
        -compute the floats
        -compute the critical path

        
    This project is a part of the course SM601I - Graph Theory (L3-INT - 2324S6)
        
        """

def read_constraint_table(file_name):

    '''read_constraint_table function takes as a parameter a .txt file and returns a graph representing the constraint table'''
    graph = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split()
                vertex_number = parts[0]
                duration = parts[1]
                predecessors = [int(p) for p in parts[2:]]
                graph[int(vertex_number)] = {'duration': int(duration), 'predecessors': predecessors}

    return graph

def get_successors(graph):

    '''get_successors function takes as a parameter a graph and returns a dictionary of successors for each vertex'''

    successors = {vertex: [] for vertex in graph}

    for vertex, data in graph.items():
        predecessors = data['predecessors']
        for predecessor in predecessors:
            successors[predecessor].append(vertex)

    return successors

def has_cycle(graph):

    '''has_cycle function takes as a parameter a graph and returns True if the graph contains a cycle, False otherwise'''

    visited = {vertex: False for vertex in graph}
    stack = {vertex: False for vertex in graph}

    def has_cycle_from_vertex(vertex):
        if not visited[vertex]:
            visited[vertex] = True
            stack[vertex] = True

            for successor in get_successors(graph)[vertex]:
                if not visited[successor] and has_cycle_from_vertex(successor):
                    return True
                elif stack[successor]:
                    return True

        stack[vertex] = False
        return False

    for vertex in graph:
        if has_cycle_from_vertex(vertex):
            return True

    return False

def has_negative_edges(graph):
    
        '''has_negative_edges function takes as a parameter a graph and returns True if the graph contains negative edges, False otherwise'''
    
        for vertex, data in graph.items():
            for predecessor in data['predecessors']:
                if graph[predecessor]['duration'] < 0:
                    return True
    
        return False

def display_graph_edges(graph):

    '''display_graph_edges function takes as a parameter a graph and displays the edges of the graph'''

    #add_fictitious_vertices(graph)
    for node, data in graph.items():
        for predecessor in data['predecessors']:
            duration = graph[predecessor]['duration']
            print(f"{predecessor} -> {node} = {duration}")

def add_fictitious_vertices(graph):
    #if any vertices has no predecessors, we add a fictitious vertex 0 with a duration of 0
    #if any vertices has no successors, we add a fictitious vertex n+1 with a duration of 0
    vertices = list(graph.keys())
    n = len(vertices)

    # Add fictitious vertex 0 if any vertex has no predecessors
    for vertex in vertices:
        if all(vertex not in graph[v]['predecessors'] for v in vertices):
            if 0 not in graph:
                graph[0] = {'predecessors': [], 'duration': 0}
            graph[vertex]['predecessors'].append(0)

    # Add fictitious vertex n+1 if any vertex has no successors
    for vertex in vertices:
        if not any(vertex in graph[v]['predecessors'] for v in vertices):
            if n+1 not in graph:
                graph[n+1] = {'predecessors': [], 'duration': 0}
            if 'successors' not in graph[vertex]:
                graph[vertex]['successors'] = []
            graph[vertex]['successors'].append(n+1)

    return graph

def display_graph_matrix(graph):
    num_vertices = len(graph)
    
    # Create an empty matrix with dimensions (num_vertices + 1) x (num_vertices + 1)
    matrix = [['*' for _ in range(num_vertices)] for _ in range(num_vertices)]
    
    # Fill in the matrix based on the edges and durations in the graph
    for vertex, data in graph.items():
        for predecessor in data['predecessors']:
            matrix[predecessor - 1][vertex - 1] = f"{data['duration']}"

    # Display the matrix with headers
    print("Value Matrix")
    print("   ", end="")
    for i in range(1, num_vertices + 1):
        print(f" {i} ", end="")
    print()
    for i, row in enumerate(matrix, start=1):
        print(f"{i}  ", end="")
        for val in row:
            print(f" {val} ", end="")
        print()

def is_scheduling_graph(graph):
    
    '''is_scheduling_graph function takes as a parameter a graph and returns True if the graph is a scheduling graph, False otherwise'''
    
    if has_cycle(graph):
        return False
    
    if has_negative_edges(graph):
        return False
    
    return True

def count_edges(graph):
    
        '''count_edges function takes as a parameter a graph and returns the number of edges in the graph'''
    
        return sum(len(data['predecessors']) for data in graph.values())

def count_vertices(graph):
    
        '''count_vertices function takes as a parameter a graph and returns the number of vertices in the graph'''
    
        return len(graph)

def return_verteces_rank(graph):
    '''return_verteces_rank function takes as a parameter a graph and returns a dictionary of rank for each vertex'''
    rank = {vertex: 0 for vertex in graph}
    successors = get_successors(graph)
    visited = {vertex: False for vertex in graph}

    def visit(vertex):
        if not visited[vertex]:
            visited[vertex] = True
            for successor in successors[vertex]:
                visit(successor)
            rank[vertex] = max([rank[s] for s in successors[vertex]], default=0) + 1

    for vertex in graph:
        visit(vertex)

    return rank

def compute_earliest_date_calendar(graph):
    '''compute_earliest_date_calendar function takes as a parameter a graph and returns a dictionary of earliest date for each vertex'''
    rank = return_verteces_rank(graph)
    earliest_date = {vertex: 0 for vertex in graph}
    successors = get_successors(graph)

    for vertex in graph:
        earliest_date[vertex] = max([earliest_date[p] + graph[p]['duration'] for p in graph[vertex]['predecessors']], default=0)

    return earliest_date

def compute_latest_date_calendar(graph):
    '''compute_latest_date_calendar function takes as a parameter a graph and returns a dictionary of latest date for each vertex'''
    rank = return_verteces_rank(graph)
    earliest_date_calendar = compute_earliest_date_calendar(graph)
    latest_date = {vertex: max([earliest_date_calendar[vertex] for vertex in graph]) for vertex in graph}
    successors = get_successors(graph)

    for vertex in reversed(list(graph)):
        latest_date[vertex] = min([latest_date[s] - graph[vertex]['duration'] for s in successors[vertex]], default=latest_date[vertex])

    return latest_date

def compute_floats(graph):  

    '''compute_floats function takes as a parameter a graph and returns a dictionary of floats for each vertex'''

    earliest_date_calendar = compute_earliest_date_calendar(graph)
    latest_date_calendar = compute_latest_date_calendar(graph)
    floats = {vertex: latest_date_calendar[vertex] - earliest_date_calendar[vertex] for vertex in graph}
    return floats

def compute_critical_paths(graph):
    '''compute_critical_paths function takes as a parameter a graph and returns a list of critical paths'''
    floats = compute_floats(graph)
    critical_paths = []
    visited = {vertex: False for vertex in graph}
    successors = get_successors(graph)

    def visit(vertex, path):
        if not visited[vertex]:
            visited[vertex] = True
            path.append(vertex)
            if not successors[vertex]:
                critical_paths.append(path.copy())
            for successor in successors[vertex]:
                if floats[successor] == 0:
                    visit(successor, path)
            path.pop()

    for vertex in graph:
        visit(vertex, [])

    return critical_paths

'''def main():
    while True:
        print("\n•───────•°•❀•°•───────  Welcome to the project of the course SM601I - Graph Theory (L3-INT - 2324S6)  ───────•°•❀•°•───────•")
        print("1. Test a constraint table")
        print("2. Exit")

        choice = input("\n❀ Choose an operation (1-2): ")

        if choice == '1':
            file_name = input("❀ Enter the name of the constraint table file: ")
            graph = read_constraint_table(file_name)
            display_graph_edges(graph)
            #display_graph_matrix(graph)
            print("\n ❀ The number of vertices is: {}".format(count_vertices(graph)))
            print("❀ The number of edges is: {}".format(count_edges(graph)))
            if is_scheduling_graph(graph):
                print("\n❀ The graph is a scheduling graph.")
                print("\n❀ The ranks of the vertices are: {}".format(return_verteces_rank(graph)))
                print("\n❀ Earliest date calendar: {}".format(compute_earliest_date_calendar(graph)))
                print("\n❀ Latest date calendar: {}".format(compute_latest_date_calendar(graph)))
                #print("❀ Floats: {}".format(compute_floats(graph)))
                #print("❀ Critical paths: {}".format(compute_critical_paths(graph)))
            else:
                print("\nThe graph is not a scheduling graph.")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 2.")'''

def main():
    graph5 = read_constraint_table("CO5.txt")
    #print(add_fictitious_vertices(graph7))
    display_graph_edges(graph5)
    display_graph_matrix(graph5)

if __name__ == "__main__":
    main()