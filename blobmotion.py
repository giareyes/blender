import bpy
import math

gia = bpy.data.objects['blobG']
max = bpy.data.objects['blobM']
matt = bpy.data.objects['blobMT']

mtlocation = [-0.26092, 2.53292, 0.24071]
glocation = [0.667523, 0.538576,0.904583]
mlocation = [0.667523, -0.777913,0.904583]
mtend = []
matt.location = mtlocation
gia.location = glocation
max.location =  mlocation
gia.rotation_euler = (0,0,0)
max.rotation_euler = (0,0, math.radians(-180))


frame_num = 10

for i in range(100):
    bpy.context.scene.frame_set(frame_num)
    x1 = mtlocation[0] - (i*3.5)/100
    z1 = mtlocation[2] + abs(math.sin(i*(365/100)*math.pi/180))
    
    
    matt.location = (x1, matt.location[1], z1)
    matt.keyframe_insert(data_path="location", index = -1)
    
    z2 = glocation[2] + abs(math.sin((i*360/100)*math.pi/180))
    z3 = mlocation[2] + abs(math.cos((i*360/100)*math.pi/180))
    
    
    gia.location = (gia.location[0], gia.location[1], z2)
    gia.keyframe_insert(data_path="location", index = -1)
    
    max.location = (max.location[0], max.location[1], z3)
    max.keyframe_insert(data_path="location", index = -1)
    
    frame_num += 1 
    
mtend = matt.location

for i in range(50):
    bpy.context.scene.frame_set(frame_num)
    z1 = mtend[2] + abs(math.sin((i*360/100)*math.pi/180))
    
    matt.location = (matt.location[0], matt.location[1], z1)
    matt.keyframe_insert(data_path="location", index = -1)
    
    frame_num += 1

frame_num = 120

for i in range(20):
    bpy.context.scene.frame_set(frame_num)
    rotation = 2.5*math.pi/180
    gia.rotation_euler = (gia.rotation_euler[0], gia.rotation_euler[1], gia.rotation_euler[2] - 2*rotation)
    max.rotation_euler = (max.rotation_euler[0], max.rotation_euler[1], max.rotation_euler[2] + rotation)
    gia.keyframe_insert("rotation_euler", index = 2, frame = frame_num)
    
    
    max.location = (max.location[0], max.location[1], z3)
    max.keyframe_insert("rotation_euler", index = 2, frame = frame_num)
    
    frame_num += 1 

    
frame_num = 110
i = 0
while max.location[2] > mlocation[2]:
    z3 = mlocation[2] + abs(math.cos((i*360/100)*math.pi/180))
    max.location = (max.location[0], max.location[1], z3)
    max.keyframe_insert(data_path="location", index = -1)
    i+= 1
    frame_num+= 1
    