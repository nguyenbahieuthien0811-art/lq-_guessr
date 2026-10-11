# main.py--

### Imports 
import asyncio
import random
import flet as ft

### LOCATIONS 
LOCATIONS = [
    {"name": "Căng tin", "image": "can_tin.jpg"},
    {"name": "Tượng LQĐ", "image": "tuong_lqd.jpg"},
    {"name": "Cổng Võ Văn Tần", "image": "cong_vo_van_tan.jpg"},
    {"name": "Hầm xe", "image": "ham_xe.jpg"},
    {"name": "Khu A", "image": "khu_A.jpg"},
    {"name": "Khu biệt thự", "image": "khu_biet_thu.jpg"},
    {"name": "Sân đá banh", "image": "san_da_banh.jpg"},
    {"name": "Thư viện 1", "image": "thu_vien_1.jpg"},
    {"name": "Thư viện 2", "image": "thu_vien_2.jpg"},
]


### DATA 
CHOICES_PER_ROUND = 4

NEXT_ROUND_DELAY = 3

IMAGE_FOLDER = "images"

VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 380

PANORAMA_WIDTH = 1800

### MAIN 
def main(page: ft.Page):


    # PAGE SETTINGS


    page.title = "SchoolGuessr"

    page.window.width = 800
    page.window.height = 750
    page.window.resizable = True

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.padding = 30

    page.bgcolor = ft.Colors.BLUE_GREY_50


    # CHECK LOCATIONS

    if len(LOCATIONS) < CHOICES_PER_ROUND:

        page.add(
            ft.Text(
                f"You need at least {CHOICES_PER_ROUND} locations.",
                color=ft.Colors.RED,
                size=16,
            )
        )

        return


    # GAME STATE

    state = {

        "round_locations": [],

        "round_index": 0,

        "answered": False,

        # Current correct answer
        "correct_answer": "",
    }



    # IMAGE ERROR TEXT

    image_error_text = ft.Text(
        "",
        color=ft.Colors.RED_700,
        size=14,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )


    # PANORAMA IMAGE

    panorama_image = ft.Image(

        src="",

        width=PANORAMA_WIDTH,

        height=VIEWPORT_HEIGHT,

        fit=ft.BoxFit.COVER,

        left=0,

        top=0,

        error_content=ft.Container(
            content=ft.Column(
                [
                    image_error_text
                ],

                alignment=ft.MainAxisAlignment.CENTER,

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
            ),

            width=PANORAMA_WIDTH,

            height=VIEWPORT_HEIGHT,
        ),
    )



    # PANORAMA DRAG

    def on_pan_update(e: ft.DragUpdateEvent):

        min_left = -(
            PANORAMA_WIDTH - VIEWPORT_WIDTH
        )

        max_left = 0


        new_left = (
            panorama_image.left
            + e.local_delta.x
        )


        new_left = max(
            min_left,
            min(max_left, new_left)
        )


        panorama_image.left = new_left

        page.update()



    # VIEWPORT

    viewport = ft.Container(

        width=VIEWPORT_WIDTH,

        height=VIEWPORT_HEIGHT,

        clip_behavior=ft.ClipBehavior.HARD_EDGE,

        border_radius=12,

        bgcolor=ft.Colors.BLACK12,

        content=ft.Stack(
            [
                panorama_image
            ]
        ),
    )



    # DRAG AREA

    panorama_drag_area = ft.GestureDetector(

        content=viewport,

        drag_interval=10,

        on_pan_update=on_pan_update,

        mouse_cursor=ft.MouseCursor.MOVE,
    )



    # TEXT

    drag_hint = ft.Text(

        "🖱️ Click and drag the photo to look around",

        size=12,

        italic=True,

        color=ft.Colors.BLUE_GREY_400,
    )


    round_label = ft.Text(

        "",

        size=14,

        weight=ft.FontWeight.BOLD,

        color=ft.Colors.BLUE_GREY_700,
    )


    feedback_text = ft.Text(

        "",

        size=18,

        weight=ft.FontWeight.BOLD,
    )


    countdown_text = ft.Text(

        "",

        size=13,

        italic=True,

        color=ft.Colors.BLUE_GREY_400,
    )



    # ANSWER BUTTONS

    choices_row = ft.Column(

        spacing=10
    )



    # GAME VIEW

    game_view = ft.Column(

        controls=[

            ft.Row(
                [
                    round_label
                ],

                alignment=ft.MainAxisAlignment.CENTER,

                width=VIEWPORT_WIDTH,
            ),

            panorama_drag_area,

            drag_hint,

            choices_row,

            feedback_text,

            countdown_text,
        ],

        horizontal_alignment=(
            ft.CrossAxisAlignment.CENTER
        ),

        spacing=12,
    )



    # START GAME

    def start_game():

        state["round_locations"] = random.sample(
            LOCATIONS,
            k=len(LOCATIONS)
        )

        state["round_index"] = 0

        load_round()



    # LOAD ROUND

    def load_round():

        state["answered"] = False


        feedback_text.value = ""

        countdown_text.value = ""



        # CURRENT LOCATION


        current = state["round_locations"][
            state["round_index"]
        ]


        # Save correct answer
        state["correct_answer"] = current["name"]



        # IMAGE


        panorama_image.src = (
            f"{IMAGE_FOLDER}/{current['image']}"
        )


        image_error_text.value = (

            f"⚠️ Couldn't load:\n"

            f"{IMAGE_FOLDER}/{current['image']}\n\n"

            f"Check that this file exists in your "
            f"images folder."
        )



        # CENTER PANORAMA

        panorama_image.left = -(
            PANORAMA_WIDTH - VIEWPORT_WIDTH
        ) / 2



        # ROUND NUMBER

        round_label.value = (

            f"Round "
            f"{state['round_index'] + 1} / "
            f"{len(state['round_locations'])}"
        )



        # CREATE WRONG ANSWERS

        wrong_pool = [

            loc

            for loc in LOCATIONS

            if loc["name"] != current["name"]
        ]


        wrong_choices = random.sample(

            wrong_pool,

            k=CHOICES_PER_ROUND - 1
        )


        # Add correct answer
        options = wrong_choices + [current]


        # Shuffle answers
        random.shuffle(options)



        # REMOVE OLD BUTTONS

        choices_row.controls.clear()



        # CREATE BUTTONS

        for option in options:

            button = ft.Button(

                content=option["name"],

                # Store answer inside button
                data=option["name"],

                width=VIEWPORT_WIDTH,

                height=45,

                # IMPORTANT:
                # Directly use async function.
                #
                # DO NOT use lambda here.

                on_click=check_answer,

                style=ft.ButtonStyle(

                    bgcolor=ft.Colors.WHITE,

                    color=ft.Colors.BLUE_GREY_900,
                ),
            )


            choices_row.controls.append(button)


        page.update()



    ### CHECK ANSWER 

    async def check_answer(e):

        # PREVENT DOUBLE CLICK

        if state["answered"]:

            return


        state["answered"] = True



        # GET PLAYER ANSWER

        chosen_answer = e.control.data



        # GET CORRECT ANSWER

        correct_answer = state["correct_answer"]



        ### COLOR BUTTONS 
 
        for btn in choices_row.controls:

            # Disable button
            btn.disabled = True



            # CORRECT ANSWER = GREEN

            if btn.data == correct_answer:

                btn.style = ft.ButtonStyle(

                    bgcolor=ft.Colors.GREEN_500,

                    color=ft.Colors.WHITE,
                )



            # PLAYER'S WRONG ANSWER = RED

            elif btn.data == chosen_answer:

                btn.style = ft.ButtonStyle(

                    bgcolor=ft.Colors.RED_500,

                    color=ft.Colors.WHITE,
                )



        ### FEEDBACK 

        if chosen_answer == correct_answer:

            feedback_text.value = "Correct! ✅"

            feedback_text.color = (
                ft.Colors.GREEN_700
            )


        else:

            feedback_text.value = (

                f"❌ Sai — "
                f"đáp án đúng là: "
                f"{correct_answer}"
            )

            feedback_text.color = (
                ft.Colors.RED_700
            )



        ### UPDATE UI IMMEDIATELY 

        page.update()



        ### COUNTDOWN 

        for remaining in range(
            NEXT_ROUND_DELAY,
            0,
            -1
        ):

            countdown_text.value = (

                f"Next round in "
                f"{remaining}..."
            )


            page.update()



            await asyncio.sleep(1)



        ### NEXT ROUND 

        next_round()



    ### NEXT ROUND 

    def next_round():

        state["round_index"] += 1


        if (
            state["round_index"]
            >= len(state["round_locations"])
        ):

            show_results()


        else:

            load_round()



    ### GAME OVER 

    def show_results():

        page.clean()


        page.add(

            ft.Column(

                controls=[

                    ft.Text(

                        "Game Over!",

                        size=32,

                        weight=ft.FontWeight.BOLD,
                    ),


                    ft.Text(

                        f"You went through all "
                        f"{len(state['round_locations'])} "
                        f"locations!",

                        size=18,

                        color=ft.Colors.BLUE_GREY_700,
                    ),


                    ft.Button(

                        content="Play Again",

                        on_click=lambda e: restart(),

                        style=ft.ButtonStyle(

                            bgcolor=ft.Colors.BLUE_600,

                            color=ft.Colors.WHITE,
                        ),
                    ),
                ],

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=20,
            )
        )


        page.update()



    ### RESTART 

    def restart():

        page.clean()

        page.add(game_view)

        start_game()



    ### RUN GAME 


    page.add(game_view)

    start_game()



### START APPLICATION 

if __name__ == "__main__":

    ft.run(main)









