from typing import Dict, List
# main.py
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  : Audrey DAMIBA, Melissa LACHEB, Timéo GOGOLACHVILI , Thomas MASSELLES, Zoé LE MAIGUET
# Creation Date: 2024-03-29
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

def has_negative_edges(graph):
    
        '''has_negative_edges function takes as a parameter a graph and returns True if the graph contains negative edges, False otherwise'''
    
        for vertex, data in graph.items():
            for predecessor in data['predecessors']:
                if graph[predecessor]['duration'] < 0:
                    print("The graph contains negative edges.")
                    return True

        print("The graph does not contain negative edges.")
        return False

def display_graph_edges(graph):

    '''display_graph_edges function takes as a parameter a graph and displays the edges of the graph'''

    for node, data in graph.items():
        for predecessor in data['predecessors']:
            duration = graph[predecessor]['duration']
            print(f"{predecessor} -> {node} = {duration}")

def add_fictitious_vertices(graph):
    '''add_fictitious_vertices function takes as a parameter a graph and adds two fictitious vertices: one at the beginning and one at the end of the graph'''
    # Add the fictitious vertex at the beginning of the graph
    graph[0] = {'predecessors': [], 'duration': 0}
    
    # Find all vertices that don't have predecessors and add vertex 0 as their predecessor
    for vertex, data in graph.items():
        if not data['predecessors'] and vertex != 0:
            data['predecessors'].append(0)
    
    # Find all vertices that don't have successors and are not the vertex 0
    vertices_without_successors = [vertex for vertex in graph if vertex != 0 and not any(vertex in graph[v]['predecessors'] for v in graph)]
    n = len(graph)-1
    # Add the fictitious vertex at the end of the graph
    graph[n+1] = {'predecessors': vertices_without_successors, 'duration': 0}
    
    return graph

def display_graph(graph):
    '''display_graph function takes as a parameter a graph and displays the graph'''
    add_fictitious_vertices(graph)
    display_graph_edges(graph)
    display_graph_matrix(graph)

def display_graph_matrix(graph):
    '''display_graph_matrix function takes as a parameter a graph and displays the matrix of the graph'''

    num_vertices = len(graph)

    matrix = [['*' for _ in range(num_vertices)] for _ in range(num_vertices)]
    
    for vertex, data in graph.items():
        for predecessor in data['predecessors']:
            duration = graph[predecessor]['duration']
            matrix[predecessor][vertex] = f"{duration}"


    print("\nValue Matrix")
    print("   ", end="")
    for i in range(num_vertices):
        print(f" {i:<2}", end="")
    print()
    for i, row in enumerate(matrix, start=0):
        print(f"{i:<2} ", end="")
        for val in row:
            if val == '*':
                print('\033[31m' + f" {val:<2}" + '\033[0m', end="")
            else:
                print(f" {val:<2}", end="")
        print()

def zero_edges(graph):
    '''zero_edges function takes as a parameter a graph and returns True if the graph contains zero edges, False otherwise'''
    for vertex, data in graph.items():
        if not data['predecessors']:
            print(f"The edge {vertex} has a weight of 0")

    print("The graph does not contain zero edges.")
    return False

def has_cycle(graph):

    '''has_cycle function takes as a parameter a graph and using depth-first search it returns True if the graph contains a cycle, False otherwise'''

    visited = {vertex: False for vertex in graph}
    stack = {vertex: False for vertex in graph}
    
    def depth_first_search(vertex):
        visited[vertex] = True
        stack[vertex] = True
        
        entry_points = [neighbor for neighbor in graph[vertex]['predecessors'] if not visited[neighbor]]
        if not entry_points:
            print(f"Entry points for vertex {vertex}")
        remaining_vertices = [v for v in graph if not visited[v] and v not in entry_points]
        print(f"Eliminating entry points")
        print(f"Remaining vertices: {' '.join(map(str, remaining_vertices)) if remaining_vertices else 'None'}")
        
        for neighbor in graph[vertex]['predecessors']:
            if not visited[neighbor]:
                if depth_first_search(neighbor):
                    return True
            elif stack[neighbor]:
                return True
        
        stack[vertex] = False
        return False
    
    for vertex in graph:
        if not visited[vertex]:
            if depth_first_search(vertex):
                return True

    return False

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


def compute_ranks(graph):

    '''compute_ranks function takes as a parameter a graph and returns a dictionary of ranks for each vertex'''

    ranks = {vertex: -1 for vertex in graph}
    predecessors = {vertex: [] for vertex in graph}
    for vertex, data in graph.items():
        for predecessor in data['predecessors']:
            predecessors[vertex].append(predecessor)

    def calculate_rank(vertex):
        if ranks[vertex] != -1:
            return ranks[vertex]
        
        if not predecessors[vertex]:
            ranks[vertex] = 0
            return 0

        max_rank = max(calculate_rank(predecessor) for predecessor in predecessors[vertex])
        
        ranks[vertex] = max_rank + 1

        return ranks[vertex]

    for vertex in graph:
        calculate_rank(vertex)

    return ranks

def main():
    graph = read_constraint_table("6.txt")
    print("\n❀ The graph is:")
    display_graph(graph)
    display_graph_edges(graph)
    if  not has_cycle(graph):
        print("\n The rank of the vertices is: {}".format(compute_ranks(graph)))
        print("\n The earliest date calendar is: {}".format(compute_earliest_date_calendar(graph)))
        print("\n The latest date calendar is: {}".format(compute_latest_date_calendar(graph)))
        print("\n The floats are: {}".format(compute_floats(graph)))
        print("\n The critical paths are: {}".format(compute_critical_paths(graph)))


def compute_earliest_date_calendar(graph):
    '''compute_earliest_date function takes as a parameter a graph and returns a dictionary of earliest date for each vertex'''
    earliest_date = {vertex: 0 for vertex in graph}  # Initialize earliest_date dictionary
    successors = get_successors(graph)  # Get successors for each vertex

    def visit(vertex):
        for successor in successors[vertex]:
            earliest_date[successor] = max(earliest_date[successor], earliest_date[vertex] + graph[vertex]['duration'])

    visit(0) 
    for vertex in graph:
        if vertex != 0:  
            visit(vertex)

    return earliest_date


def compute_latest_date_calendar(graph):
    '''compute_latest_date_calendar function takes as a parameter a graph and returns a dictionary of latest date for each vertex'''
    rank = compute_ranks(graph)  
    earliest_date_calendar = compute_earliest_date_calendar(graph)
    max_earliest_date = max(earliest_date_calendar.values())
    latest_date = {vertex: max_earliest_date for vertex in graph}
    successors = get_successors(graph)

    for vertex in reversed(list(graph)):
        if successors[vertex]:  # If the vertex has successors
            latest_date[vertex] = min(latest_date[s] for s in successors[vertex]) - graph[vertex]['duration']
            latest_date[0] = 0
    
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
    ranks = compute_ranks(graph)
    critical_paths = []
    visited = {vertex: False for vertex in graph}
    successors = get_successors(graph)
    ordered_vertices = sorted(graph, key=lambda vertex: ranks[vertex])  # Order the vertices by their ranks
    ordered_graph = {vertex: graph[vertex] for vertex in ordered_vertices}


    def visit(vertex, path, duration, max_duration, critical_paths):
        if not visited[vertex]:
            visited[vertex] = True
            path.append(vertex)
            duration += graph[vertex]['duration']
            if not successors[vertex]:
                if path[0] == 0:
                    if duration > max_duration[0]:
                        critical_paths.clear()
                        critical_paths.append(path.copy())
                        max_duration[0] = duration
                    elif duration == max_duration[0]:
                        critical_paths.append(path.copy())
            else:
                for successor in successors[vertex]:
                    if floats[successor] == 0:
                        visit(successor, path.copy(), duration, max_duration, critical_paths)
            path.pop()
            visited[vertex] = False
        return max_duration, critical_paths

    max_duration = [0]
    for vertex in ordered_graph:  # Visit the vertices in the order of their ranks
        max_duration, critical_paths = visit(vertex, [], 0, max_duration, critical_paths)

    return critical_paths
'''
def main():
    while True:
        print("\n\033[0;35m•───────•°•❀•°•───────  Welcome to the project of the course SM601I - Graph Theory (L3-INT - 2324S6)  ───────•°•❀•°•───────•")
        print("\n❀ Operations available:")
        print("1. Test a constraint table")
        print("2. Exit")

        choice = input("\n\033[0m❀ Choose an operation (1-2): ")
     

        if choice == '1':
            file_name = input("❀ Enter the name of the constraint table file: ")
            if not file_name or not file_name.endswith('.txt'):
                print("Please enter a valid file name.")
                continue
            graph = read_constraint_table(file_name)
            print("\n❀ The graph is:")
            display_graph(graph)
            print("\n ❀ The number of vertices is: {}".format(count_vertices(graph)))
            print("\n❀ The number of edges is: {}".format(count_edges(graph)))
            if zero_edges(graph):
                print("\n❀ The graph contains zero edges.")
            if is_scheduling_graph(graph):
                print("\n❀ The graph is a scheduling graph.")
                print("\n❀ The ranks of the vertices are: {}".format(compute_ranks(graph)))  
                if not all(vertex['duration'] != 0 for vertex in graph.values()):
                    print("\n❀ Earliest date calendar: {}".format(compute_earliest_date_calendar(graph)))
                    print("\n❀ Latest date calendar: {}".format(compute_latest_date_calendar(graph)))
                    print("\n❀ Floats: {}".format(compute_floats(graph)))
                    print("\n❀ Critical paths: {}".format(compute_critical_paths(graph)))
            else:
                print("\nThe graph is not a scheduling graph.")

        elif choice == '2':
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 2.")
'''
if __name__ == "__main__":
    main()