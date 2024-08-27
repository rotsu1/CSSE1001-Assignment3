# Map representation of different tiles
GRASS = 'G'
SOIL = 'S'
UNTILLED = 'U'

# Constants related to moving the player
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'

MOVE_DELTAS = {
    LEFT: (0, -1),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    UP: (-1, 0),
}

# Colours
INVENTORY_COLOUR = '#fdc074'
INVENTORY_OUTLINE_COLOUR = '#d68f54'
INVENTORY_SELECTED_COLOUR = '#d68f54'
INVENTORY_EMPTY_COLOUR = 'grey'

# Images
IMAGES = {
    GRASS: 'grass.png',
    SOIL: 'soil.png',
    UNTILLED: 'untilled_soil.png',
    DOWN: 'player_s.png',
    UP: 'player_w.png',
    LEFT: 'player_a.png',
    RIGHT: 'player_d.png',
}

# Fonts
HEADING_FONT = ('Helvetica', 15, 'bold')

# Dimensions
FARM_WIDTH = 500
INVENTORY_WIDTH = 200
INFO_BAR_HEIGHT = 90
BANNER_HEIGHT = 130

# Energy cost of actions (only applied if action was successful)
MOVE_COST = 1
HARVEST_COST = 3
PLANT_COST = 2
REMOVE_COST = 2
TILL_COST = 3
UNTILL_COST = 3

# All seeds available in the game
SEEDS = [
    'Potato Seed',
    'Kale Seed',
    'Berry Seed',
]

# All items, listed in the order in which they should appear in the inventory
ITEMS = [
    'Potato Seed',
    'Kale Seed',
    'Berry Seed',
    'Potato',
    'Kale',
    'Berry',
]

# How much it costs to buy certain items from the store
# Any items not listed cannot be bought at the store
BUY_PRICES = {
    'Potato Seed': 10,
    'Kale Seed': 70,
    'Berry Seed': 80,
}

# How much you can sell items for at the store
SELL_PRICES = {
    'Potato Seed': 5,
    'Potato': 25,
    'Kale Seed': 35,
    'Kale': 110,
    'Berry': 50,
    'Berry Seed': 40,
}
