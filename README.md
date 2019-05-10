# Blender
Scripts written for CPSC 479: Advanced Computer Graphics. These scripts can be uploaded into Blender and used to procedurally create models and animations. I created these scripts for my final project to show that I understood these techniques well enough to implement them myself.

## Procedural Modeling:

### 3dlsystems.py
A script to create plants. This file has four functions: apply_rules() and make_curves(), create_plant(), and draw_plant(). The function draw_plant() takes in 7 arguments: 

1.	Command: this is the initial command before any rules are applied (for example, “F”). It is inputted as a string.
2.	Rules: a dictionary of all the rules we will apply to the initial command. It should be passed in the format {character: replacement}, where character is a char and replacement is a string.
3.	Repeat: the number of times we are going to apply rules to the command
4.	Angle: the angle at which the pitch, roll, and turn change per command
5.	Length: the length of each segment of plant drawn by a forward draw (F)
6.	Start_pos: where in the scene the plant will be drawn
7.	name: the name of the plant object

draw_plants() takes in these arguments and creates an empty list called “curves”. It then calls apply_rules(command, rules, repeat), which applies the rules repeat times to the initial command and returns the changed command. draw_plants() then calls make_curves(), which takes the new command, the angle, length, and starting position, and creates curves based on the application of the command. make_curves() returns a list of the curves it creates and stores it in the list “curves”. draw_plants() then calls create_plants(), which takes in curves and name. It combines all the separate curves into one object, then names this combined object the inputted name. 

As the name of the file implies, the plants created through this script are made through L-systems, a graphics technique we studed in class. The file contains my implementation of L-systems, though it lacks a few of the rules that many downloadable 3d L-system packages contain. 

### lamps.py:
A script to create lamps and vases. This file has three functions: lampshade(), lampstand(), and makeLamp(). makeLamp() takes in 5 parameters:

1.	vase: this is a Boolean value. Lampshade() can make either a lampshade or a vase, so if this is True, we will only call lampshade() and not lampstand().
2.	heightStand: the height of the lampstand. If vase is true, it doesn’t matter what value is here.
3.	heightShade: the height of the lampshade.
4.	widthShade: the width of the lampshade.
5.	pos: the position of the lamp/vase

makeLamp() takes these parameters and first checks is vase is true. If it’s true, it only calls lampshade(), sending in heightShade, widthShade, True, pos. lampshade() then draws a vase using sweeping. If vase is false, it creates a lampstand using heightStand at position pos. It then creates a lampshade, sending in the values heightShade, widthShade, False, [pos[0],pos[1], pos[2] + heightStand]. 

Both lampshade() and lampstand() use sweeping. While the heights and widths can be specified, the function used for the actual sweeping cannot be changed, as this would be too difficult to implement. However, even though this function does not change, it can create a wide variety of objects. 

## Procedural Animation:

### blobmotion.py:
A script assigning motion. This file assigns motion to the three (pre-made and pre-named) characters in a scene. It creates a loop in which it assigns new positions/rotations to each characters.

### fire_functions.py:
A script that creates an animated fire through particle systems. This file has two functions: create_fire() and animate_fire(). create_fire() makes a bounding box in the location the user specifies, and inside of this bounding box it creates spheres which act as particles. These “particles” have different attributes, some of which can be specified, and some which are hard coded, since this function already has many parameters. It takes in 10 parameters:

1.	location: the location of the bounding box. Pass in as an array
2.	dimensions: the dimensions of the bounding box. Pass in as an array
3.	nparticles: the number of particles drawn
4.	mean_color: the average color of the particles. Pass in as an [r,g,b] array
5.	md_color: the maximum deviation from the average color, passed in as an [r,g,b] array
6.	mean_trans: the average opacity of each particle
7.	md_trans: the maximum deviation of opacity
8.	life_lim: the maximum lifetime any particle can have
9.	velocity: the average velocity of every particle
10.	frames: the number of frames the fire will be animated for

create_fire() makes every particle a child of the bounding box so that it is easy to move the fire around and delete it if necessary. It varies the size on its own without any input from the user. After creating the specified number of particles, it then calls animate_fire(), which takes in the initial positions of each particle, their lifetimes, the bounds, the particles themselves, the specified lifetime-limit, the average velocity, the average transparency, and the number of frames to animate. At each frame, the particle loses some life, and once its lifetime is less than 4 frames, it begins to fade. If the particle goes outside of the specified bounds, it is placed back inside the bounding box at z=0 and its life is reset. 

This script uses an implementation of particle systems that I coded myself, which is much less efficient than Blender's actual particle system, but was used as a way to ensure that I conceptually understand how particle systems function.

