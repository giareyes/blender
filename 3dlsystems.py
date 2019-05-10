import bpy
import math
import pdb
import numpy as np

from mathutils import Vector

#apply rules
def apply_rules(command, rules, repeat):
    newcommand =""
    for i in range(0,repeat):
        for char in command:
            if char in rules.keys():
                newcommand+= rules[char]
            else:
                newcommand+=char
        command = newcommand
        newcommand = ""
    return command

#create the curves that will be turned into our plant
def make_curves(command, theta, length, start_coord):
    #3d matrix [H, L, U]
    h = [0, 0, 1]
    l = [1, 0, 0]
    u = [0, 1, 0]

    direction = [[h[0], l[0], u[0]],
                 [h[1], l[1], u[1]],
                 [h[2], l[2], u[2]]]
    curves = []
    plantStack = []
    coords = [start_coord]
    current_coord = start_coord
    for char in command:
        #draw in heading direction
        if char == 'F':
            index = len(coords)
            coords.append([current_coord[0] + length*h[0], current_coord[1] + length*h[1], current_coord[2] + length*h[2]])
            current_coord = coords[index]
        #turn left by theta
        elif char == '+':
            radians = math.radians(theta)
            rotation = [[math.cos(radians), math.sin(radians), 0],
                        [-1*math.sin(radians), math.cos(radians), 0],
                        [0, 0, 1]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #turn right by theta
        elif char == '-':
            radians = math.radians(-1*theta)
            rotation = [[math.cos(radians), math.sin(radians), 0],
                        [-1*math.sin(radians), math.cos(radians), 0],
                        [0, 0, 1]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #pitch down by theta
        elif char == '&':
            radians = math.radians(theta)
            rotation = [[math.cos(radians), 0, -1*math.sin(radians)],
                        [0, 1, 0],
                        [math.sin(radians), 0, math.cos(radians)]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #pitch up by theta
        elif char == '^':
            radians = math.radians(-1*theta)
            rotation = [[math.cos(radians), 0, -1*math.sin(radians)],
                        [0, 1, 0],
                        [math.sin(radians), 0, math.cos(radians)]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #roll left by theta
        elif char == '<':
            radians = math.radians(theta)
            rotation = [[1, 0, 0],
                        [0, math.cos(radians), -1*math.sin(radians)],
                        [0, math.sin(radians), math.cos(radians)]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #roll right by theta
        elif char == '>':
            radians = math.radians(-1*theta)
            rotation = [[1, 0, 0],
                        [0, math.cos(radians), -1*math.sin(radians)],
                        [0, math.sin(radians), math.cos(radians)]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        #turn around by 180 degrees
        elif char == "|":
            radians = math.pi
            rotation = [[math.cos(radians), math.sin(radians), 0],
                        [-1*math.sin(radians), math.cos(radians), 0],
                        [0, 0, 1]]
            mx = np.array(direction)
            my = np.array(rotation)
            direction = np.matmul(mx,my)
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
        elif char == '[':
            plantStack.append([current_coord, direction])
        elif char == ']':
            current = plantStack.pop()
            curves.append(coords)
            coords = [current[0]]
            direction = current[1]
            h = [direction[0][0], direction[1][0], direction[2][0]]
            l = [direction[0][1], direction[1][1], direction[2][1]]
            u = [direction[0][2], direction[1][2], direction[2][2]]
            current_coord = current[0]
        else:
            continue

    if len(coords) > 1:
        curves.append(coords)

    return curves

#create out plant object
def create_plant(curves, name):
    i = 0
    obs = []

    # create the Curve Datablock
    for coords in curves:
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2

        # map coords to spline
        polyline = curveData.splines.new('POLY')
        polyline.points.add(len(coords)-1)
        for i, coord in enumerate(coords):
            x,y,z = coord
            polyline.points[i].co = (x, y, z, 1)

        # create Object
        curveOB = bpy.data.objects.new(name + str(i), curveData)
        curveData.bevel_depth = 0.01

        i = i + 1

        # attach to scene and validate context
        scn = bpy.context.scene
        scn.objects.link(curveOB)
        scn.objects.active = curveOB
        obs.append(curveOB)

    #combine all the curves into one plant object
    ctx = bpy.context.copy()
    ctx['active_object'] = obs[0]
    ctx['selected_objects'] = obs
    ctx['selected_editable_bases'] = [scn.object_bases[ob.name] for ob in obs]
    bpy.ops.object.join(ctx)

def draw_plant(command, rules, repeat, angle, length, start_pos, name):
    curves = []
    command = apply_rules(command, rules, repeat)
    curves = make_curves(command, angle, length, start_pos)
    create_plant(curves, name)
    
#input data
length = 0.05

#---------this code below creates the small brown tree in trees.blend----------------
#command = "F"
#repeat = 3
#rules = {'F': "F[+F]F[-F]F"}

#bpy.context.scene.objects.active = None
#draw_plant(command, rules, repeat, 25.7, length, [0, 0, 0], "plant")
#------------------------------------------------------------------------------------

#---------this code below creates the big green tree in trees.blend------------------
#command2 = "F"
#repeat = 4
#rules = {'F':"FF-[-F+F+F]+[+F-F-F]&[&F^F^F]^[^F&F&F]"}

#bpy.context.scene.objects.active = None
#draw_plant(command2, rules, repeat, 22.5, length, [0, 0, 0], "plant2")
#------------------------------------------------------------------------------------

#---------this code below creates the small red tree in trees.blend------------------
#command3 = "F"
#repeat = 5
#rules = {'F':"F[-XF[&&&A]]X[+F[^^^A]]", 'X':"F[F[+++A]][^F[---A]]"}

#bpy.context.scene.objects.active = None
#draw_plant(command3, rules, repeat, 25, length, [2, 2, 0], "plant3")
#------------------------------------------------------------------------------------

#the two below are the plants that were created for the living room scene
command4 = "A"
curves4 = []
repeat = 6
length4 = 0.05
rules = {'A':">>>BY>>>BYA",
        'B':"[&Y[+L][-L]YBF]",
        'L': "FF+X-X-X+|+X-X",
        'X': "gX",
        'Y': "FY"}

bpy.context.scene.objects.active = None

#draw_plant(command4, rules, repeat, 22.5, length4, [-4.41422, -3.25387, 0.795179], "plant1")

command5 = "A"
curves5 = []
repeat = 6
length5 = 0.05
rules = {'A':">>>BY>>>BYA",
        'B':"[&Y[+L][-L]YBF]",
        'L': "FF+X-X-X+|+X-X",
        'X': "gX",
        'Y': "FY"}

bpy.context.scene.objects.active = None

#use our functions to create our plants

#draw_plant(command5, rules, repeat, 22.5, length5, [-4.41422, 3.15531, 0.795179], "plant2")
