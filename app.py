
import streamlit as st
import streamlit.components.v1 as components
import random
import base64
import json


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Snakes & Ladders",
    page_icon="🐍"
)

st.title("🐍 Snakes & Ladders 🪜")

# =========================================================
# CUSTOMIZATION
# =========================================================

defaults = {
    "custom_names": ["Player 1", "Player 2", "Player 3", "Player 4"],
    "custom_colors": ["#16a34a", "#2563eb", "#eab308", "#9333ea"],
    "numbering_mode": "Traditional",
    "game_mode": "Classic",
    "custom_snakes": 3,
    "custom_ladders": 3,
    "image_fit": "Cover",
    "cell_color_1": "#ffffff",
    "cell_color_2": "#eaf2ff",
    "cell_opacity": 0.45,
    "show_cells": True,
    "show_grid": True,
    "board_image_bytes": None,
    "board_image_type": None,
}

for _key, _value in defaults.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value


def generate_custom_paths(snake_count, ladder_count):
    snakes_out = {}
    ladders_out = {}
    used = {1, 100}

    for _ in range(3000):
        if len(snakes_out) >= snake_count:
            break
        head = random.randint(35, 98)
        tail = random.randint(2, head - 10)
        if head not in used and tail not in used:
            snakes_out[head] = tail
            used.update([head, tail])

    for _ in range(3000):
        if len(ladders_out) >= ladder_count:
            break
        bottom = random.randint(2, 75)
        top = random.randint(bottom + 10, 99)
        if bottom not in used and top not in used:
            ladders_out[bottom] = top
            used.update([bottom, top])

    return snakes_out, ladders_out


def make_traditional_board():
    rows = []
    for row_from_bottom in range(10):
        row = list(range(row_from_bottom * 10 + 1, row_from_bottom * 10 + 11))
        if row_from_bottom % 2 == 1:
            row.reverse()
        rows.append(row)
    return rows[::-1]


def make_random_board():
    nums = list(range(1, 100))
    random.shuffle(nums)
    flat = [100] + nums
    return [flat[i:i + 10] for i in range(0, 100, 10)]


def save_configuration():
    return {
        "version": 2,
        "numbering_mode": st.session_state.numbering_mode,
        "game_mode": st.session_state.game_mode,
        "custom_snakes": st.session_state.custom_snakes,
        "custom_ladders": st.session_state.custom_ladders,
        "image_fit": st.session_state.image_fit,
        "cell_color_1": st.session_state.cell_color_1,
        "cell_color_2": st.session_state.cell_color_2,
        "cell_opacity": st.session_state.cell_opacity,
        "show_cells": st.session_state.show_cells,
        "show_grid": st.session_state.show_grid,
        "player_names": st.session_state.custom_names,
        "player_colors": st.session_state.custom_colors,
        "board_image_type": st.session_state.board_image_type,
        "board_image_base64": (
            base64.b64encode(st.session_state.board_image_bytes).decode("ascii")
            if st.session_state.board_image_bytes else None
        ),
    }


def load_configuration(data):
    st.session_state.numbering_mode = data.get("numbering_mode", "Traditional")
    st.session_state.game_mode = data.get("game_mode", "Classic")
    st.session_state.custom_snakes = int(data.get("custom_snakes", 3))
    st.session_state.custom_ladders = int(data.get("custom_ladders", 3))
    st.session_state.image_fit = data.get("image_fit", "Cover")
    st.session_state.cell_color_1 = data.get("cell_color_1", "#ffffff")
    st.session_state.cell_color_2 = data.get("cell_color_2", "#eaf2ff")
    st.session_state.cell_opacity = float(data.get("cell_opacity", 0.45))
    st.session_state.show_cells = bool(data.get("show_cells", True))
    st.session_state.show_grid = bool(data.get("show_grid", True))

    names = data.get("player_names", defaults["custom_names"])
    colors = data.get("player_colors", defaults["custom_colors"])
    st.session_state.custom_names = (names + defaults["custom_names"])[:4]
    st.session_state.custom_colors = (colors + defaults["custom_colors"])[:4]

    image_b64 = data.get("board_image_base64")
    image_type = data.get("board_image_type")
    if image_b64 and image_type:
        st.session_state.board_image_bytes = base64.b64decode(image_b64)
        st.session_state.board_image_type = image_type
    else:
        st.session_state.board_image_bytes = None
        st.session_state.board_image_type = None

    for key in [
        "players", "current_player", "dice", "number_of_players",
        "last_move", "winner", "board_signature", "paths_signature",
        "board_layout"
    ]:
        st.session_state.pop(key, None)


with st.sidebar:
    st.header("🎨 Board Customizer")

    uploaded_board = st.file_uploader(
        "Upload board background",
        type=["png", "jpg", "jpeg", "webp"],
        key="board_upload",
    )

    if uploaded_board is not None:
        st.session_state.board_image_bytes = uploaded_board.getvalue()
        st.session_state.board_image_type = uploaded_board.type or "image/png"

    st.session_state.image_fit = st.selectbox(
        "Image fit",
        ["Cover", "Contain"],
        index=["Cover", "Contain"].index(st.session_state.image_fit),
        key="image_fit_widget",
    )

    st.session_state.show_cells = st.checkbox(
        "Show cell backgrounds",
        value=st.session_state.show_cells,
        key="show_cells_widget",
    )

    st.subheader("🧩 Cell Design")

    st.session_state.cell_color_1 = st.color_picker(
        "Cell color 1", st.session_state.cell_color_1, key="cell1_widget"
    )

    st.session_state.cell_color_2 = st.color_picker(
        "Cell color 2", st.session_state.cell_color_2, key="cell2_widget"
    )

    st.session_state.cell_opacity = st.slider(
        "Cell opacity", 0.0, 1.0,
        st.session_state.cell_opacity, 0.05,
        key="opacity_widget"
    )

    st.session_state.show_grid = st.checkbox(
        "Show cell borders",
        value=st.session_state.show_grid,
        key="grid_widget",
    )

    st.subheader("🔢 Numbering")

    st.session_state.numbering_mode = st.selectbox(
        "Board numbering",
        ["Traditional", "Randomized"],
        index=["Traditional", "Randomized"].index(st.session_state.numbering_mode),
        key="numbering_widget",
    )

    st.subheader("🎮 Game Mode")

    st.session_state.game_mode = st.selectbox(
        "Game mode",
        ["Classic", "Fast", "Custom"],
        index=["Classic", "Fast", "Custom"].index(st.session_state.game_mode),
        key="mode_widget",
    )

    if st.session_state.game_mode == "Custom":
        st.session_state.custom_snakes = st.slider(
            "Number of snakes", 1, 8,
            st.session_state.custom_snakes,
            key="custom_snakes_widget"
        )
        st.session_state.custom_ladders = st.slider(
            "Number of ladders", 1, 8,
            st.session_state.custom_ladders,
            key="custom_ladders_widget"
        )

    st.subheader("👤 Players")

    for i in range(4):
        st.session_state.custom_names[i] = st.text_input(
            f"Player {i + 1} name",
            st.session_state.custom_names[i],
            key=f"name_widget_{i}",
        )
        st.session_state.custom_colors[i] = st.color_picker(
            f"Player {i + 1} token color",
            st.session_state.custom_colors[i],
            key=f"color_widget_{i}",
        )

    st.subheader("💾 Save / Load")

    st.download_button(
        "⬇️ Save My Board",
        data= json.dumps(save_configuration(), indent=2),
        file_name="my_snakes_ladders_board.json",
        mime="application/json",
        key="save_board",
    )

    loaded_board = st.file_uploader(
        "Load saved board",
        type=["json"],
        key="load_board",
    )

    if loaded_board is not None:
        load_id = f"{loaded_board.name}:{loaded_board.size}"
        if st.session_state.get("loaded_board_id") != load_id:
            try:
                load_configuration(
                    json.loads(loaded_board.getvalue().decode("utf-8"))
                )
                st.session_state.loaded_board_id = load_id
                st.rerun()
            except Exception as exc:
                st.error(f"Could not load board: {exc}")


# =========================================================
# PLAYER COLORS

# =========================================================

player_colors = ["custom-p1", "custom-p2", "custom-p3", "custom-p4"]
player_color_names = st.session_state.custom_names


# =========================================================
# PLAYER SELECTION
# =========================================================

num_players = st.selectbox(
    "Choose number of players:",
    [2, 3, 4],
    index=0,
    key="player_count"
)


# =========================================================
# CREATE BOARD

board_signature = st.session_state.numbering_mode

if (
    "board_layout" not in st.session_state
    or st.session_state.get("board_signature") != board_signature
):
    if st.session_state.numbering_mode == "Randomized":
        st.session_state.board_layout = make_random_board()
    else:
        st.session_state.board_layout = make_traditional_board()

    st.session_state.board_signature = board_signature

board = st.session_state.board_layout


# =========================================================
# SNAKES / LADDERS

paths_signature = (
    st.session_state.game_mode,
    st.session_state.custom_snakes,
    st.session_state.custom_ladders,
)

if st.session_state.get("paths_signature") != paths_signature:

    if st.session_state.game_mode == "Classic":
        st.session_state.snakes_cfg = {98: 10}
        st.session_state.ladders_cfg = {8: 48}

    elif st.session_state.game_mode == "Fast":
        st.session_state.snakes_cfg = {
            98: 10,
            76: 34,
        }
        st.session_state.ladders_cfg = {
            8: 48,
            21: 65,
        }

    else:
        st.session_state.snakes_cfg, st.session_state.ladders_cfg = (
            generate_custom_paths(
                st.session_state.custom_snakes,
                st.session_state.custom_ladders,
            )
        )

    st.session_state.paths_signature = paths_signature

snakes = st.session_state.snakes_cfg
ladders = st.session_state.ladders_cfg


# =========================================================
# FIND POSITION OF NUMBER
# =========================================================

def get_position(number):

    for row in range(10):

        for col in range(10):

            if board[row][col] == number:

                return row, col

    return None


# =========================================================
# INITIALIZE GAME
# =========================================================

if (
    "players" not in st.session_state
    or
    st.session_state.get("number_of_players")
    != num_players
):

    st.session_state.players = {
        st.session_state.custom_names[i]: 0
        for i in range(num_players)
    }

    st.session_state.current_player = 0

    st.session_state.dice = 1

    st.session_state.number_of_players = num_players

    st.session_state.last_move = None
    st.session_state.winner = None


# =========================================================
# MAKE SURE VARIABLES EXIST
# =========================================================

if "last_move" not in st.session_state:

    st.session_state.last_move = None


if "dice" not in st.session_state:
    st.session_state.dice = 1

if "winner" not in st.session_state:
    st.session_state.winner = None


# =========================================================
# CURRENT PLAYER
# =========================================================

current_player = st.session_state.current_player

player_name = st.session_state.custom_names[current_player]
current_color = player_name


st.subheader(
    f"🎮 {player_name} ({current_color})'s Turn"
)


# =========================================================
# ROLL DICE
# =========================================================

if st.button(
    "🎲 Roll Dice",
    key="roll_dice",
    disabled=st.session_state.winner is not None
):

    # -----------------------------------------------------
    # Roll
    # -----------------------------------------------------

    dice_value = random.randint(1, 6)

    st.session_state.dice = dice_value


    # -----------------------------------------------------
    # Current position
    # -----------------------------------------------------

    old_position = (
        st.session_state.players[player_name]
    )


    # -----------------------------------------------------
    # Calculate landing position
    # -----------------------------------------------------

    landing_position = (
        old_position + dice_value
    )


    # -----------------------------------------------------
    # Default values
    # -----------------------------------------------------

    final_position = landing_position

    move_type = "normal"


    # =====================================================
    # CHECK WHETHER MOVE EXCEEDS 100
    # =====================================================

    if landing_position > 100:

        landing_position = old_position

        final_position = old_position

        move_type = "invalid"


    else:

        # =================================================
        # LADDER
        # =================================================

        if landing_position in ladders:

            final_position = (
                ladders[landing_position]
            )

            move_type = "ladder"


        # =================================================
        # SNAKE
        # =================================================

        elif landing_position in snakes:

            final_position = (
                snakes[landing_position]
            )

            move_type = "snake"


        # -------------------------------------------------
        # SAVE POSITION
        # -------------------------------------------------

        st.session_state.players[player_name] = (
            final_position
        )


    if final_position == 100:
        st.session_state.winner = player_name

    # =====================================================
    # SAVE MOVE FOR ANIMATION
    # =====================================================

    st.session_state.last_move = {

        "player": player_name,

        "player_number": current_player + 1,

        "old": old_position,

        "dice": dice_value,

        "landing": landing_position,

        "final": final_position,

        "type": move_type

    }


    # =====================================================
    # EXTRA TURN RULE
    # =====================================================

    if st.session_state.winner is None and dice_value == 6:

        # SAME PLAYER GETS ANOTHER TURN

        st.session_state.current_player = (
            current_player
        )

    else:

        # MOVE TO NEXT PLAYER

        st.session_state.current_player = (

            current_player + 1

        ) % num_players


# =========================================================
# DICE DISPLAY
# =========================================================

st.subheader(
    f"🎲 Dice: {st.session_state.dice}"
)


# =========================================================
# EXTRA TURN MESSAGE
# =========================================================

if (
    st.session_state.last_move is not None
    and
    st.session_state.last_move["dice"] == 6
):

    st.success(
        f"🎉 {st.session_state.last_move['player']} "
        f"rolled a 6 and gets another chance!"
    )


# =========================================================
# PLAYER POSITIONS
# =========================================================

st.write("### 👥 Player Positions")


for i in range(num_players):

    player = st.session_state.custom_names[i]

    position = st.session_state.players[player]

    color_name = st.session_state.custom_names[i]


    if position == 0:

        position_text = "START"

    else:

        position_text = str(position)


    st.write(
        f"**{player} ({color_name}):** "
        f"{position_text}"
    )


# =========================================================
# LAST MOVE
# =========================================================

last_move = st.session_state.last_move


# =========================================================
# HTML START
# =========================================================

# =========================================================
# PREPARE CUSTOM IMAGE / CELL STYLE
# =========================================================

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        hex_color = "ffffff"
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

board_image_html = ""
if st.session_state.board_image_bytes:
    image_b64 = base64.b64encode(st.session_state.board_image_bytes).decode("utf-8")
    mime_type = st.session_state.board_image_type or "image/png"
    object_fit = "cover" if st.session_state.image_fit == "Cover" else "contain"
    board_image_html = f"""
    <img class=\"board-background\" src=\"data:{mime_type};base64,{image_b64}\"
         style=\"object-fit:{object_fit};\" alt=\"Custom board background\">
    """

if st.session_state.show_cells:
    alpha = st.session_state.cell_opacity
    cell_backgrounds = [
        hex_to_rgba(st.session_state.cell_color_1, alpha),
        hex_to_rgba(st.session_state.cell_color_2, alpha)
    ]
else:
    cell_backgrounds = ["rgba(255,255,255,0)", "rgba(255,255,255,0)"]

cell_border = (
    "1px solid rgba(0,0,0,.45)"
    if st.session_state.show_grid
    else "1px solid transparent"
)

token_css = "\n".join(
    f".custom-p{i + 1} {{ background: linear-gradient(145deg, #ffffff, {st.session_state.custom_colors[i]}); }}"
    for i in range(4)
)

html = """

<!DOCTYPE html>

<html>

<head>

<style>


/* =====================================================
   BODY
   ===================================================== */

body {

    margin: 0;

    padding: 0;

    background: white;

}


/* =====================================================
   GAME CONTAINER
   ===================================================== */

.game-container {

    position: relative;

    width: 550px;

    margin: auto;

}


/* =====================================================
   STARTING AREA
   ===================================================== */

.starting-area {

    width: 550px;

    height: 70px;

    border-bottom: 3px solid black;

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 25px;

    box-sizing: border-box;

}


/* =====================================================
   PLAYER PIECE
   ===================================================== */

.player-piece { position: relative; width: 34px; height: 38px; border: 0; box-sizing: border-box; z-index: 10; filter: drop-shadow(0 3px 2px rgba(0,0,0,.30)); }
.player-piece::before { content:""; position:absolute; width:18px; height:18px; left:8px; top:1px; border:2px solid #111; border-radius:50%; background:inherit; box-shadow:inset 3px 3px 4px rgba(255,255,255,.45); z-index:2; }
.player-piece::after { content:""; position:absolute; left:2px; bottom:1px; width:30px; height:20px; border:2px solid #111; border-radius:48% 48% 35% 35%; background:inherit; box-shadow:inset 4px 4px 5px rgba(255,255,255,.35); }


/* =====================================================
   BOARD PIECE
   ===================================================== */

.board-piece { position:absolute; width:34px; height:38px; border:0; box-sizing:border-box; z-index:10; transition:left .18s linear, top .18s linear; filter:drop-shadow(0 3px 2px rgba(0,0,0,.30)); }
.board-piece::before { content:""; position:absolute; width:18px; height:18px; left:8px; top:1px; border:2px solid #111; border-radius:50%; background:inherit; box-shadow:inset 3px 3px 4px rgba(255,255,255,.48); z-index:2; }
.board-piece::after { content:""; position:absolute; left:2px; bottom:1px; width:30px; height:20px; border:2px solid #111; border-radius:48% 48% 35% 35%; background:inherit; box-shadow:inset 4px 4px 5px rgba(255,255,255,.35); }
.token-number { position:absolute; left:0; right:0; bottom:4px; z-index:4; text-align:center; font:700 12px Arial,sans-serif; color:white; text-shadow:1px 1px 2px #111; pointer-events:none; }


/* =====================================================
   COLORS
   ===================================================== */

.green { background:linear-gradient(145deg,#5fe06a,#168b32); }
.blue { background:linear-gradient(145deg,#5f8dff,#153bd0); }
.gold { background:linear-gradient(145deg,#ffe96a,#e5a800); }
.purple { background:linear-gradient(145deg,#c878ff,#7121b8); }
.token-bounce { animation:tokenBounce .45s ease; }
@keyframes tokenBounce { 0%{transform:translateY(0) scale(1)} 35%{transform:translateY(-9px) scale(1.05)} 70%{transform:translateY(2px) scale(.98)} 100%{transform:translateY(0) scale(1)} }


/* =====================================================
   LADDER ANIMATION
   ===================================================== */

.ladder-effect {

    animation:

        ladderGlow

        0.35s

        ease-in-out

        infinite

        alternate;

}


@keyframes ladderGlow {

    from {

        transform: scale(1);

        filter: brightness(1);

    }

    to {

        transform: scale(1.35);

        filter: brightness(1.8);

    }

}


/* =====================================================
   SNAKE ANIMATION
   ===================================================== */

.snake-effect {

    animation:

        snakeShake

        0.10s

        linear

        infinite;

}


@keyframes snakeShake {

    0% {

        transform:

            translateX(0)

            rotate(0deg);

    }


    25% {

        transform:

            translateX(-6px)

            rotate(-10deg);

    }


    50% {

        transform:

            translateX(6px)

            rotate(10deg);

    }


    75% {

        transform:

            translateX(-5px)

            rotate(-8deg);

    }


    100% {

        transform:

            translateX(0)

            rotate(0deg);

    }

}


/* =====================================================
   SNAKE FLASH
   ===================================================== */

.snake-flash {

    animation:

        snakeFlash

        0.25s

        linear

        3;

}


@keyframes snakeFlash {

    0% {

        filter: brightness(1);

    }

    50% {

        filter: brightness(3);

    }

    100% {

        filter: brightness(1);

    }

}


/* =====================================================
   DICE ANIMATION
   ===================================================== */
.dice-stage { height:70px; display:flex; align-items:center; justify-content:center; margin-right:10px; perspective:700px; }
.dice-cube { width:54px; height:54px; border-radius:13px; border:3px solid #111; background:linear-gradient(145deg,#fff,#d8d8d8); box-shadow:0 7px 12px rgba(0,0,0,.25), inset 3px 3px 6px rgba(255,255,255,.9); display:flex; align-items:center; justify-content:center; font:700 40px "Segoe UI Symbol","Arial Unicode MS",sans-serif; color:#111; transform-style:preserve-3d; }
.dice-roll { animation:diceRoll .85s cubic-bezier(.2,.8,.2,1); }
@keyframes diceRoll { 0%{transform:rotateX(0) rotateY(0) rotateZ(0) scale(1)} 20%{transform:rotateX(160deg) rotateY(100deg) rotateZ(-12deg) scale(1.08)} 45%{transform:rotateX(310deg) rotateY(240deg) rotateZ(15deg) scale(1.16)} 70%{transform:rotateX(500deg) rotateY(390deg) rotateZ(-8deg) scale(1.08)} 100%{transform:rotateX(720deg) rotateY(540deg) rotateZ(0) scale(1)} }

/* =====================================================
   BOARD BACKGROUND + GRID
   ===================================================== */
.board-background { position:absolute; inset:0; width:100%; height:100%; z-index:0; pointer-events:none; 
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    z-index:0;
    pointer-events:none;
    }
.game-board { position:relative; width:550px; height:550px; display:grid; grid-template-columns:repeat(10,55px); grid-template-rows:repeat(10,55px); overflow:hidden; box-sizing:border-box; box-shadow:inset 0 0 0 3px #111; }

/* =====================================================
   SVG
   ===================================================== */

.game-overlay {

    position: absolute;

    top: 70px;

    left: 0;

    width: 550px;

    height: 550px;

    z-index: 5;

    pointer-events: none;

}


/* =====================================================
   SNAKE LINE
   ===================================================== */

.snake-outline {

    stroke: #173b16;

    stroke-width: 15;

    fill: none;

    stroke-linecap: round;

    stroke-linejoin: round;

}

.snake-line {

    stroke: url(#snakeBody);

    stroke-width: 11;

    fill: none;

    stroke-linecap: round;

    stroke-linejoin: round;

}

.snake-highlight {

    stroke: rgba(190, 240, 150, 0.65);

    stroke-width: 2.5;

    fill: none;

    stroke-linecap: round;

}

.snake-head {

    fill: url(#snakeHead);

    stroke: #173b16;

    stroke-width: 3;

}

.snake-eye {

    fill: white;

    stroke: #173b16;

    stroke-width: 1.5;

}

.snake-pupil {

    fill: #111;

}

.snake-tongue {

    stroke: #d81b60;

    stroke-width: 2.5;

    fill: none;

    stroke-linecap: round;

}

.snake-spot {

    fill: #245c1b;

    opacity: 0.9;

}


/* =====================================================
   LADDER
   ===================================================== */

.ladder-shadow { stroke:#5b351b; stroke-width:11; stroke-linecap:round; }
.ladder-line { stroke:#b87333; stroke-width:7; stroke-linecap:round; }
.ladder-highlight { stroke:#f0b36d; stroke-width:2; stroke-linecap:round; opacity:.9; }
.ladder-rung { stroke:#7b461f; stroke-width:6; stroke-linecap:round; }
.ladder-rung-highlight { stroke:#d99550; stroke-width:2; stroke-linecap:round; }

{token_css}
</style>

</head>


<body>


<div class="game-container">


<!-- =====================================================
     STARTING AREA
     ===================================================== -->

<div class="starting-area">

<div class="dice-stage"><div id="dice-cube" class="dice-cube">⚀</div></div>

"""


# =========================================================
# STARTING PIECES
# =========================================================

for i in range(num_players):

    player = f"Player {i + 1}"

    position = st.session_state.players[player]

    color = player_colors[i]


    if position == 0:

        html += f"""

        <div

            class="player-piece {color}"

            title="{player}">
            <span class="token-number">{i + 1}</span>

        </div>

        """


html += """

</div>


<!-- =====================================================
     BOARD
     ===================================================== -->

<div class="game-board">

    {board_image_html}

"""


# =========================================================
# BOARD CELLS
# =========================================================

for row_index, row in enumerate(board):

    for col_index, number in enumerate(row):

        cell_background = cell_backgrounds[(row_index + col_index) % 2]

        html += f"""

        <div

            class="cell"

            style="

                width: 55px;

                height: 55px;

                border: {cell_border};

                background: {cell_background};

                backdrop-filter: blur(1.5px);

                display: flex;

                align-items: center;

                justify-content: center;

                box-sizing: border-box;

                font-size: 17px;

                font-weight: bold;

                color: #111;

                position: relative;
                z-index: 1;

            ">

            {number}

        </div>

        """


# =========================================================
# BOARD PIECES
# =========================================================

for i in range(num_players):

    player = f"Player {i + 1}"

    position = st.session_state.players[player]

    color = player_colors[i]


    if position > 0:

        row, col = get_position(position)


        left = col * 55 + 10.5

        top = row * 55 + 8.5


        html += f"""

        <div

            id="piece-{i + 1}"

            class="board-piece {color}"

            style="

                left: {left}px;

                top: {top}px;

            "

            title="{player}">

            <span class="token-number">{i + 1}</span>
        </div>

        """


html += """

</div>


<!-- =====================================================
     SVG OVERLAY
     ===================================================== -->

<svg

    class="game-overlay"

    viewBox="0 0 550 550"

    xmlns="http://www.w3.org/2000/svg">

"""


# =========================================================
# DRAW SNAKES
# =========================================================

# Decorative SVG definitions for a more realistic snake
html += """
<defs>
    <linearGradient id="snakeBody" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#58a942"/>
        <stop offset="45%" stop-color="#3f8f2f"/>
        <stop offset="100%" stop-color="#2f7024"/>
    </linearGradient>
    <radialGradient id="snakeHead" cx="35%" cy="30%">
        <stop offset="0%" stop-color="#6fbd55"/>
        <stop offset="100%" stop-color="#347d28"/>
    </radialGradient>
</defs>
"""

for start, end in snakes.items():

    start_row, start_col = get_position(start)
    end_row, end_col = get_position(end)

    x1 = start_col * 55 + 27.5
    y1 = start_row * 55 + 27.5
    x2 = end_col * 55 + 27.5
    y2 = end_row * 55 + 27.5

    # Same curve used by the snake body and its animation path.
    middle_x = (x1 + x2) / 2 + 35
    middle_y = (y1 + y2) / 2

    # Direction of the snake's head.
    import math
    angle = math.degrees(math.atan2(middle_y - y1, middle_x - x1))

    html += f"""
    <!-- dark outline -->
    <path
        class="snake-outline"
        d="M {x1} {y1} Q {middle_x} {middle_y} {x2} {y2}">
    </path>

    <!-- green body -->
    <path
        class="snake-line"
        d="M {x1} {y1} Q {middle_x} {middle_y} {x2} {y2}">
    </path>

    <!-- small highlight along the body -->
    <path
        class="snake-highlight"
        d="M {x1 - 2} {y1 - 2} Q {middle_x - 2} {middle_y - 2} {x2 - 2} {y2 - 2}">
    </path>

    <!-- body spots -->
    <circle class="snake-spot" cx="{x1 + (middle_x-x1)*0.22}" cy="{y1 + (middle_y-y1)*0.22}" r="3.5"></circle>
    <circle class="snake-spot" cx="{x1 + (middle_x-x1)*0.48 + (x2-middle_x)*0.05}" cy="{y1 + (middle_y-y1)*0.48 + (y2-middle_y)*0.05}" r="4"></circle>
    <circle class="snake-spot" cx="{x1 + (middle_x-x1)*0.72 + (x2-middle_x)*0.20}" cy="{y1 + (middle_y-y1)*0.72 + (y2-middle_y)*0.20}" r="3.5"></circle>

    <!-- snake head, eyes and forked tongue -->
    <g transform="translate({x1} {y1}) rotate({angle})">
        <ellipse class="snake-head" cx="0" cy="0" rx="15" ry="12"></ellipse>
        <ellipse class="snake-eye" cx="-6" cy="-5" rx="4" ry="4"></ellipse>
        <ellipse class="snake-eye" cx="6" cy="-5" rx="4" ry="4"></ellipse>
        <circle class="snake-pupil" cx="-5" cy="-5" r="1.8"></circle>
        <circle class="snake-pupil" cx="7" cy="-5" r="1.8"></circle>
        <path class="snake-tongue" d="M 0 9 L 0 17 M 0 17 L -5 22 M 0 17 L 5 22"></path>
    </g>
    """


# =========================================================
# DRAW LADDERS
# =========================================================

for start, end in ladders.items():

    start_row, start_col = get_position(start)

    end_row, end_col = get_position(end)


    x1 = start_col * 55 + 27.5

    y1 = start_row * 55 + 27.5


    x2 = end_col * 55 + 27.5

    y2 = end_row * 55 + 27.5


    dx = x2 - x1

    dy = y2 - y1


    length = (

        dx ** 2

        + dy ** 2

    ) ** 0.5


    px = (

        -dy / length

    ) * 8


    py = (

        dx / length

    ) * 8


    html += f"""

    <line class="ladder-shadow" x1="{x1 + px}" y1="{y1 + py}" x2="{x2 + px}" y2="{y2 + py}"></line>
    <line class="ladder-shadow" x1="{x1 - px}" y1="{y1 - py}" x2="{x2 - px}" y2="{y2 - py}"></line>

    <line

        class="ladder-line"

        x1="{x1 + px}"

        y1="{y1 + py}"

        x2="{x2 + px}"

        y2="{y2 + py}">

    </line>


    <line

        class="ladder-line"

        x1="{x1 - px}"

        y1="{y1 - py}"

        x2="{x2 - px}"

        y2="{y2 - py}">

    </line>

    """


    number_of_rungs = max(

        3,

        int(length / 35)

    )


    for i in range(

        1,

        number_of_rungs

    ):

        t = i / number_of_rungs


        cx = x1 + dx * t

        cy = y1 + dy * t


        html += f"""

        <line

            class="ladder-rung"

            x1="{cx + px}"

            y1="{cy + py}"

            x2="{cx - px}"

            y2="{cy - py}">

        </line>

        <line class="ladder-rung-highlight" x1="{cx + px}" y1="{cy + py - 1}" x2="{cx - px}" y2="{cy - py - 1}"></line>

        """


# =========================================================
# JAVASCRIPT
# =========================================================

html += """

</svg>


<script>


// =======================================================
// AUDIO CONTEXT
// =======================================================

let audioContext = null;


function getAudioContext() {

    if (!audioContext) {

        audioContext = new (

            window.AudioContext ||

            window.webkitAudioContext

        )();

    }


    if (audioContext.state === "suspended") {

        audioContext.resume();

    }


    return audioContext;

}


// =======================================================
// LADDER SOUND
// =======================================================

function playLadderSound() {

    try {

        const audio = getAudioContext();

        const oscillator =
            audio.createOscillator();

        const gain =
            audio.createGain();


        oscillator.connect(gain);

        gain.connect(audio.destination);


        oscillator.type = "sine";


        const now = audio.currentTime;


        oscillator.frequency.setValueAtTime(
            300,
            now
        );


        oscillator.frequency.exponentialRampToValueAtTime(
            500,
            now + 0.15
        );


        oscillator.frequency.exponentialRampToValueAtTime(
            750,
            now + 0.30
        );


        oscillator.frequency.exponentialRampToValueAtTime(
            1000,
            now + 0.50
        );


        gain.gain.setValueAtTime(
            0.001,
            now
        );


        gain.gain.exponentialRampToValueAtTime(
            0.25,
            now + 0.05
        );


        gain.gain.exponentialRampToValueAtTime(
            0.001,
            now + 0.60
        );


        oscillator.start(now);

        oscillator.stop(now + 0.60);

    }

    catch (error) {

        console.log(
            "Ladder sound blocked:",
            error
        );

    }

}


// =======================================================
// SNAKE SOUND
// =======================================================

function playSnakeSound() {

    try {

        const audio = getAudioContext();

        const oscillator =
            audio.createOscillator();

        const gain =
            audio.createGain();


        oscillator.connect(gain);

        gain.connect(audio.destination);


        oscillator.type = "sawtooth";


        const now = audio.currentTime;


        oscillator.frequency.setValueAtTime(
            900,
            now
        );


        oscillator.frequency.exponentialRampToValueAtTime(
            180,
            now + 0.75
        );


        gain.gain.setValueAtTime(
            0.001,
            now
        );


        gain.gain.exponentialRampToValueAtTime(
            0.25,
            now + 0.05
        );


        gain.gain.exponentialRampToValueAtTime(
            0.001,
            now + 0.75
        );


        oscillator.start(now);

        oscillator.stop(now + 0.75);

    }

    catch (error) {

        console.log(
            "Snake sound blocked:",
            error
        );

    }

}


// =======================================================
// GET CELL POSITION
// =======================================================

function getCellPosition(number) {


    if (number <= 0) {

        return {

            left: 260,

            top: 20

        };

    }


    const rowFromBottom =

        Math.floor(

            (number - 1) / 10

        );


    let col =

        (number - 1) % 10;


    if (

        rowFromBottom % 2 === 1

    ) {

        col = 9 - col;

    }


    const row =

        9 - rowFromBottom;


    return {

        left:

            col * 55 + 10.5,

        top:

            row * 55 + 8.5

    };

}


// =======================================================
// MOVE PIECE
// =======================================================

function movePiece(

    piece,

    startPosition,

    landingPosition,

    finalPosition,

    moveType

) {


    let current = startPosition;


    // ===================================================
    // SQUARE-BY-SQUARE MOVEMENT
    // ===================================================

    function moveNextSquare() {


        if (

            current < landingPosition

        ) {


            current++;


            const position =

                getCellPosition(

                    current

                );


            piece.style.left =

                position.left + "px";


            piece.style.top =

                position.top + "px";


            setTimeout(

                moveNextSquare,

                300

            );


            return;

        }


        // =================================================
        // LADDER
        // =================================================

        if (

            moveType === "ladder"

        ) {

            piece.classList.add(

                "ladder-effect"

            );


            playLadderSound();


            // Smoothly climb from the landing square to the top.
            const from = getCellPosition(landingPosition);
            const to = getCellPosition(finalPosition);
            const climbDuration = 1100;
            const startTime = performance.now();

            function climbLadder(now) {
                const progress = Math.min(
                    (now - startTime) / climbDuration,
                    1
                );

                const eased = progress < 0.5
                    ? 2 * progress * progress
                    : 1 - Math.pow(-2 * progress + 2, 2) / 2;

                piece.style.left = (
                    from.left + (to.left - from.left) * eased
                ) + "px";
                piece.style.top = (
                    from.top + (to.top - from.top) * eased
                ) + "px";

                if (progress < 1) {
                    requestAnimationFrame(climbLadder);
                } else {
                    piece.classList.remove("ladder-effect");
                    piece.classList.add("token-bounce");
                    setTimeout(function() {
                        piece.classList.remove("token-bounce");
                    }, 450);
                }
            }

            requestAnimationFrame(climbLadder);

            return;

        }


        // =================================================
        // SNAKE
        // =================================================

        if (

            moveType === "snake"

        ) {


            piece.classList.add(

                "snake-effect"

            );


            piece.classList.add(

                "snake-flash"

            );


            playSnakeSound();


            setTimeout(

                function() {


                    piece.classList.remove(

                        "snake-effect"

                    );


                    piece.classList.remove(

                        "snake-flash"

                    );


                    const position =

                        getCellPosition(

                            finalPosition

                        );


                    piece.style.left =

                        position.left + "px";


                    piece.style.top =

                        position.top + "px";


                },

                900

            );


            return;

        }

    }


    moveNextSquare();

}

</script>


</body>

</html>

"""


# Insert the uploaded image markup into the board.
html = html.replace("{board_image_html}", board_image_html)

# =========================================================
# WINNER / RESET
# =========================================================

if st.session_state.winner is not None:
    st.success(f"🏆 {st.session_state.winner} WINS THE GAME! 🎉")
    st.balloons()

if st.button("🔄 New Game / Reset", key="new_game_reset"):
    st.session_state.players = {
        st.session_state.custom_names[i]: 0
        for i in range(num_players)
    }
    st.session_state.current_player = 0
    st.session_state.dice = 1
    st.session_state.last_move = None
    st.session_state.winner = None
    st.rerun()

# =========================================================
# ANIMATION TRIGGER
# =========================================================

if last_move is not None:


    player_number = (

        last_move["player_number"]

    )


    old_position = (

        last_move["old"]

    )


    landing_position = (

        last_move["landing"]

    )


    final_position = (

        last_move["final"]

    )


    move_type = (

        last_move["type"]

    )


    html += f"""

    <script>


    window.addEventListener(

        "load",

        function() {{


            const piece =

                document.getElementById(

                    "piece-{player_number}"

                );


            const dice = document.getElementById("dice-cube");
            const faces = ["⚀","⚁","⚂","⚃","⚄","⚅"];
            if (dice) {{
                dice.classList.remove("dice-roll");
                void dice.offsetWidth;
                dice.classList.add("dice-roll");
                let count = 0;
                const shuffle = setInterval(function() {{
                    dice.textContent = faces[Math.floor(Math.random() * 6)];
                    count++;
                    if (count >= 8) {{
                        clearInterval(shuffle);
                        dice.textContent = faces[{last_move["dice"]} - 1];
                    }}
                }}, 90);
            }}

            if (piece) {{
                piece.classList.add("token-bounce");
                setTimeout(function() {{ piece.classList.remove("token-bounce"); }}, 500);

                movePiece(

                    piece,

                    {old_position},

                    {landing_position},

                    {final_position},

                    "{move_type}"

                );


            }}

        }}

    );


    </script>

    """


# =========================================================
# DISPLAY BOARD
# =========================================================

components.html(

    html,

    height=660,

    scrolling=False

)

