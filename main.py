import pygame #egiuhwroijwgweoih
import time 
import sys
from scripts.maze_button import Button
from scripts.maze_grid import Grid
from scripts.maze_agent import Agent
from scripts.maze_algorithm import search_algo
from scripts.maze_algo_dijkstra import dijkstra
from scripts.maze_algo_gbfs import gbfs

pygame.init() #initialize the pygame library

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 850

BORDER_WIDTH = 700
BORDER_HEIGHT = 700

CELL_SIZE = 35
NUM_ROWS = BORDER_HEIGHT // CELL_SIZE
NUM_COLS = BORDER_WIDTH // CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

background = pygame.image.load(r"assets\background.jpg")

clock = pygame.time.Clock()

def getFont(size):
    return pygame.font.Font("assets/font.ttf", size)

def drawText(text, font, text_color, x_and_y, screen):
    text_img = font.render(text, True, text_color)
    screen.blit(text_img, x_and_y)

def showGridNumbers(border_coords, screen):
    temp_obj = Grid(NUM_COLS, NUM_ROWS, CELL_SIZE)
    for i in range(0, 400):
        text = str(i)
        x_and_y = temp_obj.cellArrayIndexToXandYPos(i, border_coords)
        drawText(text, getFont(10), (40,76,255), x_and_y, screen)

def showMaze2DInfo(maze_obj):
    maze_info = maze_obj.convert2D()
    print(f"\nMaze Information: \n{maze_info}")

def drawStartAndEndPoints(start_end_idx, border_coords, screen):
    temp_obj = Grid(NUM_COLS, NUM_ROWS, CELL_SIZE)
    temp_obj.drawPassage(start_end_idx[0], CELL_SIZE, screen, (175,43,13), border_coords)
    temp_obj.drawPassage(start_end_idx[1], CELL_SIZE, screen, (38,120,18), border_coords)

def drawLinesForStartScreen(screen):
    pygame.draw.line(screen, (255,255,255), (755, 250), (1230, 250), width=4)
    pygame.draw.line(screen, (255,255,255), (755, 410), (1230, 410), width=4)
    pygame.draw.line(screen, (255,255,255), (755, 520), (1230, 520), width=4)
    pygame.draw.line(screen, (255,255,255), (755, 660), (1230, 660), width=4)

def start():
    key_idx = []
    none_key_idx = []
    start_run = True
    maze_generation_check = True
    border_coords = [(25,75), (25+BORDER_WIDTH,75), (25+BORDER_WIDTH,75+BORDER_HEIGHT), (25,75+BORDER_HEIGHT)]
    #border_coords = [top_left corner, top_right corner, bottom_right corner, bottom_left corner]

    maze_grid = Grid(NUM_COLS, NUM_ROWS, CELL_SIZE)
    agent = Agent(border_coords)

    OBSTACLE = pygame.image.load(r"assets\obstacle.png")
    OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE, (33,33))

    KEY = pygame.image.load(r"assets\key.png")
    KEY_IMAGE = pygame.transform.scale(KEY, (33,33))

    AGENT = pygame.image.load(r"assets\agent.png")
    AGENT_IMAGE = pygame.transform.scale(AGENT, (33,33))

    NONE_KEY = pygame.image.load(r"assets\red_cross.png")
    NONE_KEY_IMAGE = pygame.transform.scale(NONE_KEY, (33,33))

    MAX_KEY = 4

    choosen_algo = None
    time_taken = None
    path_cost = None

    no_algo_check = False
    no_algo_display_time = None

    algo_start_run = False
    algo_start_run_key_lock = False
    algo_start_run_reached_end = False
    algo_start_run_time = None
    algo_start_run_current_idx = 0

    clear_check = True
    clear_text_check = False
    clear_text_start_time = None

    while start_run == True:
        clock.tick(60)
        START_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        START_BACK = Button(None, (1120, 770), "BACK", getFont(40),"White", "Green")

        START_BACK.changeColor(START_MOUSE_POS)
        START_BACK.update(screen)

        START_REROLL = Button(None, (875, 770), "REROLL", getFont(40),"White", "Green")

        START_REROLL.changeColor(START_MOUSE_POS)
        START_REROLL.update(screen)

        START_BEGIN = Button(None, (855, 700), "BEGIN", getFont(40),"White", "Green")

        START_BEGIN.changeColor(START_MOUSE_POS)
        START_BEGIN.update(screen)

        START_CLEAR = Button(None, (1135, 700), "CLEAR", getFont(40),"White", "Green")

        START_CLEAR.changeColor(START_MOUSE_POS)
        START_CLEAR.update(screen)

        START_ALGO_BFS = Button(None, (815, 160), "BFS", getFont(30),"White", "Red")

        START_ALGO_BFS.changeColor(START_MOUSE_POS)
        START_ALGO_BFS.update(screen)

        START_ALGO_IDS = Button(None, (1135, 160), "IDS", getFont(30),"White", "Red")

        START_ALGO_IDS.changeColor(START_MOUSE_POS)
        START_ALGO_IDS.update(screen)

        START_ALGO_GBFS = Button(None, (975, 160), "GBFS", getFont(30),"White", "Red")

        START_ALGO_GBFS.changeColor(START_MOUSE_POS)
        START_ALGO_GBFS.update(screen)

        START_ALGO_DIJKSTRA = Button(None, (975, 210), "DIJKSTRA'S", getFont(30),"White", "Red")

        START_ALGO_DIJKSTRA.changeColor(START_MOUSE_POS)
        START_ALGO_DIJKSTRA.update(screen)

        for i in range(0,4):
            if i == 3:
                k = 0
            else:
                k = i+1
            pygame.draw.line(screen, (255,255,255), border_coords[i], border_coords[k], width=3)
        
        drawLinesForStartScreen(screen)

        maze_grid.initializeGrid()
        maze_grid.drawGrid(border_coords, screen)

        drawText("PICK AN ALGO:", getFont(35), "Yellow", (752, 78), screen)
        drawText("CURRENT ALGO:", getFont(35), "White", (765, 280), screen)
        drawText("Num Keys: ", getFont(24), "White", (765,435), screen)
        drawText("Time Taken: ", getFont(24), "White", (761,550), screen)
        drawText("Path Cost : ", getFont(24), "White", (765,600), screen)

        num_key_text = str(maze_grid.num_key) + " / " + str(MAX_KEY)
        drawText(num_key_text, getFont(24), "Green", (1010,435), screen)

        match choosen_algo:
            case 1:
                drawText("BFS", getFont(40), "Red", (925, 340), screen)

            case 2:
                drawText("IDS", getFont(40), "Red", (925, 340), screen)

            case 3:
                drawText("GBFS", getFont(40), "Red", (905, 340), screen)

            case 4:
                drawText("DIJKSTRA'S", getFont(40), "Red", (795, 340), screen)

            case None:
                pass

        if maze_generation_check == True:
            maze_grid.randomizedPrimsAlgorithm()
            start_end_idx = maze_grid.setStartPointAndEndPoint()
            obstacle_pos = maze_grid.randomGenerateObstacles(10, border_coords)
            agent.start_point_idx = maze_grid.startPoint_idx
            agent.idx = maze_grid.startPoint_idx
            agent.updateAgentXandYIndexPos()
            maze_generation_check = False
        else:
            maze_grid.drawMazeGeneration(screen, border_coords)
            drawStartAndEndPoints(start_end_idx, border_coords, screen)

            for pos in obstacle_pos:
                screen.blit(OBSTACLE_IMAGE, pos)
            
            if len(key_idx) > 0:
                for idx in key_idx:
                    pos = maze_grid.cellArrayIndexToXandYPos(idx, border_coords)
                    screen.blit(KEY_IMAGE, pos)
            
            if len(none_key_idx) > 0:
                for idx in none_key_idx:
                    pos = maze_grid.cellArrayIndexToXandYPos(idx, border_coords)
                    screen.blit(NONE_KEY_IMAGE, pos)
            
            if maze_grid.num_key == MAX_KEY:
                drawText("REACHED MAX KEY", getFont(24), "Red", (790,475), screen)
            
            if time_taken != None:
                time_taken = round(time_taken, 5)
                TIME_TAKEN_TEXT = str(time_taken)
                drawText(TIME_TAKEN_TEXT, getFont(24), "Green", (1050,550), screen)

            if path_cost != None:
                PATH_COST_TEXT = str(path_cost)
                drawText(PATH_COST_TEXT, getFont(24), "Green", (1050,600), screen)
            
            if (no_algo_check == True) and choosen_algo == None:
                drawText("Choose Algo!", getFont(35), "Red", (770, 340), screen)
                if (time.time() - no_algo_display_time) >2:
                    no_algo_check = False
            
            if clear_text_check == True:
                drawText("Please Clear Maze To Begin!", getFont(30), "Red", (250, 30), screen)
                if (time.time() - clear_text_start_time) >2:
                    clear_text_check = False
            
            if algo_start_run == True:
                max_path_num = len(agent.path)
                screen.blit(AGENT_IMAGE, (agent.x_pos, agent.y_pos))
                agent.pathTracing(screen, max_path_num)

                if (time.time() - algo_start_run_time >= 0.3*algo_start_run_current_idx):
                    algo_start_run_current_idx += 1

                    if algo_start_run_current_idx < max_path_num:
                        agent.x_idx, agent.y_idx = agent.path[algo_start_run_current_idx]
                        agent.visited_path.append(agent.path[algo_start_run_current_idx])
                        agent.idx = agent.checkPathArrayIndex(agent.x_idx, agent.y_idx)
                        agent.updateAgentXandYIndexPos()

                        if agent.idx in key_idx:
                            none_key_idx.append(agent.idx)
                        
                    else:
                        algo_start_run_key_lock = False
                        algo_start_run_reached_end = True
                        algo_start_run = False

            if algo_start_run_reached_end == True:
                max_path_num = len(agent.path)
                agent.x_idx, agent.y_idx = agent.path[max_path_num-1]
                agent.idx = maze_grid.checkCellArrayIndex(agent.x_idx, agent.y_idx)
                agent.updateAgentXandYIndexPos()
                screen.blit(AGENT_IMAGE, (agent.x_pos, agent.y_pos))
                agent.pathTracing(screen, max_path_num)
            
            if algo_start_run == False:
                screen.blit(AGENT_IMAGE, (agent.x_pos, agent.y_pos))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if START_BACK.checkForInput(START_MOUSE_POS):
                        mainMenu()

                    if START_BEGIN.checkForInput(START_MOUSE_POS):
                        if clear_check == True:
                            agent.start_point_idx = maze_grid.startPoint_idx
                            agent.idx = maze_grid.startPoint_idx
                            agent.num_key_available = maze_grid.num_key
                            if choosen_algo != None:
                                maze_info = maze_grid.convert2D()
                                algo_start_run = True

                                if choosen_algo == 1:
                                    search = search_algo(maze_info)
                                    algo_start_run_time = time.time()
                                    agent.path, time_taken, path_cost= search.final_outcome("BFS")
                                    agent.path = agent.invertXandYIdx()
                                    clear_check = False
                                    algo_start_run_key_lock = True

                                elif choosen_algo == 2:
                                    search = search_algo(maze_info)
                                    algo_start_run_time = time.time()
                                    agent.path, time_taken, path_cost= search.final_outcome("BFS")
                                    agent.path = agent.invertXandYIdx()
                                    clear_check = False
                                    algo_start_run_key_lock = True

                                elif choosen_algo == 3:
                                    algo_start_run_time = time.time()
                                    agent.path, path_cost = gbfs(maze_grid, maze_grid.startPoint_idx, key_idx, maze_grid.endPoint_idx)
                                    time_taken = time.time() - algo_start_run_time
                                    clear_check = False
                                    algo_start_run_key_lock = True

                                elif choosen_algo == 4:
                                    algo_start_run_time = time.time()
                                    agent.path, path_cost = dijkstra(maze_grid, maze_grid.startPoint_idx, key_idx, maze_grid.endPoint_idx)
                                    time_taken = time.time() - algo_start_run_time
                                    clear_check = False
                                    algo_start_run_key_lock = True

                            else:
                                no_algo_display_time = time.time()
                                no_algo_check = True
        
                        else:
                            clear_text_check = True
                            clear_text_start_time = time.time()

                    if START_CLEAR.checkForInput(START_MOUSE_POS):
                        maze_grid.resetKeyStatus()
                        choosen_algo = None
                        time_taken = None
                        path_cost = None
                        key_idx = []
                        none_key_idx = []
                        agent.clearAgentStatus(0,0)
                        agent.start_point_idx = maze_grid.startPoint_idx
                        agent.idx = maze_grid.startPoint_idx
                        agent.updateAgentXandYIndexPos()
                        no_algo_check = False
                        no_algo_display_time = None

                        algo_start_run = False
                        algo_start_run_key_lock = False
                        algo_start_run_reached_end = False
                        algo_start_run_time = None
                        algo_start_run_current_idx = 0
                        clear_check = True
                        clear_text_check = False
                        clear_text_start_time = None

                    if START_REROLL.checkForInput(START_MOUSE_POS):
                        maze_grid.resetCellStatus()
                        maze_grid.randomizedPrimsAlgorithm()
                        start_end_idx = maze_grid.setStartPointAndEndPoint()
                        obstacle_pos = maze_grid.randomGenerateObstacles(10, border_coords)
                        choosen_algo = None
                        time_taken = None
                        path_cost = None
                        key_idx = []
                        none_key_idx = []
                        agent.clearAgentStatus(0,0)
                        agent.start_point_idx = maze_grid.startPoint_idx
                        agent.idx = maze_grid.startPoint_idx
                        agent.updateAgentXandYIndexPos()
                        no_algo_check = False
                        no_algo_display_time = None

                        algo_start_run = False
                        algo_start_run_key_lock = False
                        algo_start_run_reached_end = False
                        algo_start_run_time = None
                        algo_start_run_current_idx = 0
                        clear_check = True
                        clear_text_check = False
                        clear_text_start_time = None

                    if algo_start_run_key_lock == False:
                        if START_ALGO_BFS.checkForInput(START_MOUSE_POS):
                            choosen_algo = 1
                        if START_ALGO_IDS.checkForInput(START_MOUSE_POS):
                            choosen_algo = 2
                        if START_ALGO_GBFS.checkForInput(START_MOUSE_POS):
                            choosen_algo = 3
                        if START_ALGO_DIJKSTRA.checkForInput(START_MOUSE_POS):
                            choosen_algo = 4
                    
                    if algo_start_run_key_lock == False:
                        if maze_grid.num_key < MAX_KEY:
                            key_idx = maze_grid.putKey(START_MOUSE_POS, border_coords, key_idx)
                            if type(key_idx) == type(None):
                                key_idx = []  
                
                if event.button == 3:
                    if algo_start_run_key_lock == False:
                        if maze_grid.num_key >= 0:
                            key_idx = maze_grid.removeKey(START_MOUSE_POS, border_coords, key_idx)
                            if type(key_idx) == type(None):
                                key_idx = []

        pygame.display.update()

def credit():
    options_run = True

    while options_run == True:
        clock.tick(60)
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("#79578a")

        RULES_Tittle = getFont(50).render(" Ge Rui Sen", True, "light blue")
        RULES_TRect = RULES_Tittle.get_rect(center=(232, 40))
        screen.blit(RULES_Tittle, RULES_TRect)

        RULES_1TEXT = getFont(20).render("- Maze system developer", True, "Black")
        RULES_1RECT = RULES_1TEXT.get_rect(center=(270, 100)) 
        screen.blit(RULES_1TEXT, RULES_1RECT)

        RULES_2TEXT = getFont(20).render("- Design overall structure, layout of maze system", True, "Black")
        RULES_2RECT = RULES_2TEXT.get_rect(center=(530, 130))
        screen.blit(RULES_2TEXT, RULES_2RECT)

        RULES_3TEXT = getFont(20).render("- Identify and fix bugs to improve system performance", True, "Black")
        RULES_3RECT = RULES_3TEXT.get_rect(center=(570, 160))
        screen.blit(RULES_3TEXT, RULES_3RECT)

        RULES_Tittle = getFont(50).render(" Yeoh Tzi Kian", True, "light blue")
        RULES_TRect = RULES_Tittle.get_rect(center=(300, 235))
        screen.blit(RULES_Tittle, RULES_TRect)

        RULES_1TEXT = getFont(20).render("- Maze agent developer", True, "Black")
        RULES_1RECT = RULES_1TEXT.get_rect(center=(260, 295)) 
        screen.blit(RULES_1TEXT, RULES_1RECT)

        RULES_2TEXT = getFont(20).render("- Design maze agent's structure", True, "Black")
        RULES_2RECT = RULES_2TEXT.get_rect(center=(350, 325))
        screen.blit(RULES_2TEXT, RULES_2RECT)

        RULES_3TEXT = getFont(20).render("- Optimize agent's performance to handle maze patterns", True, "Black")
        RULES_3RECT = RULES_3TEXT.get_rect(center=(580, 355))
        screen.blit(RULES_3TEXT, RULES_3RECT)

        RULES_Tittle = getFont(50).render(" Lee Jun Wen", True, "light blue")
        RULES_TRect = RULES_Tittle.get_rect(center=(250, 430))
        screen.blit(RULES_Tittle, RULES_TRect)

        RULES_1TEXT = getFont(20).render("- Algorithm Researcher", True, "Black")
        RULES_1RECT = RULES_1TEXT.get_rect(center=(260, 490)) 
        screen.blit(RULES_1TEXT, RULES_1RECT)

        RULES_2TEXT = getFont(20).render("- Understand and identify potential algorithm for maze", True, "Black")
        RULES_2RECT = RULES_2TEXT.get_rect(center=(580, 520))
        screen.blit(RULES_2TEXT, RULES_2RECT)

        RULES_3TEXT = getFont(20).render("- Recommend and code for the suitable algorithms for project", True, "Black")
        RULES_3RECT = RULES_3TEXT.get_rect(center=(640, 550))
        screen.blit(RULES_3TEXT, RULES_3RECT)

        RULES_Tittle = getFont(50).render(" Yip Mun Jun", True, "light blue")
        RULES_TRect = RULES_Tittle.get_rect(center=(250, 625))
        screen.blit(RULES_Tittle, RULES_TRect)

        RULES_1TEXT = getFont(20).render("- Algorithm Researcher", True, "Black")
        RULES_1RECT = RULES_1TEXT.get_rect(center=(260,685)) 
        screen.blit(RULES_1TEXT, RULES_1RECT)

        RULES_2TEXT = getFont(20).render("- Analyse on recommended algorithm for maze solving", True, "Black")
        RULES_2RECT = RULES_2TEXT.get_rect(center=(550,715))
        screen.blit(RULES_2TEXT, RULES_2RECT)

        RULES_3TEXT = getFont(20).render("- Provide a comparative of the selected algorithms and code", True, "Black")
        RULES_3RECT = RULES_3TEXT.get_rect(center=(630, 745))
        screen.blit(RULES_3TEXT, RULES_3RECT)

        CREDITS_BACK = Button(None, (1170, 25), "BACK", getFont(30), "Black", "Green")

        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    mainMenu()
        
        pygame.display.update()

def guide():
    def page2():
        page2_run = True
        
        while page2_run == True:
            clock.tick(144)
            GUIDES_MOUSE_POS = pygame.mouse.get_pos()
            guideBackground2 = pygame.image.load(r"assets\GuideBackground2.png")
            
            screen.blit(guideBackground2,(0,22))

            GUIDES_NEXT = Button(None,(1000,750),"-->",getFont(75),"White","Dark Green")
            GUIDES_NEXT.changeColor(GUIDES_MOUSE_POS)
            GUIDES_NEXT.update(screen)
            GUIDES_PREVIOUS = Button(None,(280,750),'<--',getFont(75),"White","Dark Green")
            GUIDES_PREVIOUS.changeColor(GUIDES_MOUSE_POS)
            GUIDES_PREVIOUS.update(screen)
            GUIDES_BACK = Button(None,(640, 750), "MENU", getFont(75), "White", "Dark Green")
            GUIDES_BACK.changeColor(GUIDES_MOUSE_POS)
            GUIDES_BACK.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if GUIDES_BACK.checkForInput(GUIDES_MOUSE_POS):
                            mainMenu()
                        if GUIDES_PREVIOUS.checkForInput(GUIDES_MOUSE_POS):
                            guide()
                        if GUIDES_NEXT.checkForInput(GUIDES_MOUSE_POS):
                            page3()
            pygame.display.update()
            
    guides_run = True

    def page3():
        page3_run = True
        
        while page2_run == True:
            clock.tick(144)
            GUIDES_MOUSE_POS = pygame.mouse.get_pos()
            guideBackground3 = pygame.image.load(r"assets\GuideBackground3.png")
            
            screen.blit(guideBackground3,(0,22))

            GUIDES_PREVIOUS = Button(None,(280,750),'<--',getFont(75),"White","Dark Green")
            GUIDES_PREVIOUS.changeColor(GUIDES_MOUSE_POS)
            GUIDES_PREVIOUS.update(screen)
            GUIDES_BACK = Button(None,(640, 750), "MENU", getFont(75), "White", "Dark Green")
            GUIDES_BACK.changeColor(GUIDES_MOUSE_POS)
            GUIDES_BACK.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if GUIDES_BACK.checkForInput(GUIDES_MOUSE_POS):
                            page2()
                        if GUIDES_NEXT.checkForInput(GUIDES_MOUSE_POS):
                            page4()
            pygame.display.update()
            
    guides_run = True
    
    while guides_run == True:
        clock.tick(60)
        GUIDES_MOUSE_POS = pygame.mouse.get_pos()

        guideBackground1 = pygame.image.load(r"assets\GuideBackground1.png")
    
        screen.blit(guideBackground1,(0,22))

        GUIDES_NEXT = Button(None,(1000,750),"-->",getFont(75),"White","Dark Green")
        GUIDES_NEXT.changeColor(GUIDES_MOUSE_POS)
        GUIDES_NEXT.update(screen)
        GUIDES_BACK = Button(None,(640, 750), "MENU", getFont(75), "White", "Dark Green")
        GUIDES_BACK.changeColor(GUIDES_MOUSE_POS)
        GUIDES_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if GUIDES_BACK.checkForInput(GUIDES_MOUSE_POS):
                        mainMenu()
                        
                    if GUIDES_NEXT.checkForInput(GUIDES_MOUSE_POS):
                        page2()
        
        pygame.display.update()

def mainMenu():
    mainMenu_run = True

    while mainMenu_run == True:
        clock.tick(60)
        screen.blit(background, (0,0))

        MENU_MOUSE_POSITION = pygame.mouse.get_pos()
        MENU_TEXT = getFont(100).render("ALGO MAZE", True, "#b68f40")

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        button_image = pygame.image.load(r"assets\button_clear.png")
        BUTTON_IMAGE = pygame.transform.scale(button_image, (600,120))

        START_BUTTON = Button(BUTTON_IMAGE, (640, 280), "START", getFont(69), "#d7fcd4", "White")
        GUIDE_BUTTON = Button(BUTTON_IMAGE, (640, 430), "GUIDES", getFont(69), "#d7fcd4", "White")
        CREDIT_BUTTON = Button(BUTTON_IMAGE, (640, 580), "CREDITS", getFont(69), "#d7fcd4", "White")
        QUIT_BUTTON = Button(BUTTON_IMAGE, (640, 730), "QUIT", getFont(69), "#d7fcd4", "White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [START_BUTTON, GUIDE_BUTTON, CREDIT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POSITION)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if START_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                        start()
                    
                    if GUIDE_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                        guide()

                    if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                        credit()

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                        pygame.quit()
                        sys.exit()
    
        pygame.display.update()

mainMenu()
