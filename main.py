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
    
    add_fictitious_tasks(graph)
    for node, data in graph.items():
        for predecessor in data['predecessors']:
            duration = graph[predecessor]['duration']
            print(f"{predecessor} -> {node} = {duration}")

def add_fictitious_tasks(graph):
    num_vertices = len(graph)
    new_graph = {}
    new_graph[0] = {'duration': 0, 'predecessors': []}
    predecessors_n = [v for v in graph if not graph[v]['predecessors']]  
    if predecessors_n:  
        last_vertex = max(predecessors_n)  
    else:
        last_vertex = max(graph)  
    new_graph[num_vertices + 1] = {'duration': 0, 'predecessors': [last_vertex]}
    for vertex, data in graph.items():
        new_graph[vertex] = {'duration': data['duration'], 'predecessors': data['predecessors']}

    return new_graph

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


'''def main():
    "⊹₊┈ㆍ┈ㆍ┈ㆍ✿ㆍ┈ㆍ┈ㆍ┈₊⊹"
    
    
if __name__ == "__main__":
    main()'''

def main():
    while True:
        print("\n•───────•°•❀•°•───────  Welcome to the project of the course SM601I - Graph Theory (L3-INT - 2324S6)  ───────•°•❀•°•───────•")
        print("1. Test a constraint table")
        print("2. Exit")

        choice = input("\nChoose an operation (1-2): ")

        if choice == '1':
            file_name = input("Enter the name of the constraint table file: ")
            graph = read_constraint_table(file_name)
            display_graph_edges(graph)
            #display_graph_matrix(graph)
            print("\nThe number of vertices is: {}".format(count_vertices(graph)))
            print("The number of edges is: {}".format(count_edges(graph)))
            if is_scheduling_graph(graph):
                print("\nThe graph is a scheduling graph.")
                print("\nThe ranks of the vertices are: {}".format(return_verteces_rank(graph)))
                print("\nEarliest date calendar: {}".format(compute_earliest_date_calendar(graph)))
                print("\nLatest date calendar: {}".format(compute_latest_date_calendar(graph)))
                #print("Floats: {}".format(compute_floats(graph)))
                #print("Critical paths: {}".format(compute_critical_paths(graph)))
            else:
                print("\nThe graph is not a scheduling graph.")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 2.")

if __name__ == "__main__":
    main()