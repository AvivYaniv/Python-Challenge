from PIL import Image, ImageSequence

# The image to process to JoyStick movments
white_gif = Image.open("white.gif")

size_unit = 200
special_value = 8
joystick_static_position = 100, 100

# The result image, representing the letters written by JoyStick
black_img = Image.new('RGB', (5 * size_unit, size_unit), "white")

space_between_letters = 100
initial_drawing_position = (space_between_letters, space_between_letters)
drawing_position = initial_drawing_position

# Going over the frames and converting "special value" indexes to movments
for frame in ImageSequence.Iterator(white_gif):    
    # Getting the index of the "special value" in current frame
    index_in_frame = list(frame.getdata()).index(special_value)
    
    # Converting index to position in frame
    position_in_frame = index_in_frame % size_unit, index_in_frame / size_unit

    # If JoyStick is currently static, adding space between letters
    if position_in_frame == joystick_static_position:
        drawing_position = drawing_position[0] + space_between_letters, drawing_position[1]

    # Setting the movment as the diffrence between JoyStick location and JoyStick stationary position
    movment_direction = position_in_frame[0] - joystick_static_position[0], position_in_frame[1] - joystick_static_position[1]
	
    # Updating drawing postion according to JoyStick movment direction
    drawing_position = drawing_position[0] + movment_direction[0], drawing_position[1] + movment_direction[1]

    # Writting current position
    black_img.putpixel(drawing_position, 0)

# Saving the dechipered letters image
black_img.save('22_black.gif')

print "Done :)"
