from collections import deque
import time

class search_algo:
    def __init__(self, maze):
        self.maze = maze
        self.rows = 20
        self.colms = 20
        self.path_cost=0
        self.start_point = self.find_start_point()
        self.end_point = self.find_end_point()
        self.key_point = self.find_key_point()

        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


    def find_start_point(self):
        for y in range (0,self.rows ):
            for x in range (0, self.colms):
                if self.maze[x][y] == 4:
                    return(x,y)
    
    def find_end_point(self):
        for y in range (0, self.rows ):
            for x in range (0, self.colms):
                if self.maze[x][y] == 5:
                    return(x,y)
                
                
    def find_key_point(self):
        keys = []
        for y in range(self.rows):
            for x in range(self.colms):
                if self.maze[x][y] == 3:
                   keys.append((x,y))
        return keys

    def calculate_path_cost(self, path):
        cost = 1  
        for position in path:
            x, y = position
            if self.maze[x][y] == 1:
                cost += 1
            if self.maze[x][y] == 2:
                cost += 5
        return cost  

    def bfs(self,current_start_point,keypoint):
        queue = deque([current_start_point])
        visited = set([current_start_point])
        parent = {current_start_point: None}

        while queue:
            current = queue.popleft() #after explore the node remove it 
            
            if current == keypoint:
                path = []
                while current:
                    path.append(current)
                    current = parent[current] 
                path.reverse()
                # print("Get the path already")  
                return path

            time.sleep(0.001) # Small delay to make the timing measurement noticeable

            for x in self.directions: #finding the neighbour for up down laft right of current position
                neighbor = (current[0] + x[0], current[1] + x[1]) #set all neighbour

                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.colms: #check valid of neighbour
                    if self.maze[neighbor[0]][neighbor[1]] != 0 and neighbor not in visited: #check valid of neighbour
                        queue.append(neighbor) 
                        visited.add(neighbor)
                        parent[neighbor] = current 

    def find_path_current_to_keyBFS(self):  
        current_start_point = self.start_point
        # path_current_to_end=[]   
        final_path =[]
        if self.key_point:
            for key in self.key_point:
                path_to_key = self.bfs(current_start_point, key)
                if path_to_key:   
                    final_path.extend(path_to_key[:-1]) # : to prevent the duplication for the last coordinate(in 1st list) and 1st coordinate ()in the next list)
                    current_start_point = key
            path_current_to_end = self.bfs(current_start_point, self.end_point)
            if path_current_to_end:
                final_path.extend(path_current_to_end)
        else:
            path_current_to_end = self.bfs(current_start_point, self.end_point)
            final_path.extend(path_current_to_end)
        return final_path

    def run_algorithmBFS (self):
        start_time = time.time()
        path = self.find_path_current_to_keyBFS()
        end_time = time.time() 
        time_taken = end_time - start_time # Calculate the total time taken
        return path, time_taken
            
    def dfs_with_depth_limit(self,start_point,limit,goal):
        stack = [(start_point, [start_point], 0)] #staring position, list from start to current position, initial deapth lvl
        visited = set()
        time.sleep(0.001) # Small delay to make the timing measurement noticeable


        while stack:  
            current, path, depth = stack.pop() #unpack the last note in the stack 
            if depth > limit:  
                continue
            if current == goal:
                return path #if we find the end, we should return the path
            visited.add(current) 
            for x in self.directions:
                neighbor = (current[0] + x[0], current[1] + x[1]) 
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.colms:
                    if self.maze[neighbor[0]][neighbor[1]] != 0 and neighbor not in visited: 
                        stack.append((neighbor, path + [neighbor], depth + 1)) 
        return None
    
    def ids (self,current_start_point,endpoint):
        limit = 0
        # print("Get the path already")  
        while True:
            path = self.dfs_with_depth_limit(current_start_point,limit,endpoint)
            if path is not None: 
                return path
            limit += 1

    def find_path_current_to_keyIDS(self):  
        current_start_point = self.start_point
        path_current_to_end=[]
        final_path =[]
        if self.key_point:
            for key in self.key_point:
                path_to_key = self.ids(current_start_point, key)
                if path_to_key:   
                    final_path.extend(path_to_key[:-1]) 
                    current_start_point = key
            path_current_to_end = self.ids(current_start_point, self.end_point)
            if path_current_to_end:
                final_path.extend(path_current_to_end)
            return final_path
        else:
            path_current_to_end = self.ids(current_start_point, self.end_point)
            return path_current_to_end

    def run_algorithmIDS (self):
        # print("inside run_algorithmIDS")
        start_time = time.time()
        path = self.find_path_current_to_keyIDS()
        end_time = time.time() # End time
        time_taken = end_time - start_time # Calculate the total time taken
        return path, time_taken

    def final_outcome(self,algorithem_name):
        path=[]
        # print("inside final_outcome")
        if algorithem_name == "BFS":
            path, time_taken = self.run_algorithmBFS()
            path_cost = self.calculate_path_cost(path)
            return path,time_taken,path_cost
        
        elif algorithem_name == "IDS":
            #print("inside final of IDS")
            path, time_taken = self.run_algorithmIDS()
            path_cost = self.calculate_path_cost(path)
            return path,time_taken,path_cost
        
        else:
            print("error")