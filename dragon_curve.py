import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def nb_corners(folds):
    '''
    Description:
    ------------
    Calculates the number of corners produced
    by a given number of paper strip folds

    Parameters:
    -----------
    folds: int
        the number of paper strip folds

    Returns:
    --------
    a float, corresponding to the number of corners
    '''
    return 2**folds - 1

def nb_folds(corners):
    '''
    Description:
    ------------
    Calculates the number of folds perfomed 
    to obtain a given number of paper strip corners

    Parameters:
    -----------
    corners: int
        the number of paper strip corners

    Returns:
    --------
    a float, corresponding to the number of folds
    '''
    return np.log2(corners + 1)

def is_even(num):
    '''
    Description:
    ------------
    Determines whether or not a number is even

    Parameters:
    -----------
    num: int
        the number considered

    Returns:
    --------
    boolean: True when even, False otherwise
    '''
    return num % 2 == 0

def rotation_matrix(angle):
    '''
    Description:
    ------------
    Creates a rotation matrix 

    Parameters:
    -----------
    angle: float
        The angle (in radiant) to which the 
        curve rotates at each fold

    Returns:
    --------
    a rotation matrix as a np.array object
    '''
    mat = np.array([[np.cos(angle), -np.sin(angle)], 
                    [np.sin(angle), np.cos(angle)]])
    return mat

def curve(folds, angle = 2*np.pi/4, alternate = False):
    '''
    Description:
    ------------
    Calculates coordinates for the dragon curve

    Parameters:
    -----------
    folds: int
        the number of paper strip folds
    angle: float
        The angle (in radiant) to which the 
        curve rotates at each fold
    alternate: Boolean
        if True, folds are performed up and down
        alternatively. If False, folds are performed 
        always up.

    Returns:
    --------
    a np.array object, with curve coordinates
    '''
    coord = np.array([[0, 0], [1, 0]])
    if alternate:
        direction = []
        for f in range(folds):
            if is_even(f):
                direction.append(1)
            else:
                direction.append(-1)
    else:
        direction = np.ones(folds)

    for d in direction:
        rot_mat = rotation_matrix(angle = d*angle)
        rot_coord = rot_mat.dot(coord)
        new_orig = rot_coord[:, 0]
        translation = new_orig*np.array([-1, -1])
        trans_x = coord[0] + np.repeat(translation[0], coord[0].shape[0])
        trans_y = coord[1] + np.repeat(translation[1], coord[1].shape[0])
        new_x = np.append(trans_x, rot_coord[0][::-1][1:] + np.repeat(translation[0], rot_coord[0][1:].shape[0]))
        new_y = np.append(trans_y, rot_coord[1][::-1][1:] + np.repeat(translation[1], rot_coord[1][1:].shape[0]))
        new_coord = np.array([new_x, new_y])
        coord = new_coord
    return coord


def draw_curve(folds, angle = 2*np.pi/4, alternate = False, color_gradient = None, background_color = 'black', save = False):
    '''
    Description:
    ------------
    draws the dragon curve

    Parameters:
    -----------
    folds: int
        the number of paper strip folds
    angle: float
        The angle (in radiant) to which the 
        curve rotates at each fold
    alternate: Boolean
        if True, folds are performed up and down
        alternatively. If False, folds are performed 
        always up.
    color_gradient: None or str
        if None, the curve is drawn in tab:orange.
        Otherwise, users can specify which color gradient 
        to use among: 'viridis', 'inferno', 'cool' or 'tab'.
    background_color: str
        the color of the graph background
    save: Boolean
        if True, the graph is saved in the current working path.

    Returns:
    --------
    a matplotlib graph of the curve
    '''
    coords = curve(folds=folds, angle=angle, alternate = alternate)
    if color_gradient == None:
        fig, ax = plt.subplots(figsize = (5, 5))
        plt.plot(coords[0], coords[1], '-', color = 'tab:orange')
    else: 
        prev = 0
        if color_gradient == 'viridis':
            colors=plt.cm.viridis(np.linspace(0,1,folds+1))
        elif color_gradient == 'inferno':
            colors=plt.cm.inferno(np.linspace(0,1,folds+1))
        elif color_gradient == 'cool':
            colors=plt.cm.cool(np.linspace(0,1,folds+1))
        elif color_gradient == 'tab':
            colors=plt.cm.tab20(np.linspace(0,1,folds+1))
            
        fig, ax = plt.subplots(figsize = (5, 5))
        for fold, col in enumerate(colors):
            corners = int(np.ceil(nb_corners(fold)))
            plt.plot(coords[0][prev:corners], coords[1][prev:corners], '-', color = col)
            prev = corners - 1
    plt.tick_params(
        axis='both',        
        which='both',     
        bottom=False,
        left = False,
        labelbottom=False,
        labelleft=False)
    ax.set_facecolor(background_color)
    if save:
        plt.savefig('dragon_curve.jpg', dpi = 800)