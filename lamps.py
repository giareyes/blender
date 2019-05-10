import bpy

def lampshade(height, width, invert, init_pos):
    my_curve = bpy.data.curves.new("lampshade", "CURVE")
    my_curve.dimensions = "3D"

    points = []
    flat = []

    if not invert:
        for i in range(0, 4):
            points.append([(0.2 * i * i - i + 2 + width) * (width/ 4), 0, i *(height / 4)])
    else:
        for i in range(4, 0, -1):
            points.append([(0.2 * i * i - i + 2 + width) * (width/ 4), 0, i *(height / 4)])
        points.append([0,0,0])

    for point in points:
        flat.append(point[0])
        flat.append(point[1])
        flat.append(point[2])

    s = my_curve.splines.new('BEZIER')
    s.bezier_points.add(len(points)-1)
    s.bezier_points.foreach_set("co", flat)

    for bp in s.bezier_points:
        bp.handle_left_type = bp.handle_right_type = "AUTO"

    bpy.ops.curve.primitive_bezier_curve_add()
    ob = bpy.context.object
    ob.data = my_curve
    if not invert:
        ob.name = "lampShade"
    else:
        ob.name = "vase"

    screw = ob.modifiers.new("Screw", "SCREW")

    ob.location = init_pos

    return ob


def lampstand(height, init_pos):
    my_curve = bpy.data.curves.new("lampstand", "CURVE")
    my_curve.dimensions = "3D"

    points = []
    flat = []

    points.append([-0.55 *(height/2), 0, 0])
    points.append([-0.55*(height/2), 0, 0.3])
    points.append([-0.3*(height/2) , 0, 0.315625])
    points.append([-0.2*(height/2),0,1])

    if(height > 1):
        points.append([-0.1*(height/2),0,height])

    for point in points:
        flat.append(point[0])
        flat.append(point[1])
        flat.append(point[2])

    s = my_curve.splines.new('BEZIER')
    s.bezier_points.add(len(points)-1)
    s.bezier_points.foreach_set("co", flat)

    for bp in s.bezier_points:
        bp.handle_left_type = bp.handle_right_type = "AUTO"

    bpy.ops.curve.primitive_bezier_curve_add()
    ob = bpy.context.object
    ob.data = my_curve
    ob.name = "lampStand"

    screw = ob.modifiers.new("Screw", "SCREW")
    ob.location = init_pos

    return ob



def makeLamp(vase, heightStand, heightShade, widthShade, pos):
    if vase:
         lampshade(heightShade, widthShade, True, pos)
    else:
        lampstand(heightStand, pos)
        lampshade(heightShade, widthShade, False, [pos[0],pos[1], pos[2] + heightStand])


#makeLamp(False, 1, 0.5, 0.75, [1.24742, 2.94902, 1])
#makeLamp(True, 1, 0.75, 0.75, [-4.41422,-3.25387,0])

makeLamp(True, 1, 1, 0.75, [-4.41422, 3.15531,0])
