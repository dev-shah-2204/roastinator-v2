# Feel free to add more colors
red = 0xFF0000
l_red = 0xEC5858
orange = 0xFF4500
yellow = 0xFFFF00
l_yellow = 0xFFFF4E

green = 0x00FF00
l_green = 0x55AA5B
blue = 0x0000FF
l_blue = 0x60C1E8
cyan = 0x00FFFF

black = 0x000000
white = 0xFFFFFF

colors = [
    0xFF0000,
    0xEC5858,
    0x00FF00,
    0x55AA5B,
    0xFFFF00,
    0xFFFF4E,
    0x0000FF,
    0x60C1E8,
    0x00FFFF,
    0xFF4500
]

colors_but_dict = {
    'red': 0xFF0000,
    'l_red': 0xEC5858,
    'green': 0x00FF00,
    'l_green': 0x55AA5B,
    'yellow ': 0xFFFF00,
    'l_yellow': 0xFFFF4E,
    'blue': 0x0000FF,
    'l_blue': 0x60C1E8,
    'cyan': 0x00FFFF,
    'orange': 0xFF4500,
    'black': 0x000000,
    'white': 0xFFFFFF
}

def get_color(color: str):
    try:
        return colors_but_dict[color]
    except KeyError:
        return colors_but_dict['l_red']
