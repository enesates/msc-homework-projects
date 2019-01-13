import pygtk, gtk.gdk
pygtk.require('2.0')

import graph_area
import config as cfg


class Interface():
   
    
    def graph_paint(self, *args):
        
        self.g_area.graph_paint()
        
    
    def shortest_path(self, *args):
        
        if self.shortest_from_entry.get_text() and self.shortest_to_entry.get_text():
            shortest_from = int(self.shortest_from_entry.get_text())-1
            shortest_to   = int(self.shortest_to_entry.get_text())-1
            
            self.g_area.shortest_path(shortest_from, shortest_to)
        
    
    def are_isomorphic(self, *args):
        
        filename = self.chooser_dialog("open")
        if filename:
            self.g_area.are_isomorphic(filename)
        
    
    def is_a_planar(self, *args):
        
        self.g_area.is_a_planar()
        
        
    def is_a_bipartite(self, *args):
        
        self.g_area.is_a_bipartite()
        
        
    def is_a_tree(self, *args):
        
        self.g_area.is_a_tree()

    
    def print_hamilton_paths(self, *args):
        
        self.g_area.print_hamilton_paths()
        
        
    def print_hamilton_cycles(self, *args):
        
        self.g_area.print_hamilton_cycles()
    
    
    def print_euler_paths(self, *args):
        
        self.g_area.print_euler_paths()
        
        
    def print_euler_cycles(self, *args):
        
        self.g_area.print_euler_cycles()
        
        
    def print_paths(self, *args):
        
        n = int(self.print_paths_entry.get_text())
        self.g_area.print_paths(n)
   
    
    def print_cycles(self, *args):
        
        n = int(self.print_cycles_entry.get_text())
        self.g_area.print_cycles(n)
    
    
    def weight_set(self, *args):
        
        weight = self.weight_entry.get_text()
        self.g_area.weight_set(weight)
        
    
    def read_graph_from_file(self, *args):
        
#        filename = self.chooser_dialog("open")
#        if filename:
#            self.g_area.read_graph_from_file(filename)
        self.g_area.read_graph_from_file("graph.txt")
            
            
    def write_graph_to_file(self, *args):
        
        filename = self.chooser_dialog("save")
        if filename:
            self.g_area.write_graph_to_file(filename)
    
    
    def chooser_dialog(self, action):
        
        if action == "open":
            action = gtk.FILE_CHOOSER_ACTION_OPEN
            action_button = gtk.STOCK_OPEN
        elif action == "save":
            action = gtk.FILE_CHOOSER_ACTION_SAVE
            action_button = gtk.STOCK_SAVE
            
        dialog = gtk.FileChooserDialog("Choose a File", None, action,
                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                        action_button, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        file_filter = gtk.FileFilter()
        file_filter.set_name("Text")
        file_filter.add_mime_type("text/txt")
        file_filter.add_pattern("*.txt")
        dialog.add_filter(file_filter)

        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
                
        elif response == gtk.RESPONSE_CANCEL:
            
            print "No file selected"
            dialog.destroy()
            return None 
    
    
    def run(self):
        
        window = gtk.Window()
        window.set_title("Graph Library")
        window.set_size_request(cfg.width + 300, cfg.height)
        window.connect("delete_event", gtk.main_quit)
        
        self.g_area = graph_area.Graph_Area()
        self.g_area.set_size_request(cfg.width, cfg.height)
        fixed = gtk.Fixed()
        
        
        window.connect('key_press_event',self.g_area.key_press_event)
        self.g_area.connect('button_press_event',self.g_area.button_press_event)
        self.g_area.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.POINTER_MOTION_MASK
                            | gtk.gdk.POINTER_MOTION_HINT_MASK)
        
        self.weight_label = gtk.Label("Weight:")
        self.weight_entry = gtk.Entry()
        self.weight_entry.set_size_request(40, 20)
        self.weight_set_button = gtk.Button("Set Weight")
        self.weight_set_button.connect("clicked", self.weight_set)
        
        self.read_graph_button = gtk.Button("Read Graph From File")
        self.read_graph_button.connect("clicked", self.read_graph_from_file)
        
        self.write_graph_button = gtk.Button("Write Graph to File")
        self.write_graph_button.connect("clicked", self.write_graph_to_file)
        
        self.print_paths_label = gtk.Label("n:")
        self.print_paths_entry = gtk.Entry()
        self.print_paths_entry.set_size_request(40, 20)       
        self.print_paths_entry.set_text("1")       
        self.print_paths_button = gtk.Button("List Paths")
        self.print_paths_button.connect("clicked", self.print_paths)
        
        self.print_cycles_label = gtk.Label("n:")
        self.print_cycles_entry = gtk.Entry()
        self.print_cycles_entry.set_size_request(40, 20)          
        self.print_cycles_entry.set_text("1")          
        self.print_cycles_button = gtk.Button("List Cycles")
        self.print_cycles_button.connect("clicked", self.print_cycles)
        
        self.print_euler_paths_button = gtk.Button("List Euler Paths")
        self.print_euler_paths_button.connect("clicked", self.print_euler_paths)
        
        self.print_euler_cycles_button = gtk.Button("List Euler Cycles")
        self.print_euler_cycles_button.connect("clicked", self.print_euler_cycles)
                
        self.print_hamilton_paths_button = gtk.Button("List Hamilton Paths")
        self.print_hamilton_paths_button.connect("clicked", self.print_hamilton_paths)
        
        self.print_hamilton_cycles_button = gtk.Button("List Hamilton Cycles")
        self.print_hamilton_cycles_button.connect("clicked", self.print_hamilton_cycles)
        
        self.shortest_from_label = gtk.Label("From:")
        self.shortest_from_entry = gtk.Entry()
        self.shortest_from_entry.set_size_request(40, 20)  
        self.shortest_to_label = gtk.Label("To:")
        self.shortest_to_entry = gtk.Entry()
        self.shortest_to_entry.set_size_request(40, 20)  
        self.shortest_path_button = gtk.Button("Find Shortest Path")
        self.shortest_path_button.connect("clicked", self.shortest_path)

        self.graph_paint_button = gtk.Button("Graph Paint")
        self.graph_paint_button.connect("clicked", self.graph_paint)
        
        self.are_isomorphic_button = gtk.Button("Graphs are Isomorphic?")
        self.are_isomorphic_button.connect("clicked", self.are_isomorphic)
        
        self.is_a_bipartite_button = gtk.Button("Graph is a Bipartite?")
        self.is_a_bipartite_button.connect("clicked", self.is_a_bipartite)
        
        self.is_a_planar_button = gtk.Button("Graph is a Planar?")
        self.is_a_planar_button.connect("clicked", self.is_a_planar)
        
        self.is_a_tree_button = gtk.Button("Graph is a Tree?")
        self.is_a_tree_button.connect("clicked", self.is_a_tree)
               
        fixed.put(self.g_area, 0, 0)
        fixed.put(self.weight_label, 650, 27)
        fixed.put(self.weight_entry, 700, 25)
        fixed.put(self.weight_set_button, 750, 20)
        
        fixed.put(self.read_graph_button, 650, 60)
        fixed.put(self.write_graph_button, 800, 60)
        
        fixed.put(self.print_paths_label, 650, 117)
        fixed.put(self.print_paths_entry, 665, 115)
        fixed.put(self.print_paths_button, 710, 110)
        fixed.put(self.print_cycles_label, 790, 117)
        fixed.put(self.print_cycles_entry, 805, 115)
        fixed.put(self.print_cycles_button, 850, 110)
        
        fixed.put(self.print_euler_paths_button, 650, 160)
        fixed.put(self.print_euler_cycles_button, 800, 160)
        
        fixed.put(self.print_hamilton_paths_button, 650, 190)
        fixed.put(self.print_hamilton_cycles_button, 800, 190)
        
        fixed.put(self.shortest_from_label, 660, 247)
        fixed.put(self.shortest_from_entry, 695, 245)
        fixed.put(self.shortest_to_label, 740, 247)
        fixed.put(self.shortest_to_entry, 765, 245)
        fixed.put(self.shortest_path_button, 820, 240)
        
        fixed.put(self.graph_paint_button, 650, 310)
        fixed.put(self.are_isomorphic_button, 650, 340)
        fixed.put(self.is_a_bipartite_button, 650, 370)
        fixed.put(self.is_a_planar_button, 650, 400)
        fixed.put(self.is_a_tree_button, 650, 430)
        
        
        window.add(fixed)
        fixed.show()
        window.present()
        window.show_all()
        gtk.main()


if __name__ == "__main__":
    
    interface = Interface()
    interface.run()