import pygtk, gtk
pygtk.require('2.0')
import sys
import math
import copy
import string

from graph import *
from node import *
import config as cfg
from heapq import heappush, heappop


class Graph_Area(gtk.DrawingArea):
    
    
    __gsignals__ = { "expose_event": "override" }
    
    graph = Graph()
    node_count = 0
    src_node  = None
    dest_node = None
    src_edge  = None
    
    
    def graph_paint(self):
        
        
        colors = range(0, len(self.graph.nodes))
        node_colors = [-1] * len(self.graph.nodes)
        
        for i in range(0, len(self.graph.weight_matrix)):

            color = list(colors)
            
            for j in range(0, len(self.graph.weight_matrix[i])):
                if self.graph.weight_matrix[i][j] != "X":
                    if node_colors[j] != -1:
                        if node_colors[j] in color:
                            color.remove(node_colors[j])
            node_colors[i] = color[0]
        
        print node_colors
            
    
    def dijkstra(self, src, graph):
        
        class Node(object):
            def __init__(self, i, d):
                self.i = i
                self.d = d
            def __cmp__(self, obj): return cmp(self.d, obj.d)
    
        n = len(graph)
        dist = [-1] * n
        heap = []
        heappush(heap, Node(src, 0))
        
        while not len(heap) == 0:
            
            node = heappop(heap)
            if dist[node.i] >= 0: continue
            dist[node.i] = node.d
            
            for i in range(n):
                if i == node.i: continue
                if graph[node.i][i] >= 0:
                    heappush(heap, Node(i, node.d + graph[node.i][i]))
        
        return dist
    
    
    def shortest_path(self, shortest_from, shortest_to):
            
        graph = copy.deepcopy(self.graph.weight_matrix)
        
        
        if 0 <= (shortest_from and shortest_to) < len(graph):
            
            for i in range(0,len(graph)):
                for j in range(0, len(graph[i])):
                    if graph[i][j] == "X":
                        graph[i][j] = -1
            
            dist = self.dijkstra(shortest_from, graph)
            
            if dist[shortest_to] == -1:
                print "end of eternity"
            else:
                print dist[shortest_to]
                
        else:
            print "Over limit for node counts.."
        
    
    def read_isomorph_from_file(self, filename, first_weight_matrix, second_weight_matrix):
                
        isomorph_file = open (filename , 'r')
        graph_list = [ map(str,line.split(' ')) for line in isomorph_file ]
        
        first_number_of_nodes = int(graph_list[0][0])
        second_number_of_nodes = int(graph_list[first_number_of_nodes+1][0])
        
        for i in range(1, first_number_of_nodes+1):
            
            first_weight_matrix.append([0] * first_number_of_nodes)
            
            for k in range(0, first_number_of_nodes):
                if graph_list[i][k] != 0:
                    first_weight_matrix[i-1][k] = int(graph_list[i][k])
                    
        for j in range(i+2, i+second_number_of_nodes+2):
            
            second_weight_matrix.append([0] * second_number_of_nodes)
            
            for k in range(0, second_number_of_nodes):
                if graph_list[j][k] != 0:
                    second_weight_matrix[j-i-2][k] = int(graph_list[j][k])
        
        isomorph_file.close()
        
        
    def are_isomorphic(self, filename):
                
        first_weight_matrix = []
        second_weight_matrix = []
        
        self.read_isomorph_from_file(filename, first_weight_matrix, second_weight_matrix)
        
        if len(first_weight_matrix) != len(second_weight_matrix) or len(first_weight_matrix[0]) != len(second_weight_matrix[0]):
            print "\nNumber of nodes is different. They aren't isomorph."
            return
        
        print "\nNumber of nodes  checking... Successful!.."
        
        
        first_matrix_edge_count = 0
        second_matrix_edge_count = 0
            
        first_matrix_node_count  = [0] * len(first_weight_matrix)
        second_matrix_node_count = [0] * len(second_weight_matrix)
        
        for i in range(0, len(first_weight_matrix)):
            
            for j in range(0, len(first_weight_matrix[i])):
                
                if first_weight_matrix[i][j] != 0:
                    first_matrix_edge_count  += 1
                    first_matrix_node_count[i] += 1
                    
                if second_weight_matrix[i][j] != 0:
                    second_matrix_edge_count += 1
                    second_matrix_node_count[i] += 1
                    
        if first_matrix_edge_count != second_matrix_edge_count:
            print "\nNumber of edges is different. They aren't isomorph."
            return
        
        print "\nNumber of edges checking... Successful!."
        
            
        degree_of_nodes_first  = [0] * first_matrix_edge_count
        degree_of_nodes_second = [0] * second_matrix_edge_count
        
        for i in range(0, len(first_matrix_node_count)):
            degree_of_nodes_first[first_matrix_node_count[i]] += 1
            degree_of_nodes_second[second_matrix_node_count[i]] += 1
            
        for i in range(0, len(first_matrix_node_count)):
            if degree_of_nodes_first[i] != degree_of_nodes_second[i]:
                print "\nDegrees of nodes are different. They aren't isomorph." 
                return
        
        print "\nDegrees of nodes checking... Successful!.."
        
            
        for i in range(0, len(first_weight_matrix)):
            if first_weight_matrix[i] != second_weight_matrix[i]:
                print "\nNodes matrix is different. They aren't isomorph."
                return
        
        print "\nNodes matrix checking... Successful!.."
            
        print "\nGraphs are isomorph."
    
    
    def is_a_planar(self):
        
        print "planar"
        
        
    def is_a_bipartite(self):
        
        cycles = self.list_cycles(len(self.graph.nodes))
        
        for cycle in cycles:
            print len(cycle), cycle
            if len(cycle) % 2 == 1:
                print "Graph isn't bipartite."
                return
        
        print "Graph is bipartite."
    
    
    def tour_graph(self, start, visited, all_node_id, weight_matrix):
        
        visited.append(all_node_id[start]-1)
        
        for i in range(0, len(weight_matrix[start])):
            if weight_matrix[start][i] != "X"  and   i not in visited:
                self.tour_graph(i, visited, all_node_id, weight_matrix)
    
    
    def is_a_tree(self):
        
        all_node_id = []
        visited = []
        
        for node in self.graph.nodes:
            all_node_id.append(node.node_id)
            
        self.tour_graph(0, visited, all_node_id, self.graph.weight_matrix)
        cycles = self.list_cycles(len(self.graph.nodes))
        
        
        for i in range(0, len(self.graph.weight_matrix)):
            if self.graph.weight_matrix[i][i] != "X": 
                print "\nGraph isn't a tree."
                return
        
        if len(visited) != len(all_node_id) or len(cycles) > 0:
            print "\nGraph isn't a tree."
            return
        else:
            print "\nGraph is a tree."
       
        
    def hamilton_cycle(self, weight_matrix, prev, row, first_node, n, size, list_of_nodes, all_node_id, all_hamilton_cycles):
        
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if j+1 not in list_of_nodes:
                
                    size += 1
                    list_of_nodes.append(j+1)
                    all_node_id.remove(j+1)
                    
                    if size == n:
                        size -= 1
                        if len(all_node_id) == 0 and j == first_node:
                            all_hamilton_cycles.append(list(list_of_nodes))
                            
                        list_of_nodes.pop()
                        all_node_id.append(j+1)
                    else:
                        self.hamilton_cycle(weight_matrix, row, j, first_node, n, size, list(list_of_nodes), list(all_node_id), all_hamilton_cycles)        
                       
                        list_of_nodes.pop()
                        all_node_id.append(j+1)
                        size -= 1    
                        
    
    def hamilton_cycles(self):
        
        all_hamilton_cycles = []
        list_of_nodes = []
        all_node_id = []
        
        for node in self.graph.nodes:
            all_node_id.append(node.node_id)
        
        for j in range(0, len(self.graph.weight_matrix)):
            
            self.hamilton_cycle(self.graph.weight_matrix, None, j, j, len(all_node_id), 0, list(list_of_nodes), list(all_node_id), all_hamilton_cycles)  
        
        return  all_hamilton_cycles
    
    
    def print_hamilton_cycles(self):
    
        print "\nHamilton Cycles:"
        print "------------\n"
        
        all_hamilton_cycles = self.hamilton_cycles()
        
        for hamilton_cycle in all_hamilton_cycles:
            print hamilton_cycle
                   

    def hamilton_path(self, weight_matrix, prev, row, n, size, list_of_nodes, all_node_id, all_hamilton_paths):
        
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if j+1 not in list_of_nodes:
                
                    size += 1
                    list_of_nodes.append(j+1)
                    all_node_id.remove(j+1)
                    
                    if size == n:
                        size -= 1
                        if len(all_node_id) == 0:
                            all_hamilton_paths.append(list(list_of_nodes))
                            
                        list_of_nodes.pop()
                        all_node_id.append(j+1)
                    else:
                        self.hamilton_path(weight_matrix, row, j, n, size, list(list_of_nodes), list(all_node_id), all_hamilton_paths)        
                       
                        list_of_nodes.pop()
                        all_node_id.append(j+1)
                        size -= 1    
                        
    
    def hamilton_paths(self):
        
        all_hamilton_paths = []
        list_of_nodes = []
        all_node_id = []
        
        for node in self.graph.nodes:
            all_node_id.append(node.node_id)
        
        for j in range(0, len(self.graph.weight_matrix)):
            all_node_id.remove(j+1)
            list_of_nodes.append(j+1)

            self.hamilton_path(self.graph.weight_matrix, None, j, len(all_node_id), 0, list(list_of_nodes), list(all_node_id), all_hamilton_paths)  
            
            all_node_id.append(j+1) 
            list_of_nodes.remove(j+1)
            
        return all_hamilton_paths
    
    
    def print_hamilton_paths(self):
             
        print "\nHamilton Paths:"
        print "------------\n"
        
        all_hamilton_paths = self.hamilton_paths()
        
        for hamilton_path in all_hamilton_paths:
            print hamilton_path 
    
    
    def euler_cycle(self, weight_matrix, prev, row, first_node, n, size, list_of_row, edges, all_euler_cycles):
        
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if [row+1, j+1] not in list_of_row and [j+1, row+1] not in list_of_row:
                
                    size += 1
                    list_of_row.append([row+1, j+1])

                    edges.remove([row, j])
                    edges.remove([j, row])
                    
                    if size == n:
                        size -= 1
                        if len(edges) == 0 and j == first_node:
                            all_euler_cycles.append(list(list_of_row))
                        list_of_row.pop()
                        edges.append([row, j])
                        edges.append([j, row])
                    else:
                        self.euler_cycle(weight_matrix, row, j, first_node, n, size, list(list_of_row), list(edges), all_euler_cycles)        
                        list_of_row.pop()
                        edges.append([row, j])
                        edges.append([j, row])
                        size -= 1    
                        
    
    def euler_cycles(self):
        
        all_euler_cycles = []
        
        number_of_edges = len(self.graph.edges_without_itself)/2
        
        for j in range(0, len(self.graph.weight_matrix)):
            self.euler_cycle(self.graph.weight_matrix, None, j, j, number_of_edges, 0, [], list(self.graph.edges_without_itself), all_euler_cycles)   
    
        return all_euler_cycles
    
    
    def print_euler_cycles(self):
        
        print "\nEuler Cycles:"
        print "------------\n"
        
        all_euler_cycles = self.euler_cycles()
        
        for euler_cycle in all_euler_cycles:
            print euler_cycle
            
      
    def euler_path(self, weight_matrix, prev, row, n, size, list_of_row, edges, all_euler_paths):
        
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if [row+1, j+1] not in list_of_row and [j+1, row+1] not in list_of_row:
                
                    size += 1
                    list_of_row.append([row+1, j+1])

                    edges.remove([row, j])
                    edges.remove([j, row])
                    
                    if size == n:
                        size -= 1
                        if len(edges) == 0:
                            all_euler_paths.append(list(list_of_row))
                        list_of_row.pop()
                        edges.append([row, j])
                        edges.append([j, row])
                    else:
                        self.euler_path(weight_matrix, row, j, n, size, list(list_of_row), list(edges), all_euler_paths)        
                        list_of_row.pop()
                        edges.append([row, j])
                        edges.append([j, row])
                        size -= 1    
                        
    
    def euler_paths(self):
        
        all_euler_paths = []
                
        number_of_edges = len(self.graph.edges_without_itself)/2
        
        for j in range(0, len(self.graph.weight_matrix)):
            self.euler_path(self.graph.weight_matrix, None, j, number_of_edges, 0, [], list(self.graph.edges_without_itself), all_euler_paths)   
    
        return all_euler_paths
    
    
    def print_euler_paths(self):
        
        print "\nEuler Paths:"
        print "-------------\n"
        
        all_euler_paths = self.euler_paths()
        
        for euler_path in all_euler_paths:
            print euler_path   
    
    
    def list_cycle(self, weight_matrix, prev, row, first_node, n, size, list_of_row, all_cycles):
    
        
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if [row+1, j+1] not in list_of_row and [j+1, row+1] not in list_of_row:
                    
                    size += 1
                    list_of_row.append([row+1, j+1])
                    
                    if size == n:
                        size -= 1
                        if j == first_node:
                            all_cycles.append(list(list_of_row))
                        list_of_row.pop()
                    else:
                        self.list_cycle(weight_matrix, row, j, first_node, n, size, list(list_of_row), all_cycles)        
                        list_of_row.pop()
                        size -= 1
        
    
    def list_cycles(self, n, start = 1):
        
        all_cycles = []
                
        for i in range(start, n+1):
            for j in range(0, len(self.graph.weight_matrix)):
                self.list_cycle(self.graph.weight_matrix, None, j, j, i, 0, [], all_cycles)
                
        return all_cycles
              
                
    def print_cycles(self, n):
        
        print "\nCycles:"
        print "------\n"
        
        all_cycles = self.list_cycles(n)
        
        for cycle in all_cycles:
            print cycle
                
    
    def list_path(self, weight_matrix, prev, row, n, size, list_of_row, all_paths):
    
        for j in range(0, len(weight_matrix[row])):
            if weight_matrix[row][j] != "X" and row != j and prev != j:
                if [row+1, j+1] not in list_of_row and [j+1, row+1] not in list_of_row:
                
                    size += 1
                    list_of_row.append([row+1, j+1])
                    
                    if size == n:
                        size -= 1
                        all_paths.append(list(list_of_row))
                        list_of_row.pop()
                    else:
                        self.list_path(weight_matrix, row, j, n, size, list(list_of_row), all_paths)        
                        list_of_row.pop()
                        size -= 1
        
    
    def list_paths(self, n, start = 1):
        
        all_paths = []
        
        for i in range(start, n+1):
            for j in range(0, len(self.graph.weight_matrix)):
                self.list_path(self.graph.weight_matrix, None, j, i, 0, [], all_paths)
                
        return all_paths
        
    
    def print_paths(self, n):
        
        print "\nPaths:"
        print "------\n"
        
        all_paths = self.list_paths(n)
        
        for path in all_paths:
            print path
        
    
    def find_node(self, nodes, node_id):
        
        for node in nodes:
            if node.node_id == node_id:
                return node
        
        return False
        
        
    def select_node(self, nodes, x_pos, y_pos):
        
        min_dist = cfg.radius
        selected_node = None
        
        for node in nodes: 
            dist = math.sqrt((node.x_pos - x_pos) ** 2 + (node.y_pos - y_pos) ** 2)
            if dist <= cfg.radius and dist <= min_dist:
                min_dist = dist
                selected_node = node
        
        if selected_node:
            print "Selected node:", selected_node.node_id       
        return selected_node
    
    
    def select_edge(self, x_pos, y_pos, nodes, weight_matrix):
        
        src_edge = None
        
        for i in range(0, len(weight_matrix)):
            for j in range(0, len(weight_matrix[i])):
                if weight_matrix[i][j] != "X":
                    
                    x = (nodes[i].x_pos+nodes[j].x_pos) / 2
                    y = (nodes[i].y_pos+nodes[j].y_pos) / 2
                    
                    if i == j:
                        if x < cfg.width / 2:
                            x -= cfg.radius * 2
                        else:
                            x += cfg.radius * 2 
                   
                    dist = math.sqrt((x - x_pos) ** 2 + (y - y_pos) ** 2)
                    if dist <= 5:
                        src_edge = [i, j]
                        print  "Selected edge:", src_edge
                        return src_edge
                        
        return src_edge            
    
    
    def add_node(self, nodes, node_count, x_pos, y_pos):
        
        nodes.append(Node(node_count, x_pos, y_pos))
        
        
    def remove_node(self, index_src, nodes):
        
        nodes.pop(index_src)
        
    
    def move_node(self, node, x_pos, y_pos):
        
        node.x_pos = x_pos
        node.y_pos = y_pos
        
    
    def add_edge(self, nodes, src_node, dest_node, weight_matrix):
        
        index_src = nodes.index(src_node)
        index_dest = nodes.index(dest_node)
        weight_matrix[index_src][index_dest] = 0
        weight_matrix[index_dest][index_src] = 0

        if index_src == index_dest:
            self.graph.edges.append([index_src, index_dest])
        else:
            self.graph.edges.append([index_src, index_dest])
            self.graph.edges.append([index_dest, index_src])
            self.graph.edges_without_itself.append([index_src, index_dest])
            self.graph.edges_without_itself.append([index_dest, index_src])
        
    
    def remove_edge(self, i, j, weight_matrix):
        
        weight_matrix[i][j] = "X"
        weight_matrix[j][i] = "X"
        self.graph.edges.remove([i, j])
        
        if i != j:
            self.graph.edges_without_itself.remove([i, j])
            self.graph.edges_without_itself.remove([j, i])
    
        
    def add_weight_matrix(self, node_count, weight_matrix):

        weight_matrix.append(["X"] * node_count)
        
        for i in range(0, node_count-1):
            weight_matrix[i].append("X")
            
    
    def remove_weight_matrix(self, index_src, weight_matrix):
        
        weight_matrix.pop(index_src)
        for i in range(0, len(weight_matrix)):
            weight_matrix[i].pop(index_src)
        
        
    def weight_set(self, weight):
        
        if self.src_edge:
            self.graph.weight_matrix[self.src_edge[0]][self.src_edge[1]] = int(weight)
            self.graph.weight_matrix[self.src_edge[1]][self.src_edge[0]] = int(weight)
            
        self.src_edge = None
        self.queue_draw()
    

    def read_graph_from_file(self, filename):
        
        self.node_count = 0
        self.graph.nodes = []
        self.graph.edges = []
        self.graph.edges_without_itself = []
        self.graph.weight_matrix = []
        
        graph_file = open (filename , 'r')
        graph_list = [ map(str,line.split(' ')) for line in graph_file ]
        
        number_of_nodes = int(graph_list[0][0])
        for i in range(1, number_of_nodes+1):
            self.node_count += 1
            self.graph.nodes.append(Node(self.node_count, int(graph_list[i][0]), int(graph_list[i][1])))
        for j in range(i+1, i+number_of_nodes+1):
            self.graph.weight_matrix.append([0] * number_of_nodes)
            for k in range(0, number_of_nodes):
                if graph_list[j][k] == "X" or graph_list[j][k] == "X\n":
                    self.graph.weight_matrix[j-number_of_nodes-1][k] = "X"
                else:
                    index = j-number_of_nodes-1
                    self.graph.weight_matrix[index][k] = int(graph_list[j][k])
                    if index == k:
                        if [index, k] not in self.graph.edges:
                            self.graph.edges.append([index, k])
                    else:
                        self.graph.edges.append([k, index])
                        self.graph.edges_without_itself.append([k, index])           
        
        graph_file.close()
        self.queue_draw()  
        
        
    def write_graph_to_file(self, filename):
        
        graph_file = open(filename, "wb")
        
        graph_file.write(str(len(self.graph.nodes)))
        
        for node in self.graph.nodes:
            graph_file.write("\n" + str(int(node.x_pos)) + " " + str(int(node.y_pos)))
        
        for i in range(0, len(self.graph.weight_matrix)):
            graph_file.write("\n")
            for j in range(0, len(self.graph.weight_matrix[i])):
                graph_file.write(str(self.graph.weight_matrix[i][j]))
                if j != len(self.graph.weight_matrix[i])-1:
                    graph_file.write(" ")
               
        graph_file.close()
        

    def do_expose_event(self, event):

        self.cr = self.window.cairo_create()
        self.cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        self.cr.clip()
        
        self.draw(self.graph.nodes, self.graph.weight_matrix)
        
        
    def key_press_event(self, *args):
        
        event = args[1]
        
        key = gtk.gdk.keyval_name(event.keyval)
        
        if key == "Delete":
            
            if self.src_node:
                
                index_src = self.graph.nodes.index(self.src_node)
                self.remove_node(index_src, self.graph.nodes)
                self.remove_weight_matrix(index_src, self.graph.weight_matrix)
                
                self.src_node = None
                self.queue_draw()
                
            elif self.src_edge:
                
                self.remove_edge(self.src_edge[0], self.src_edge[1], self.graph.weight_matrix)
                
                self.src_edge = None
                self.queue_draw()
                
        if key == "Escape":
            sys.exit()


    def button_press_event(self, *args):

        event = args[1]
        
        if event.button == 1:
            if self.src_node:
                self.move_node(self.src_node, event.x, event.y)
                self.src_node = None
            else:
                self.node_count += 1
                self.add_node(self.graph.nodes, self.node_count, event.x, event.y)
                self.add_weight_matrix(len(self.graph.nodes), self.graph.weight_matrix)
           
        elif event.button == 3:
            self.src_edge = None
            if self.src_node == None:
                self.src_node = self.select_node(self.graph.nodes, event.x, event.y)
            else:
                self.dest_node = self.select_node(self.graph.nodes, event.x, event.y)
            if self.src_node == None and self.dest_node == None:
                self.src_edge = self.select_edge(event.x, event.y, self.graph.nodes, self.graph.weight_matrix)
        
        if self.src_node and self.dest_node:
            self.add_edge(self.graph.nodes, self.src_node, self.dest_node, self.graph.weight_matrix)
            self.src_node, self.dest_node = None, None

        self.queue_draw()
        
        
    def draw(self, nodes, weight_matrix):
        
        self.cr.set_source_rgb(0.8, 0.0, 0.0)
        self.cr.set_line_width(0.3)
            
        for i in range(40, cfg.height, 40):
           
            self.cr.move_to(0, i)
            self.cr.line_to(cfg.width, i) 
            self.cr.stroke()
           
        for i in range(40, cfg.width, 40):
           
            self.cr.move_to(i, 0)
            self.cr.line_to(i, cfg.height) 
            self.cr.stroke()
           
        self.cr.arc(cfg.width/2, cfg.height/2, 5, 0, 2 * math.pi)
        self.cr.stroke()
        
        self.cr.set_source_rgb(0.1, 0.1, 0.4)
        self.cr.set_line_width(2.0)
        
        for node in nodes:
           
            self.cr.arc(node.x_pos, node.y_pos, cfg.radius, 0, 2 * math.pi)
            self.cr.stroke()
           
            self.cr.move_to(node.x_pos-5, node.y_pos+4)
            self.cr.show_text(str(node.node_id))
            self.cr.stroke()
            
        self.cr.set_line_width(0.7)
        for i in range(0, len(weight_matrix)):
            for j in range(0, len(weight_matrix[i])):
                if weight_matrix[i][j] != "X":
                    
                    if i==j:
                        self.cr.save()
                        self.cr.set_line_width(2.0)
                        
                        if nodes[i].x_pos > cfg.width / 2:
                            radius = cfg.radius
                        else:
                            radius = cfg.radius * (-1)
                        
                        self.cr.translate(nodes[i].x_pos + radius, nodes[i].y_pos)
                            
                        self.cr.scale(1, 0.2)
                        self.cr.arc(0, 0, cfg.radius, 0, 2 * math.pi)
                        self.cr.stroke()
                        self.cr.restore()
                        
                        self.cr.arc(nodes[i].x_pos + radius * 2, nodes[i].y_pos, cfg.small_radius, 0, 2 * math.pi)
                        
                        if self.graph.weight_matrix[i][j] != 0:
                            self.cr.move_to(nodes[i].x_pos + radius * 2, nodes[i].y_pos - 5)
                            self.cr.show_text(str(self.graph.weight_matrix[i][j]))
                        
                        self.cr.stroke()    
                        
                    else:
                        self.cr.move_to(nodes[i].x_pos, nodes[i].y_pos)
                        self.cr.line_to(nodes[j].x_pos, nodes[j].y_pos) 
                        self.cr.stroke()
                        
                        x_pos = (nodes[i].x_pos + nodes[j].x_pos) / 2
                        y_pos = (nodes[i].y_pos + nodes[j].y_pos) / 2
                        self.cr.arc(x_pos, y_pos, cfg.small_radius, 0, 2 * math.pi)
                        
                        if self.graph.weight_matrix[i][j] != 0:
                            self.cr.move_to(x_pos, y_pos - 5)
                            self.cr.show_text(str(self.graph.weight_matrix[i][j]))
                        
                        self.cr.stroke()          
                
                
                
