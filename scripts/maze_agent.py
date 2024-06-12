import pygame

class Agent:
    def __init__(self, border_coords):
        self.idx = None
        self.x_idx = None
        self.y_idx = None
        self.x_pos = None
        self.y_pos = None
        self.start_point_idx = None
        self.end_point_idx = None
        self.num_key_available = None
        self.num_key_found = 0
        self.reached_goal = False
        self.border_coords = border_coords
        self.path = []
        self.visited_path = []

    def checkCellXandYIndex(self):
        x_index = self.idx % 20
        y_index = self.idx // 20
        
        return x_index, y_index
    
    def checkCellXandYPos(self, x_index, y_index):
        top_left_x, top_left_y = self.border_coords[0]
        top_left_x = top_left_x+(x_index*35)
        top_left_y = top_left_y+(y_index*35)

        return top_left_x, top_left_y
    
    def updateAgentXandYPos(self):
        x_pos, y_pos = self.checkCellXandYPos(self.x_idx, self.y_idx)
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def updateAgentXandYIndex(self):
        x_idx, y_idx = self.checkCellXandYIndex()
        self.x_idx = x_idx
        self.y_idx = y_idx
    
    def updateAgentXandYIndexPos(self):
        self.updateAgentXandYIndex()
        self.updateAgentXandYPos()
    
    def clearAgentStatus(self, start_point_idx, num_key_available):
        self.idx = start_point_idx
        self.x_idx = None
        self.y_idx = None
        self.x_pos = None
        self.y_pos = None
        self.start_point_idx = start_point_idx
        self.end_point_idx = None
        self.num_key_available = num_key_available
        self.num_key_found = 0
        self.reached_goal = False
        self.path = []
        self.visited_path = []
    
    def checkPathArrayIndex(self, x_index, y_index):
        index = x_index + (y_index*20)
        
        return index
    
    def invertXandYIdx(self):
        new_path_list = []
        for path in self.path:
            x_idx, y_idx = path
            new_x_idx = y_idx
            new_y_idx = x_idx
            new_path_list.append((new_x_idx, new_y_idx))
        
        return new_path_list
    
    def draw_rect_outline(self, screen, color, x_pos, y_pos, tile_size, width):
        pygame.draw.line(screen, color, (x_pos+2, y_pos+2), (x_pos+tile_size-4, y_pos+2), width)
        pygame.draw.line(screen, color, (x_pos+tile_size-4, y_pos+2),  (x_pos+tile_size-4, y_pos+tile_size-4), width)
        pygame.draw.line(screen, color, (x_pos+tile_size-4, y_pos+tile_size-4), (x_pos+2, y_pos+tile_size-4), width)
        pygame.draw.line(screen, color, (x_pos+2, y_pos+2), (x_pos+2, y_pos+tile_size-4), width)

    def pathTracing(self, screen, max_path_length):
        color_list = ["#FF2300", "#FF9300", "#FFF000", "#59FF00", "#0051FF", "#6800FF"]
        max_stages = max_path_length // len(color_list)

        for i in range(0, len(self.visited_path)):
            color_idx = i // max_stages
            x_idx, y_idx = self.visited_path[i]
            x_pos, y_pos = self.checkCellXandYPos(x_idx, y_idx)
            if color_idx == 6:
                color_idx -= 1
            self.draw_rect_outline(screen, color_list[color_idx], x_pos, y_pos, 35, 3)