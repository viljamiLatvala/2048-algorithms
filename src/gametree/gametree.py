from xml.etree.ElementTree import Element, ElementTree, SubElement, Comment, tostring
from pathlib import Path

# BOARD DIMENSIONS
TILEWIDTH = 50
PADDING = 7
BGCOLOR = "#bbada0"
TILECONFIG = {
    0: {"bgcolor": "#cdc1b4"},
    2: {"bgcolor": "#eee4da", "textcolor": "#776e65", "fontsize": 27.5, "textwidth": "15.56", "textheight": "30"},
    4: {"bgcolor": "#ede0c8", "textcolor": "#776e65", "fontsize": 27.5, "textwidth": "15.56", "textheight": "30"},
    8: {"bgcolor": "#f2b179", "textcolor": "#f9f6f2", "fontsize": 27.5, "textwidth": "15.56", "textheight": "30"},
    16: {"bgcolor": "#f59563", "textcolor": "#f9f6f2", "fontsize": 27.5, "textwidth": "30.86", "textheight": "30"},
    32: {"bgcolor": "#f59563", "textcolor": "#f9f6f2", "fontsize": 27.5, "textwidth": "30.86", "textheight": "30"},
    64: {"bgcolor": "#f65e3b", "textcolor": "#f9f6f2", "fontsize": 27.5, "textwidth": "37.55", "textheight": "24.44"},
    128: {"bgcolor": "#edcf72", "textcolor": "#f9f6f2", "fontsize": 22.5, "textwidth": "37.55", "textheight": "24.44"},
    256: {"bgcolor": "#edcc61", "textcolor": "#f9f6f2", "fontsize": 22.5, "textwidth": "37.55", "textheight": "24.44"},
    512: {"bgcolor": "#edc850", "textcolor": "#f9f6f2", "fontsize": 22.5, "textwidth": "37.55", "textheight": "24.44"},
    1024: {"bgcolor": "#edc53f", "textcolor": "#f9f6f2", "fontsize": 17.5, "textwidth": "39.2", "textheight": "18.89"},
    2048: {"bgcolor": "#edc22e", "textcolor": "#f9f6f2", "fontsize": 17.5, "textwidth": "39.2", "textheight": "18.89"},
    "super": {
        "bgcolor": "#3c3a32",
        "textcolor": "#f9f6f2",
        "fontsize": 17.5,
        "textwidth": "39.2",
        "textheight": "18.89",
    },
}

MARGIN = 100  # MARGIN BETWEEN BOARDS
VERTICAL_MARGIN = 100
BOARDWIDTH = (4 * TILEWIDTH) + (5 * PADDING)


def draw_state(state):
    board = state["board"]
    path = state["path"]
    xcoord = 0
    ycoord = 0

    node = Element("svg")
    board_element = Element(
        "svg",
        {"class": "board", "width": f"{(4*TILEWIDTH) + (5*PADDING) }", "height": f"{(4*TILEWIDTH) + (5*PADDING) }"},
    )

    bg = Element(
        "rect",
        {
            "width": f"{(4*TILEWIDTH) + (5*PADDING) }",
            "height": f"{(4*TILEWIDTH) + (5*PADDING) }",
            "rx": "6",
            "ry": "6",
            "style": f"fill:{BGCOLOR};",
        },
    )
    board_element.append(bg)

    for y in range(4):
        for x in range(4):
            tile_lookup = board[x][y] if board[x][y] <= 2048 else "super"
            tile_color = TILECONFIG[tile_lookup]["bgcolor"]

            tile = Element("g")
            tile.append(
                Element(
                    "rect",
                    {
                        "x": str(PADDING + xcoord),
                        "y": str(PADDING + ycoord),
                        "rx": "4",
                        "ry": "4",
                        "width": f"{TILEWIDTH}",
                        "height": f"{TILEWIDTH}",
                        "style": f"fill:{tile_color};",
                    },
                )
            )
            if board[x][y] > 0:
                xbalance = (TILEWIDTH - float(TILECONFIG[tile_lookup]["textwidth"])) / 2
                ybalance = 2 if board[x][y] < 1000 else 3.5
                ybalance = (
                    ybalance
                    + float(TILECONFIG[tile_lookup]["textheight"])
                    + ((TILEWIDTH - float(TILECONFIG[tile_lookup]["textheight"])) / 2)
                )
                text = Element(
                    "text",
                    {
                        "x": str(PADDING + xcoord + xbalance),
                        "y": str(ycoord + ybalance),
                        "style": "font-family: Clear Sans, Helvetica Neue, Arial, sans-serif; font-weight: bold;",
                        "font-size": str(TILECONFIG[tile_lookup]["fontsize"]),
                        "fill": str(TILECONFIG[tile_lookup]["textcolor"]),
                    },
                )
                text.text = str(board[x][y])
                tile.append(text)

            board_element.append(tile)
            ycoord += TILEWIDTH + PADDING
        ycoord = 0
        xcoord += TILEWIDTH + PADDING

    node.append(board_element)
    # node gets the added dimensions of its children
    childwidths = [float(child.attrib["width"]) for child in node.findall("*")]
    widthsum = sum(childwidths)
    node.attrib = {
        "width": f"{widthsum}",
        "class": "node",
        "path": f"{path}",
        "y": f"{BOARDWIDTH + VERTICAL_MARGIN}",
    }

    return node


def write_html(root, name, path=Path(".")):
    html = Element("html")
    body = SubElement(html, "body")
    main_svg = Element("svg")
    main_svg.set("height", "3000")
    main_svg.set("width", "3000")
    body.append(main_svg)
    main_svg.append(root)
    main = ElementTree(html)
    main.write(path / f"{name}.html")


def assign_widths(node: Element):
    children = node.findall("./svg[@class = 'node']")
    subtree_width = 0

    if not children:
        # Leaves
        node.set("subtree-width", "1")
        node.set("width", f"{BOARDWIDTH + MARGIN}")
        subtree_width = 1

    for child in children:
        if "subtree-width" not in child.attrib:
            # Child has not yet been calculated
            subtree_width += assign_widths(child)
        else:
            # Case when child node has already been calculated
            subtree_width += int(child.get("subtree-width"))

    node.set("subtree-width", f"{subtree_width}")
    node.set("width", f"{(subtree_width * (BOARDWIDTH + MARGIN)) }")
    return subtree_width


def set_x(node: Element, prec_child_w=0):
    children = node.findall("./svg[@class = 'node']")

    preceeding_w = 0
    for child in children:
        set_x(child, f"{preceeding_w}")
        preceeding_w += float(child.get("width"))

    node.set("x", f"{prec_child_w}")
    board = node.find("./svg[@class='board']")
    board.set("x", f"{(float(node.get('width')) / 2)-((BOARDWIDTH + MARGIN)/2)}")


def draw_boards(states):
    state_elements = {}
    for state in states:
        element = draw_state(state)
        parent = state["path"][:-1]
        if parent:
            state_elements[f"{parent}"].append(element)

        state_elements[f"{state['path']}"] = element

    root_state = [value for value in state_elements.values()][0]
    assign_widths(root_state)
    set_x(root_state)
    root_state.set("y", "0")

    return root_state


def draw_connections(root: Element):
    board = root.find("./svg[@class='board']")
    from_mid_x = ((float(root.get("width"))) / 2) - (MARGIN / 2)
    from_y = float(board.get("height"))

    for child in root.findall("./svg[@class='node']"):
        to_mid_x = float(child.get("width")) / 2 + float(child.get("x")) - (MARGIN / 2)
        to_y = float(child.get("y"))
        root.append(
            Element(
                "line",
                {"x1": f"{from_mid_x}", "y1": f"{from_y}", "x2": f"{to_mid_x}", "y2": f"{to_y}", "stroke": "black"},
            )
        )
        draw_connections(child)


def form_graph(states):
    boards = draw_boards(states)
    draw_connections(boards)
    return boards


states = [
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root"]},
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root", "left"]},
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root", "right"]},
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root", "right", "left"]},
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root", "right", "mid"]},
    {"board": [[0, 2, 32, 0], [16, 0, 512, 0], [0, 8, 2048, 1024], [0, 16, 0, 0]], "path": ["root", "right", "right"]},
]
