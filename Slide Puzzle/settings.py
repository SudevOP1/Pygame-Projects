import pygame
from random import choice
import json
from os.path import join

WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720
BLOCK_SIZE    = 100
BLOCK_SPEED   = 5
COLORS = {
    "bg"        : "#2b374b",
    "block"     : "#178a94",
    "block text": "#bfd8d1",
    "text"      : "#ee8080",
    "text bg"   : "#d03161",
}
PADDING = {
    "block"          : 5,
}
BLOCK_POS = {}
for row in range(1, 5):
    for col in range(1, 5):
        x = (col - 1) * (BLOCK_SIZE + PADDING["block"]) + (WINDOW_WIDTH  - (4 * (BLOCK_SIZE + PADDING["block"]))) // 2
        y = (row - 1) * (BLOCK_SIZE + PADDING["block"]) + (WINDOW_HEIGHT - (4 * (BLOCK_SIZE + PADDING["block"]))) // 2
        BLOCK_POS[(row, col)] = (x, y)