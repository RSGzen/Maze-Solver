import pygame
from .maze_cell import Cell
from .maze_frontier import FrontierNode
from random import choice

class Grid:
    def __init__(self, num_cols, num_rows, cell_size):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size = cell_size
        self.cell_array = []
        self.num_key = 0
        self.startPoint_idx = None
        self.endPoint_idx = None
    
    def drawGrid(self, border_coords, screen):
        for i in range(1, self.num_rows-1):
            start_x, start_y = border_coords[0]
            starting_point = start_x, start_y + (i*self.cell_size)

            end_x, end_y = border_coords[1]
            end_point = end_x, end_y + (i*self.cell_size)  

            pygame.draw.line(screen, (0,0,0), starting_point, end_point, 1)
        
        for i in range(1, self.num_cols-1):
            start_x, start_y = border_coords[0]
            starting_point = start_x + (i*self.cell_size), start_y

            end_x, end_y = border_coords[3]
            end_point = end_x + (i*self.cell_size), end_y

            pygame.draw.line(screen, (0,0,0), starting_point, end_point, 1)

    def initializeGrid(self):  
        for y in range(0, self.num_rows):
            for x in range(0, self.num_cols):
                temp_cell = Cell(x, y)
                self.cell_array.append(temp_cell)
    
    def checkCellArrayIndex(self, x_index, y_index):
        index = x_index + (y_index*20)
        
        return index
    
    def checkCellXandYIndex(self, index):
        x_index = index % 20
        y_index = index // 20
        
        return x_index, y_index
    
    def checkCellXandYPos(self, x_index, y_index, border_coords):
        top_left_x, top_left_y = border_coords[0]
        top_left_x = top_left_x+(x_index*self.cell_size)
        top_left_y = top_left_y+(y_index*self.cell_size)

        return top_left_x, top_left_y
    
    def checkCellArrayIndexBetweenTwoCell(self, first_cell_idx, second_cell_idx):
        if (first_cell_idx - second_cell_idx) == 2:
            middle_cell_idx = first_cell_idx - 1
            return middle_cell_idx

        elif (first_cell_idx - second_cell_idx) == -2:
            middle_cell_idx = first_cell_idx + 1
            return middle_cell_idx

        elif (first_cell_idx - second_cell_idx) == 40:
            middle_cell_idx = first_cell_idx - 20
            return middle_cell_idx

        elif (first_cell_idx - second_cell_idx) == -40:
            middle_cell_idx = first_cell_idx + 20
            return middle_cell_idx
    
    def arrayIndexConvertAppendList(self, temp_list, temp_x_idx, temp_y_idx):
        temp_array_idx = self.checkCellArrayIndex(temp_x_idx, temp_y_idx)
        temp_list.append(temp_array_idx)
        return temp_list
    
    def checkNeighbourCellsSpecific(self, current_cell_idx, check_range):
        x_idx, y_idx = self.checkCellXandYIndex(current_cell_idx)
        neighbourIndexList = []
        
        if (x_idx + check_range) < 20:
            temp_x_idx, temp_y_idx = x_idx + check_range, y_idx
            neighbourIndexList = self.arrayIndexConvertAppendList(neighbourIndexList, temp_x_idx, temp_y_idx)
        
        if (x_idx - check_range) >= 0:
            temp_x_idx, temp_y_idx = x_idx - check_range, y_idx
            neighbourIndexList = self.arrayIndexConvertAppendList(neighbourIndexList, temp_x_idx, temp_y_idx)
        
        if (y_idx + check_range) < 20:
            temp_x_idx, temp_y_idx = x_idx, y_idx + check_range
            neighbourIndexList = self.arrayIndexConvertAppendList(neighbourIndexList, temp_x_idx, temp_y_idx)
        
        if (y_idx - check_range) >= 0:
            temp_x_idx, temp_y_idx = x_idx, y_idx - check_range
            neighbourIndexList = self.arrayIndexConvertAppendList(neighbourIndexList, temp_x_idx, temp_y_idx)
        
        return neighbourIndexList

    def checkFrontierCells(self, current_cell_idx, history_frontier_cell_idx):      
        neighbourIndexList = self.checkNeighbourCellsSpecific(current_cell_idx, 2)
        frontier_cell_list = []

        for idx in neighbourIndexList:
            current_cell = self.cell_array[idx]
            if current_cell.wall == True:
                if idx not in history_frontier_cell_idx:
                    frontier_cell_list.append(idx)
                    history_frontier_cell_idx.append(idx)
        
        return frontier_cell_list, history_frontier_cell_idx
    
    def cellArrayIndexToXandYPos(self, idx, border_coords):
        x_idx, y_idx = self.checkCellXandYIndex(idx)
        top_left_x, top_left_y = self.checkCellXandYPos(x_idx, y_idx, border_coords)

        return top_left_x, top_left_y

    def drawPassage(self, array_idx, tile_size, screen, color, border_coords):
        x_coord, y_coord = self.cellArrayIndexToXandYPos(array_idx, border_coords)
        temp_rect = pygame.Rect(x_coord, y_coord, tile_size, tile_size)
        pygame.draw.rect(screen, color, temp_rect)

    def generateMazeWalls(self, current_idx, historic_frontier, existing_frontier, node_frontier):
        temp_frontier, historic_frontier = self.checkFrontierCells(current_idx, historic_frontier) 

        temp_node = FrontierNode(current_idx)
        temp_node.frontier_nodes_list = temp_frontier.copy()
        node_frontier.append(temp_node)

        historic_frontier.extend(temp_frontier)

        existing_frontier.extend(temp_frontier)

        picked_frontier = choice(existing_frontier)
        existing_frontier.remove(picked_frontier)

        self.cell_array[picked_frontier].wall = False

        parent_node = temp_node.checkParentAndChildNode(picked_frontier, node_frontier)

        middle_cell = self.checkCellArrayIndexBetweenTwoCell(parent_node, picked_frontier)
        self.cell_array[middle_cell].wall = False

        current_idx = picked_frontier

        return current_idx, historic_frontier, existing_frontier, node_frontier

    def randomizedPrimsAlgorithm(self):
        temp_random_list = [*range(0,400,1)]
        current_idx = choice(temp_random_list)
        existing_frontier = []
        historic_frontier = []
        node_frontier = []

        self.cell_array[current_idx].wall = False

        current_idx, historic_frontier, existing_frontier, node_frontier = self.generateMazeWalls(current_idx, historic_frontier, existing_frontier, node_frontier)

        while len(existing_frontier) > 0 :
            current_idx, historic_frontier, existing_frontier, node_frontier = self.generateMazeWalls(current_idx, historic_frontier, existing_frontier, node_frontier)

    def drawMazeGeneration(self, screen, border_coords):
        for cell in self.cell_array:
            if cell.wall == False:
                cell_idx = self.checkCellArrayIndex(cell.x, cell.y)
                self.drawPassage(cell_idx, self.cell_size, screen, (255,255,255), border_coords)

    def setStartPointAndEndPoint(self):
        start_end_idx = []
        
        start_check = False
        for x in range(1,3):
            for y in range(1,3):
                cell_idx = self.checkCellArrayIndex(x, y)
                current_cell = self.cell_array[cell_idx]
                if current_cell.wall == False:
                    current_cell.start_point = True
                    start_end_idx.append(cell_idx)
                    self.startPoint_idx = cell_idx
                    start_check = True
                if start_check == True:
                    break
            if start_check == True:
                break
        
        end_check = False
        for x in range(18, 16, -1):
            for y in range(18, 16, -1):
                cell_idx = self.checkCellArrayIndex(x, y)
                current_cell = self.cell_array[cell_idx]
                if current_cell.wall == False:
                    current_cell.end_point = True
                    start_end_idx.append(cell_idx)
                    self.endPoint_idx = cell_idx
                    end_check = True
                if end_check == True:
                    break
            if end_check == True:
                break
        
        return start_end_idx
    
    def resetCellStatus(self):
        self.num_key = 0
        self.startPoint_idx = None
        self.endPoint_idx = None
        for cell in self.cell_array:
            cell.wall = True
            cell.obstacle = False
            cell.key = False
            cell.visited = False
            cell.start_point = False
            cell.end_point = False
    
    def resetKeyStatus(self):
        self.num_key = 0
        for cell in self.cell_array:
            cell.key = False
    
    def randomGenerateObstacles(self, num_obstacles, border_coords):
        temp_random_list = [*range(0,400,1)]
        
        put_obstacles = 1
        obstacle_pos = []

        while (put_obstacles <= num_obstacles):
            rand_choice = choice(temp_random_list)
            current_cell = self.cell_array[rand_choice]
            if current_cell.wall == False:
                if current_cell.start_point == False:
                    if current_cell.end_point == False:
                        current_cell.obstacle = True
                        x_idx, y_idx = self.checkCellXandYIndex(rand_choice)
                        x_and_y_pos = self.checkCellXandYPos(x_idx, y_idx, border_coords)
                        obstacle_pos.append(x_and_y_pos)
                        put_obstacles += 1

        return obstacle_pos
    
    def checkCellStatus(self):
        cell_count = 0
        for cell in self.cell_array:
            print(f"\n{cell_count}. ", end="")
            if cell.wall == True:
                print("w ", end="")
            if cell.wall == False:
                print("p ", end="")
            if cell.start_point == True:
                print("s ", end="")
            if cell.end_point == True:
                print("e ", end="")
            if cell.obstacle == True:
                print("o ", end="")

            cell_count += 1
    
    def putKey(self, mouse_pos, border_coords, key_idx):
        temp_idx = []
        for i in range(0,400):
            cell_x_pos, cell_y_pos = self.cellArrayIndexToXandYPos(i, border_coords)
            if mouse_pos[0] in range(25, 726) and mouse_pos[1] in range(75, 776):
                if mouse_pos[0] in range(cell_x_pos, cell_x_pos+self.cell_size) and mouse_pos[1] in range(cell_y_pos, cell_y_pos+self.cell_size):
                    current_cell = self.cell_array[i]
                    if current_cell.wall == False:
                        if current_cell.obstacle == False:
                            if current_cell.key == False:
                                if current_cell.start_point == False:
                                    if current_cell.end_point == False:
                                        current_cell.key = True
                                        temp_idx.append(i)
                                        key_idx.extend(temp_idx)
                                        self.num_key += 1
                                        return key_idx
        
        return key_idx
    
    def removeKey(self, mouse_pos, border_coords, key_idx):
        for i in range(0, 400):
            cell_x_pos, cell_y_pos = self.cellArrayIndexToXandYPos(i, border_coords)
            if mouse_pos[0] in range(25, 726) and mouse_pos[1] in range(75, 776):
                if mouse_pos[0] in range(cell_x_pos, cell_x_pos+self.cell_size) and mouse_pos[1] in range(cell_y_pos, cell_y_pos+self.cell_size):
                    current_cell = self.cell_array[i]
                    if current_cell.key == True:
                            key_idx.remove(i)
                            current_cell.key = False
                            self.num_key -= 1
                            return key_idx
        
        return key_idx

    def convert2D(self):
        maze_info = []
        for y in range(0, 20):
            temp_row_info = []
            for x in range(0, 20):
                current_idx = self.checkCellArrayIndex(x, y)
                current_cell = self.cell_array[current_idx]
                if current_cell.wall == True:
                    current_cell_condition = 0 # wall = 0
                else:
                    if current_cell.obstacle == True:
                        current_cell_condition = 2 # obstacle = 2
                    elif current_cell.key == True:
                        current_cell_condition = 3 # key = 3
                    elif current_cell.start_point == True:
                        current_cell_condition = 4 # start_point = 4
                    elif current_cell.end_point == True: 
                        current_cell_condition = 5 # end_point = 5
                    else:
                        current_cell_condition = 1 # passage = 1
                temp_row_info.append(current_cell_condition)
            maze_info.append(temp_row_info)
        
        return maze_info
        