from typing import Dict, List
# main.py
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  : Audrey DAMIBA, Melissa LACHEB, Timéo GOGOLACHVILI , Thomas MASSELLES, Zoé LE MAIGUET
# Created Date: 2024-03-29
# ---------------------------------------------------------------------------

""" This  as for objective to do somes operations to automata 
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


def main():
    file_name = 'CO1.txt'
    graph1 = read_constraint_table(file_name)
    graph2 = read_constraint_table('CO2.txt')
    graph3 = read_constraint_table('CO3.txt')
    graph4 = read_constraint_table('CO4.txt')
    graph5 = read_constraint_table('CO5.txt')
    graph6 = read_constraint_table('CO6.txt')
    graph7 = read_constraint_table('CO7.txt')
    print(add_fictitious_tasks(graph7))
    display_graph_edges(graph7)        
    
if __name__ == "__main__":
    main()


