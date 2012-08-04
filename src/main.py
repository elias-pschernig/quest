import common
import raytrace
import color
import graphics
import actor

global char *main_data_path
LandFont *font

Actor *hunter
Actor *dragon

bool debug_lines

def runner_init(LandRunner *self):
    land_clear(0, 0, 1, 1)
    land_flip()
    land_display_title("TINS 2012")

    font = land_font_load("data/6x6.png", 0)

    hunter = actor_new()

def runner_done(LandRunner *self):
    pass

def runner_update(LandRunner *self):
    if land_closebutton():
        land_quit()

    if not land_keybuffer_empty():
        int k, u
        land_keybuffer_next(&k, &u)

        if k == LandKeyEscape:
            land_quit()

        if k == LandKeyFunction + 1:
            debug_lines ^= 1

def draw_colors():
    int x = 2
    int y = 2
    for int i = 0 while colors[i].name with i++:
        land_text_pos(x + 25, y)
        land_color(0, 0, 0, 1)
        land_print(colors[i].name)
        float r = colors[i].r / 255.0
        float g = colors[i].g / 255.0
        float b = colors[i].b / 255.0
        land_color(r, g, b, 1)
        land_filled_rectangle(x, y, x + 20, y + 10)
        y += 12
        if y + 10 > 360:
            y = 2
            x += 120

def runner_redraw(LandRunner *self):
    land_clear(1, 1, 0.75, 1)
    
    Actor *actor = hunter
    for int i in range(40):
        if not actor->images[i]: continue
        land_reset_transform()
        land_image_draw_scaled(actor->images[i], (i & 7) * 32,
            (i >> 3) * 32, 1, 1)

        if debug_lines:
            land_color(1, 0, 0, 1)
            land_scale(0.25, 0.25)
            land_translate((i & 7) * 32 + 16, (i >> 3) * 32 + 16)
            raytracer_draw_lines(actor->traces[i])

int def my_main():
    int w = 640
    int h = 360

    main_data_path = land_strdup(".")

    land_init()
    land_set_display_parameters(w, h, LAND_MULTISAMPLE)
    LandRunner *game_runner = land_runner_new("TINS 2012",
        runner_init,
        None,
        runner_update,
        runner_redraw,
        None,
        runner_done)

    land_runner_register(game_runner)
    land_set_initial_runner(game_runner)
    land_mainloop()

    land_free(main_data_path)

    return 0

land_use_main(my_main)

