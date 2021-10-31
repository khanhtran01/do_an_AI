from typing import List, Tuple
import numpy as np
from numpy.core.numeric import argwhere
from numpy.lib.twodim_base import triu_indices_from
import pygame
import sys
from queue import PriorityQueue
import time
from pygame import display

BLACK = (1,1,1)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PINK = (255,51,255)
YELLOW = (255,255,0)
WHITE = (254,254,254)
GREY = (160,160,160)


class Point:
        def __init__(self,pos,piority=-1,parent=None,step :int = 0) -> None:
            self.pos = pos
            self.piority = piority
            self.parent = parent
            self.step = step
        def __str__(self) -> str:
            return "x: {0}, y: {1}".format(self.pos[0],self.pos[1])

        def __eq__(self, o: object) -> bool:
            return self.pos == o
        def update_piority(self, h):
            self.piority = self.piority + h


def transfer(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n', '') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ':
                layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == '#':
                layout[irow][icol] = -2  # wall
            elif layout[irow][icol] == '&':
                layout[irow][icol] = 1  # player
            elif layout[irow][icol] == '.':
                layout[irow][icol] = -1  # goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)])
    return np.array(layout)

def readCommand(argv):
    """đọc map từ command line"""
    layout = []
    f = open("map/"+ str(argv[0]) , "r")
    for i in f:
        layout.append(i)
    return layout

def getDestination(gameMap):
    """Lấy vị trí của điểm đích"""
    return tuple(np.argwhere(gameMap==-1)[0])

def getWall(gameMap):
    """Lấy danh sách các vị trí của tường trong map"""
    return tuple(tuple(i) for i in np.argwhere(gameMap == -2))

def getStartPoint(gameMap):
    """Lấy vị trí của điểm xuất phát"""
    return tuple(np.argwhere(gameMap==1)[0])

def step(point : Point):
    return point.step + 1

def check_wall(action, visited):
    """kiểm tra vị trí có tồn tại trong visited hay trùng với tường hay không"""
    if action not in walls + tuple(visited):
        return True
    else:
        return False

def action(posplayer, visited):
    """Trả về các bước đi hợp lệ"""
    allAction = [[-1,0],[1,0],[0,-1],[0,1]]
    convert = list(posplayer)
    list_action = []
    for action in allAction:
        xNew, yNew = convert[0] + action[0] , convert[1] + action[1]
        if yNew < 0:
            continue

        if check_wall(tuple((xNew,yNew)), visited):
            list_action.append(tuple((xNew,yNew)))
    return list_action
        
def h(point):
    """Tính khoảng cách từ điểm hiện tại đến điểm đích"""
    return abs(point[0] - getdespoint[0]) + abs(point[1] - getdespoint[1])

def h2(point):
    """Tính khoảng cách từ điểm xuất phát điểm điểm hiện tại"""
    return abs(point[0] - getstartPoint[0]) + abs(point[1] - getstartPoint[1])

def draw_color(screen,point,color,size):
    """Tô màu cho ô vuông"""
    pygame.draw.rect(screen,color,(point[1] * size,point[0] * size, size, size))

def draw_button(screen, point, color):
    """Vẽ button"""
    pygame.draw.rect(screen,color, (point[0], point[1],80,20))

def bfs(gameMap,screen,clock):
    """Thực thi BFS"""
    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)

    visited = []
    opended = []

    opended.append(startPoint)

    while len(opended) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        visit_point = opended.pop(0)
        # kiểm tra vị trí hiện tại có phải là vị trí đích hay chưa
        if visit_point == desPoint:
            return visit_point
        #kiểm tra vị trí hiện tại đã đi qua hay chưa
        if visit_point not in visited:
            visited.append(visit_point)

            # Lấy danh sách các bước đi hợp lệ
            actions = action(visit_point.pos,visited)

            for neighbor in actions:
                newPos = Point (neighbor,-1,visit_point)
                opended.append(newPos)
                # Tô màu cho những node con
                draw_color(screen,neighbor,PINK,32)
        
            draw_color(screen,visit_point.pos,YELLOW,32)
            clock.tick(60)
            pygame.display.update()


def dfs(gameMap,screen,clock):
    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)

    visited = []
    opended = []

    opended.append(startPoint)
    while len(opended) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        visit_point = opended.pop()

        if visit_point == desPoint:
            return visit_point
        
        if visit_point not in visited:
            visited.append(visit_point)

            actions = action(visit_point.pos,visited)

            for neighbor in actions:
                newPos = Point (neighbor,-1,visit_point)
                opended.append(newPos)
                draw_color(screen,neighbor,PINK,32)
            draw_color(screen,visit_point.pos,YELLOW,32)
            clock.tick(60)
            pygame.display.update()

def astar(gameMap,screen,clock):
    # count dùng để phân biệt 2 node con có piority bằng nhau
    # node nào được tìm thấy trước sẽ có giá trị nhỏ hơn
    count = 0

    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)

    visited = []
    pioQueue = PriorityQueue()
    # bỏ điểm xuất phát vào piority queue
    pioQueue.put((startPoint.piority,count,startPoint))
    
    while not pioQueue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # lấy node đầu của pioQueue (node có piority thấp nhất)
        # nếu piority bằng nhau -> node có count thấp nhất
        visit_point = pioQueue.get()[2]

        #kiểm tra điểm hiện tại có phải là điểm đích
        if visit_point == desPoint:
            return visit_point
        
        # Kiểm tra trong visited
        if visit_point not in visited:
            visited.append(visit_point)

            # cập nhật số bước đã đi
            newStep = step(visit_point)

            actions = action(visit_point.pos, visited)
            for neighbor in actions:
                count += 1

                # node con có piority = số step + khoảng cách đến đích
                newPos = Point(neighbor,h(neighbor) + newStep,visit_point,newStep)

                # đặt node con vào trong piority queue
                pioQueue.put((newPos.piority,count,newPos))
                # tô màu cho node con
                draw_color(screen,neighbor,PINK,32)
            
            # tô màu cho node đã đi qua
            draw_color(screen,visit_point.pos,YELLOW,32)
            clock.tick(60)
            pygame.display.update()

def greedy(gameMap,screen,clock):
    """Hiện thực greedy"""
    # Cách làm tương tự A*
    count = 0
    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)

    visited = []
    pioQueue = PriorityQueue()
    pioQueue.put((startPoint.piority,count,startPoint))
    while not pioQueue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        visit_point = pioQueue.get()[2]
        if visit_point == desPoint:
            return visit_point
        if visit_point not in visited:
            visited.append(visit_point)
            newStep = 0
            actions = action(visit_point.pos, visited)
            for neighbor in actions:
                count += 1
                newPos = Point(neighbor,h(neighbor) + newStep,visit_point,newStep)
                pioQueue.put((newPos.piority,count,newPos))
                draw_color(screen,neighbor,PINK,32)
                
            draw_color(screen,visit_point.pos,YELLOW,32)
            clock.tick(60)
            pygame.display.update()

def checkEndState(point1, visit1, point2, visit2):
    """kiểm tra điểm point1 có nằm trong những điểm point 2 đã thấy hay chưa và ngược lại"""
    if point1 in visit2:
        return True
    if point2 in visit1:
        return True
    
    return False


def bidirectional(gameMap,screen,clock):
    """Hiện thực bidirectional với A*"""

    # Đẩy 2 điểm xuất phát và piority queue
    count = 0
    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)
    
    visited = []
    visited2 = []

    pioQueue = PriorityQueue()
    pioQueue2 = PriorityQueue()

    pioQueue.put((startPoint.piority,count,startPoint))
    pioQueue2.put((desPoint.piority,count,desPoint))

    while not pioQueue.empty() and not pioQueue2.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        visit_point = pioQueue.get()[2]
        visit_point2 = pioQueue2.get()[2]

        # Kiểm tra điểm thứ nhất đã đi qua vùng quét của điểm thứ 2 và ngược lại
        if visit_point == visit_point2 or checkEndState(visit_point,visited,visit_point2,visited2):
            if visit_point == visit_point2:
                return visit_point,visit_point2
            elif visit_point in visited2:
                return visit_point, visited2[visited2.index(visit_point)]
            elif visit_point2 in visited:
                return visited[visited.index(visit_point2)], visit_point2
        
        # Đẩy các node con của điểm thứ nhất và queue
        if visit_point not in visited:
            visited.append(visit_point)
            newStep = step(visit_point)
            actions = action(visit_point.pos, visited)
            for neighbor in actions:
                count += 1
                newPos = Point(neighbor,h(neighbor) + newStep,visit_point,newStep)
                pioQueue.put((newPos.piority,count,newPos))
                draw_color(screen,neighbor,PINK,32)
        
        # Đẩy các node con của điểm thứ 2 vào queue
        if visit_point2 not in visited2:
            visited2.append(visit_point2)
            newStep = step(visit_point2)
            actions = action(visit_point2.pos, visited2)
            for neighbor in actions:
                count += 1
                newPos = Point(neighbor,h2(neighbor) + newStep,visit_point2,newStep)
                pioQueue2.put((newPos.piority,count,newPos))
                draw_color(screen,neighbor,PINK,32)   
            
            # Vẽ màu cho 2 điểm đã đi qua
            draw_color(screen,visit_point.pos,YELLOW,32)
            draw_color(screen,visit_point2.pos,YELLOW,32)
            clock.tick(60)
            pygame.display.update()

def getpath_nonRecur(finalnode:Point,screen,clock):
    temp = finalnode
    length = 0
    while temp != None:
        length +=1
        draw_color(screen,temp.pos,BLUE,32)
        temp = temp.parent
        clock.tick(60)
        pygame.display.update()
    return length
        

def getpath2(finalnode1:Point,finalnode2:Point,screen,clock):
    if finalnode1.parent != None and finalnode2.parent != None:
        getpath2(finalnode1.parent,finalnode2.parent,screen,clock)
    elif finalnode1.parent != None:
        getpath2(finalnode1.parent,finalnode2,screen,clock)
    elif finalnode2.parent != None:
        getpath2(finalnode1,finalnode2.parent,screen,clock)
    draw_color(screen,finalnode1.pos,BLUE,32)
    draw_color(screen,finalnode2.pos,BLUE,32)
    clock.tick(60)
    pygame.display.update()

def getpath2_update(start:Point,des:Point,screen,clock):
    length = 0
    finalnode1 = start
    finalnode2 = des
    while finalnode1 != None or finalnode2 != None:
        if finalnode1 != None:
            draw_color(screen,finalnode1.pos,BLUE,32)
        if finalnode2 != None:
            draw_color(screen,finalnode2.pos,BLUE,32)
        clock.tick(60)
        pygame.display.update()
        if finalnode1 != None and finalnode2 != None:
            length +=2
            finalnode1 = finalnode1.parent
            finalnode2 = finalnode2.parent
        elif finalnode1 != None and finalnode2 == None:
            length += 1
            finalnode1 = finalnode1.parent
        elif finalnode2 != None and finalnode1 == None:
            length += 1
            finalnode2 = finalnode2.parent
    return length



def draw_text(screen,font,point,color,data):
    text = font.render(data, True, color)
    screen.blit(text,(point))

def pause(reset_pos):
    paused = True
    while paused:
        mouse_pos = pygame.mouse.get_pos()    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (reset_pos[0] <= mouse_pos[0] <= reset_pos[0] + 80) and (reset_pos[1] <= mouse_pos[1] <= reset_pos[1] + 20):
                    if event.button == 1:
                        paused = False
    
def runwithpygame():
    pygame.init()
    startPoint = Point(getstartPoint)
    desPoint = Point(getdespoint)

   
    maxwidth = 0
    maxheight = 0
    for wall in walls:
        if wall[0] > maxheight:
            maxheight = wall[0]
        if wall[1] > maxwidth:
            maxwidth = wall[1]
    font = pygame.font.Font('freesansbold.ttf', 14)
    btn_font = pygame.font.Font('freesansbold.ttf', 12)
    
    icon = pygame.image.load("maze.png")
    
    maxwidth += 5
    game_over = 0

    fixed_size = 32
    maxwidth *= fixed_size
    maxheight *= fixed_size
    maxheight += fixed_size

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((maxwidth, maxheight ))
    pygame.display.set_icon (icon)
    pygame.display.set_caption("MAZE")

# ----------------------------- some mode and status --------------------------
    mode = 0
    mouseClicking = False
    path = []
    runtime = 0
    paused = False

    btn_first_height = 40
    base_width = maxwidth-4*fixed_size
    btn_space = 90
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClicking = True
        mouse_pos = pygame.mouse.get_pos()    
        screen.fill((0,0,0))
# -------------------------- draw button ---------------------------------------
        list_btn = ["ASTAR","BIDIRECTION", "GREEDY","BFS"]
        i = 0
        for btn in list_btn:
            draw_button(screen,[base_width + 24,btn_first_height  + btn_space*i],RED)
            draw_text(screen,font,[base_width + fixed_size,btn_first_height  + btn_space*i-25], WHITE,btn)
            draw_text(screen,btn_font,[base_width +45,btn_first_height  + btn_space*i + 5],WHITE,"START")
            draw_text(screen,btn_font,[base_width,btn_first_height  + btn_space*i + 22],WHITE,"runtime :")
            draw_text(screen,btn_font,[base_width,btn_first_height  + btn_space*i + 44],WHITE,"length :")
            i += 1
        draw_button(screen,[base_width + 24,btn_first_height  + btn_space*i],RED)
        draw_text(screen,btn_font,[base_width +45,btn_first_height  + btn_space*i + 5],WHITE,"RESET")
        reset_pos = [base_width + 24,btn_first_height  + btn_space*i]
# ------------------------- draw background -------------------------
        pygame.draw.rect(screen,WHITE ,(0,0,maxwidth - 5 * fixed_size,maxheight))
        draw_color(screen,startPoint.pos,GREEN,fixed_size)
        draw_color(screen,desPoint.pos,RED,fixed_size)
        for wall in walls:
            draw_color(screen,wall,GREY,fixed_size)
        
        
        if base_width + 24 <= mouse_pos[0] <= base_width + 24 + 80 and (40 <=mouse_pos[1] <= 60) and mouseClicking ==True:
            mode = 1
        elif base_width + 24 <= mouse_pos[0] <= base_width + 24 + 80 and (40 + btn_space <=mouse_pos[1] <= 60 + btn_space) and mouseClicking == True:
            mode = 2
        elif base_width + 24 <= mouse_pos[0] <= base_width + 24 + 80 and (40 + btn_space * 2 <=mouse_pos[1] <= 60 + btn_space * 2) and mouseClicking == True:
            mode = 3
        elif base_width + 24 <= mouse_pos[0] <= base_width + 24 + 80 and (40 + btn_space * 3 <=mouse_pos[1] <= 60 + btn_space * 3) and mouseClicking == True:
            mode = 4
# ------------------------------------------------        
        if mode != 0:
            timestart = time.time()
            length = 0
            if mode == 1:
                finalnode = astar(gameMap,screen,clock)
            elif mode == 2:
                finalnode1,finalnode2 = bidirectional(gameMap,screen,clock)
            elif mode == 3:
                finalnode = greedy(gameMap,screen,clock)
            elif mode == 4:
                finalnode = bfs(gameMap,screen,clock)
            timeend = time.time()
            if mode != 2:
                length = getpath_nonRecur(finalnode,screen,clock)
            else:
                length = getpath2_update(finalnode1,finalnode2,screen,clock) - 1 # vì có 1 node trùng từ 2 phía
            
            runtime = timeend - timestart
            # print(runtime)
            draw_text(screen,btn_font,[base_width,btn_first_height + 22 + (mode-1) * btn_space],WHITE,"runtime : " + str (runtime) )
            draw_text(screen,btn_font,[base_width,btn_first_height + 44 + (mode-1) * btn_space],WHITE,"length : " + str (length) )
            paused = True    
        
# ------------------------- set default mode and status ------------
        mode = 0
        mouseClicking = False
        clock.tick(60)
        pygame.display.update()
        if paused == True:
            pause(reset_pos)
            paused =False


if __name__ =='__main__':
    layout = readCommand(sys.argv[1:])
    gameMap = transfer(layout)
    walls = getWall(gameMap)
    getdespoint = getDestination(gameMap)
    getstartPoint = getStartPoint(gameMap)
    runwithpygame()
