import pygame

def map_coordinates(point, input_size, output_size):
    """
    Maps coordinates from input space (webcam) to output space (game window)
    
    Args:
        point (tuple): (x, y) coordinates in input space
        input_size (tuple): (width, height) of input space
        output_size (tuple): (width, height) of output space
    
    Returns:
        tuple: (x, y) coordinates mapped to output space
    """
    x, y = point
    input_width, input_height = input_size[1], input_size[0]  # OpenCV returns (height, width)
    output_width, output_height = output_size
    
    # Map x and y to game window coordinates
    mapped_x = int((x / input_width) * output_width)
    mapped_y = int((y / input_height) * output_height)
    
    return (mapped_x, mapped_y)

def check_collision(point, rect):
    """
    Check if a point (fingertip) collides with a rectangle (balloon)
    
    Args:
        point (tuple): (x, y) coordinates of the point
        rect (pygame.Rect): Rectangle to check collision with
    
    Returns:
        bool: True if collision detected, False otherwise
    """
    return rect.collidepoint(point)

def normalize_webcam_position(hand_landmarks, cam_width, cam_height, game_width, game_height):
    """
    Normalize and map hand landmark positions to game coordinates
    
    Args:
        hand_landmarks: MediaPipe hand landmarks
        cam_width: Width of webcam frame
        cam_height: Height of webcam frame
        game_width: Width of game window
        game_height: Height of game window
    
    Returns:
        tuple: (x, y) normalized coordinates for game window
    """
    # Get index finger tip position (landmark 8)
    x = hand_landmarks.landmark[8].x * cam_width
    y = hand_landmarks.landmark[8].y * cam_height
    
    # Map to game coordinates
    game_x = int(x / cam_width * game_width)
    game_y = int(y / cam_height * game_height)
    
    return (game_x, game_y)