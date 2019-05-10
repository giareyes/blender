import bpy
import bmesh
import math
import random
    

def animate_fire(init_pos, lifetime, bounds, objs, life_lim, velocity, mean_trans, frames):
    frame_num = 0

    for i in range(0, frames, 5):
        j=0
        for obj in objs:
            bpy.context.scene.frame_set(frame_num)
            lifetime[j] -=1
            x = init_pos[j][0] + velocity[0]*random.uniform(-1,1)
            y = init_pos[j][1] + velocity[1]*random.uniform(-1,1)
            z = init_pos[j][2] + velocity[2]*random.random()
            obj.location = (x, y, z)
            
            if lifetime[j] > 4 and obj.material_slots[0].material.alpha < mean_trans - 0.1:
                obj.material_slots[0].material.alpha += (0.2 * random.random())
                
            if lifetime[j] < 5:
                obj.material_slots[0].material.alpha -= 0.1
            
            if x > bounds[0][1] or x < bounds[0][0] or y > bounds[1][1] or y < bounds[1][0] or z > bounds[2][1] or z < bounds[2][0] or lifetime[j] == 0:
                x = random.uniform(bounds[0][0], bounds[0][1])
                y = random.uniform(bounds[1][0], bounds[1][1])
                z = 0
                lifetime[j] = random.randint(1,life_lim)
                obj.material_slots[0].material.alpha = 0.2
            
            init_pos[j] = [x,y,z]
            obj.keyframe_insert(data_path="location", index = -1)
            j = j + 1
            
        frame_num += 5 

def create_fire(location, dimensions, nparticles, mean_color, md_color, mean_trans, md_trans, life_lim, velocity, frames):
    scene = bpy.context.scene

    # Create an empty mesh and the object.
    bpy.ops.mesh.primitive_cube_add()

    bound_box = bpy.context.active_object
    bound_box.dimensions = dimensions
    bound_box.location = location
    bound_box.name = "fire"
    bound_box.draw_type = "BOUNDS"
    bound_box.hide_render = True
    
    #we will use these bounds while animating
    bounds = [[location[0] - (dimensions[0]/2),location[0] + (dimensions[0]/2)], 
                [location[1] - (dimensions[1]/2), location[1] + (dimensions[1]/2)], 
                [location[2] - (dimensions[2]/2), location[2] + (dimensions[2]/2)]]
    
    init_pos = []
    lifetime = []
    
    objs = []
    for i in range(0, nparticles):
        mesh = bpy.data.meshes.new('particle' + str(i))
        basic_sphere = bpy.data.objects.new('particle' + str(i), mesh)

        # Add the object into the scene.
        scene.objects.link(basic_sphere)
        scene.objects.active = basic_sphere
        basic_sphere.select = True
        
        new_mat = bpy.data.materials.new("color" + str(i))
        new_mat.diffuse_color = (mean_color[0] + md_color[0]*random.uniform(-1,1), 
                                    mean_color[1] + md_color[1]*random.uniform(-1,1), 
                                    mean_color[2] + md_color[2]*random.uniform(-1,1)) 
        new_mat.type = "HALO"
        new_mat.alpha = mean_trans + md_trans*random.uniform(-1,1)
        new_mat.halo.hardness = 15
        new_mat.halo.size = 0.082 + 0.05*random.uniform(-1,1)
        new_mat.halo.add = 0.775
        new_mat.halo.use_texture = True 
        new_mat.halo.use_soft = True 
        bpy.ops.object.material_slot_add()
        bpy.context.object.material_slots[0].material = new_mat
        
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=1, v_segments=1, diameter=0.01)
        bm.to_mesh(mesh)
        bm.free()
        
        x = random.uniform(bounds[0][0], bounds[0][1])
        y = random.uniform(bounds[1][0], bounds[1][1])
        z = 0
        basic_sphere.location = [x,y,z]
        init_pos.append([x,y,z])
        lifetime.append(random.randint(1,life_lim))
        
        objs.append(basic_sphere)
        #bpy.ops.object.modifier_add(type='SUBSURF')
        #bpy.ops.object.shade_smooth()
        

    #taken from stack overflow (https://blender.stackexchange.com/questions/26108/how-do-i-parent-objects)
    for obj in objs:
        parent = bpy.data.objects.get("fire")
        if obj:
            obj.parent = parent
            if parent:
                obj.matrix_parent_inverse = parent.matrix_world.inverted()
    
    animate_fire(init_pos, lifetime, bounds, objs, life_lim, velocity, mean_trans, frames)
    



create_fire([-4.6839,-0.046422,0.55], [0.15,1.4,1.1], 200, [1.0, 0.15, 0], [0.0,0.13,0.0], 0.45, 0.1, 15, [0.1, 0.2, 0.3], 200)
