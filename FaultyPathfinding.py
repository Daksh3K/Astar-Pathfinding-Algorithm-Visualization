import tkinter as tk
import math
import time

WIDTH = 20
root = tk.Tk()

class Node:
    
    OPEN = []
    CLOSED = []
    clicks = 0
    start_node = None
    end_node = None
    current_node = None
    
    __slots__ = ['button','row', 'column', 'parent',
     'heuristic', 'Gcost', 'Fcost', 'start', 'end', 'barrier']
    
    def __init__(self, column, row):
        
        self.button = tk.Button(root, width = 2, height = 1,
        command = lambda a=row, b=column: self.click(a, b))
        self.button.grid(row = row, column = column)
        
        self.column = column
        self.row = row
        self.parent = None
        self.heuristic = None
        self.Gcost = None
        self.Fcost = None
        self.start = False
        self.end = False
        self.barrier = False
 
    def click(self, row, column):
        Node.clicks += 1
        if Node.clicks == 1:   
            self.button.config(bg = "green")
            self.start = True
            Node.start_node = (self.column, self.row)
        elif Node.clicks == 2:
            self.button.config(bg = "red")
            self.end = True
            Node.end_node = (self.column, self.row)
        # else :
        #     self.button.config(bg = "black")
        #     self.barrier = True    
    
    @staticmethod
    def add_start_node():
        '''
        finds start node, makes it the current node
        '''
        x,y = Node.start_node       
        Node.current_node = (node_list[x][y].column, node_list[x][y].row)       
        Node.neighbours()

    @staticmethod
    def Fcost_calculation():
        '''
        calculates the Fcost of every item in OPEN
        '''
        xs, ys = Node.start_node
        xe, ye = Node.end_node
        for node in Node.OPEN:
            x, y = node.column, node.row
            node.Gcost =  math.hypot(x - xs, y - ys)#(math.sqrt( (x - xs)**2 + (y - ys)**2 ) ) 
            node.heuristic =  math.hypot(x - xe, y - ye)#math.sqrt( (x - xe)**2 + (y - ye)**2 ) 
            node.Fcost = node.Gcost + 1.5 * node.heuristic
            node.button.config(text = int(node.Fcost))

    @staticmethod
    def neighbours():
        '''
        find the neighbours of current node
        '''
        xc , yc = Node.current_node
        for a in range(xc - 1, xc + 2):
            for b in range(yc - 1, yc + 2):
                if node_list[a][b].start == False and node_list[a][b].barrier == False and node_list[a][b] not in Node.CLOSED:
                    Node.OPEN.append( node_list[a][b] )
                    node_list[a][b].button.config(bg = "purple")
                    root.update_idletasks()
                    time.sleep(0.05)
                    if node_list[a][b].end == True:
                        node_list[a][b].button.config(bg = "red")

        Node.Fcost_calculation()
        Node.find_current()

    @staticmethod
    def find_current():
        '''
        finds node with lowest Fcost from OPEN, and makes it the current node
        '''
        fcost_list = []
        for node in Node.OPEN:
            fcost_list.append(node.Fcost)
  
        openlist_index = fcost_list.index(min(fcost_list))
        xc, yc = Node.OPEN[openlist_index].column, Node.OPEN[openlist_index].row
        node_list[xc][yc].parent = node_list[Node.current_node[0]][Node.current_node[1]]
        Node.current_node = (xc, yc)
        
        if node_list[xc][yc].end == True:
            print("End Node Found")
            Node.find_path()
            return
        
        node.OPEN[openlist_index].button.config(bg = "pink")
        root.update_idletasks()
        time.sleep(0.25)
        
        Node.OPEN.remove(node_list[xc][yc])
        Node.CLOSED.append(node_list[xc][yc])
        fcost_list.clear()
        Node.neighbours()

    @staticmethod
    def find_path():
        '''
        goes through the parent nodes of all current nodes, and draws the path found
        '''
        while True:
            parent_node = node_list[Node.current_node[0]][Node.current_node[1]].parent
            if parent_node.start == True:
                break
            parent_node.button.config(bg = "grey")
            root.update_idletasks()
            time.sleep(0.25)
            Node.current_node = (parent_node.column, parent_node.row)

    # @staticmethod
    # def refresh():
    #     for row in node_list:
    #         for node in row:
    #             node.button.destroy()
    #             row.remove(node)    
    #     for x in range(WIDTH):
    #         row_list = [Node(x, y) for y in range(WIDTH)]
    #         node_list.append(row_list)
        
if __name__ == "__main__":    
    node_list = []
    for x in range(WIDTH):
        row_list = [Node(x, y) for y in range(WIDTH)]
        node_list.append(row_list)

    menu = tk.Toplevel()
    start_button = tk.Button(menu, text = "Start", command = Node.add_start_node).pack()
    #refresh_button = tk.Button(menu, text = "Refresh", command = Node.refresh).pack()
    #next_button = tk.Button(menu, text = "Next", command = Node.neighbours).pack()
    root.tk.mainloop()

# faulty algorithm, doesnt work for barriers