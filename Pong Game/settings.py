import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 
SIZE = {
    "paddle": (40,100),
    "ball"  : (30,30),
}
POS = {
    "player"  : (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2),
    "opponent": (50, WINDOW_HEIGHT / 2),
}
SPEED = {
    "player"  : 500,
    "opponent": 400,
    "ball"    : 650,
}
COLORS = {
    "paddle"       : "#ee322c",
    "ball"         : "#87CEFA",
    "bg"           : "#002633",
    "bg detail"    : "#004a63",
}
#Ball alternate color ee622c