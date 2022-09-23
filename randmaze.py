#!/usr/local/bin/python3.7
# copyright 2022 by moshix
# v0.01 Humble beginnings
# v0.02 Make it do mazes
# v1.00 randomizer in wallFollower function
# v1.10 user input
# v1.11 Print size of paths
# v1.20 3 different maze rats
# v2.00 Multi=threading to print stats
# v2.10 Print way more stats
# v2.20 Fix stats 
# v2.21 Stats now in the window itself

try:
    from pyamaze import  maze,agent,COLOR,textLabel
except ImportError as e:
    print("******Error*******    - Please install the package pyamaze to run this proram.")
    print("Terminating now...")
    pass  # module doesn't exist, deal with it.

#from   pyamaze import maze,agent,COLOR,textLabel
import random
import threading
import time
import sys

def RCW():
    global direction
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=[v[-1]]+v[:-1]
    direction=dict(zip(k,v_rotated))

def RCCW():
    global direction
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=v[1:]+[v[0]]
    direction=dict(zip(k,v_rotated))

def moveForward(cell):
    if direction['forward']=='E':
        return (cell[0],cell[1]+1),'E'
    if direction['forward']=='W':
        return (cell[0],cell[1]-1),'W'
    if direction['forward']=='N':
        return (cell[0]-1,cell[1]),'N'
    if direction['forward']=='S':
        return (cell[0]+1,cell[1]),'S'

def wallFollower(m,focus):
    global direction
    # steps 1 is the counter for printStats
    global steps1
    global steps2
    steps1=0
    steps2=0

    direction={'forward':'N','left':'W','back':'S','right':'E'}
    currCell=(m.rows,m.cols)
    path=''
    while True:
        
        if currCell==(1,1):
            break

        k = random.randint(0, 10) 
        if m.maze_map[currCell][direction['forward']]==1 and k > focus:
              #print('Random k >7')
              currCell,d=moveForward(currCell)                                
              path+=d
              steps1=len(path)


        if m.maze_map[currCell][direction['left']]==0:
            if m.maze_map[currCell][direction['forward']]==0:
                #print('turn right but not forward')
                RCW()
            else:
                #print('move forward')
                currCell,d=moveForward(currCell)
                path+=d
                steps1=len(path)
        else:
              #print('go left and forward')
              RCCW()
              currCell,d=moveForward(currCell)
              path+=d
              steps1=len(path)

    path2=path
    steps2=len(path2)

    while 'EW' in path2 or 'WE' in path2 or 'NS' in path2 or 'SN' in path2:
        path2=path2.replace('EW','')
        path2=path2.replace('WE','')
        path2=path2.replace('NS','')
        path2=path2.replace('SN','')
        steps2=len(path2)
    return path,path2
        
# This is the third maze rat 
def wallFollower2(m,focus):
    global direction
    #steps2 is the counter for printStats
    global steps3
    d=0
    direction={'forward':'N','left':'W','back':'S','right':'E'}
    currCell=(m.rows,m.cols)
    path3=''
    while True:
        
        if currCell==(1,1):
            break

        k = random.randint(0, 10) 
        if m.maze_map[currCell][direction['forward']]==1 and k > focus:
              currCell,d=moveForward(currCell)                                
              path3+=d 
              steps3=len(path3)


        if m.maze_map[currCell][direction['left']]==0:
            if m.maze_map[currCell][direction['forward']]==0:
                #print('turn right but not forward')
                RCW()
            else:
                #print('move forward')
                currCell,d=moveForward(currCell)
                path3+=d
                steps3=len(path3)
        else:
              #print('go left and forward')
              RCCW()
              currCell,d=moveForward(currCell)
              path3+=d
              steps3=len(path3)



#    while 'EW' in path3 or 'WE' in path3 or 'NS' in path3 or 'SN' in path3:
#       path3=path3.replace('EW','')
#        path3=path3.replace('WE','')
#        path3=path3.replace('NS','')
#        path3=path3.replace('SN','')
    return path3

def printStats():
     global steps1
     global steps2
     global steps3
     steps3=0
     while True:
        time.sleep(3)       
       
        print('Stats update --  path1(red) elements',steps1,'  path2(green) elements: ',steps2,'  path3(yellow) elements: ',steps3)
        
        if finished == True:
            break
  


if __name__=='__main__':
    irow = input("How many rows x columns: ")
    val = input("How focus shall red be (6-9, higher number more focussed): ")
    valint = int(val)
    introws = int(irow)
    speedval = input("How fast should the rats run (20-80): ")
    speed = int(speedval)
    loopval = input("Percentage of loops in maze: ")
    loop = int(loopval)
    myMaze=maze(introws,introws+10)
    myMaze.CreateMaze(loopPercent=loop)
    
    steps3=0
    t1 = threading.Thread(target=printStats, args=())
    t1.start()
    
    finished=False
    a=agent(myMaze,filled=True,shape='square',footprints=True,color=COLOR.red)
    b=agent(myMaze,filled=True,shape='square',footprints=True,color=COLOR.green)
    c=agent(myMaze,filled=True,shape='square',footprints=True,color=COLOR.yellow)
    path,path2=wallFollower(myMaze,valint)
    path3=wallFollower2(myMaze,valint-1) #make maze rat 3 most confused one
    finished=True 
    myMaze.tracePath({a:path,b:path2,c:path3},delay=speed)
    arraylength=len(path)
    array2length=len(path2)
    array3length=len(path3)
    print('Final count -- path1(red) elements',arraylength,'  path2(green) elements: ',array2length,'  path3(yellow) elements: ',array3length)
    sizarray1=sys.getsizeof(path)
    sizarray2=sys.getsizeof(path2)
    sizarray3=sys.getsizeof(path3)
    totsize=int((sizarray1+sizarray2+sizarray3)/1024)
    #print('Memory used by: path1(red): ',sizarray1,' - path2(green): ',sizarray2,' - path3(yellow): ',sizarray3)
    #print('Percentage of loops in maze: ',loop,' - maze size: ',introws,'x',introws+10)
    #print('Total memory used in Kbit: ',totsize)
    ltstring = 'Number of elements for: path1: '+str(sizarray1)+' - path2(green): '+str(sizarray2)+' - path3(yellow): '+str(sizarray3)+'  -  Memory used in Kbit: '+str(totsize)
    l1=textLabel(myMaze,'Stats:',ltstring)
    
    #now execute the maze
    myMaze.run()