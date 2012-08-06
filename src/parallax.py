import common
import main

class Parallax:
    LandImage *sky
    LandImage *ground
    LandArray *layers[4] # Item

static Parallax *parallax

static float scrollpos(float w):
    return fmod(fmod(app->parallax_scroll, w) + w, w)

def parallax_init():
    land_alloc(parallax)
    parallax->sky = land_image_new(8, 5)
    parallax->ground = land_image_new(1280 / 20, 160 / 20)

    for int layer in range(4):
        parallax->layers[layer] = land_array_new()

    for int i in range(0, 1280, 40):
        float angle = land_rnd(0, 2 * pi)
        float x = i + land_rnd(0, 80)
        float y = land_rnd(120, 150)
        Item *it = item_new(IT_CLOUD2, x, y, angle)
        land_array_add(parallax->layers[0], it)

    for int i in range(0, 1280, 80):
        float angle = land_rnd(0, 2 * pi)
        float x = i + land_rnd(0, 80)
        float y = land_rnd(150, 180)
        Item *it = item_new(IT_CLOUD, x, y, angle)
        land_array_add(parallax->layers[1], it)

    for int i in range(0, 1280, 100):
        float angle = land_rnd(0, 2 * pi)
        float x = i + land_rnd(0, 50)
        float y = 200
        Item *it = item_new(IT_MOUNTAIN, x, y, angle)
        land_array_add(parallax->layers[2], it)

    for int i in range(0, 1280, 100):
        float angle = land_rnd(0, 2 * pi)
        float x = i + land_rnd(0, 80)
        float y = land_rnd(220, 240)
        Item *it = item_new(land_rand(0, 1) ? IT_WALL : IT_WALL2,
            x, y, angle)
        land_array_add(parallax->layers[3], it)

    unsigned char rgba[8 * 5 * 4]
    memset(rgba, 0, sizeof rgba)
    unsigned char *p = rgba
    for int y in range(5):
        for int x in range(8):
            if y == 0 or y == 1:
                p[0] = 0x80
                p[1] = 0xc0
                p[2] = 0xff
            elif y == 2:
                p[0] = 0
                p[1] = 0x80
                p[2] = 0xff
            elif y == 3:
                p[0] = 0
                p[1] = 0
                p[2] = 0xff
            elif y == 4:
                p[0] = 150
                p[1] = 150
                p[2] = 125
            else:
                p[0] = 0x80
                p[1] = 0x80
                p[2] = 0x80
            p[3] = 255
            p += 4

    p = rgba + 4
    p[0] = 0xff
    p[1] = 0xff

    p = rgba + 4 + 4 * 8 * 4
    p[1] = 0x80

    p = rgba + 4 + 7 * 8 * 4
    p[2] = 0xff
   
    land_image_set_rgba_data(parallax->sky, rgba)

    unsigned char rgba2[64 * 8 * 4]
    p = rgba2
    for int y in range(8):
        unsigned char *row = p
        for int x in range(64):
            if x == 63:
                p[0] = row[0]
                p[1] = row[1]
                p[2] = row[2]
            else:
                p[0] = land_rand(150, 200)
                p[1] = land_rand(150, 175)
                p[2] = land_rand(125, 150)
            p[3] = 255
            p += 4
    land_image_set_rgba_data(parallax->ground, rgba2)

def parallax_draw():

    for int i in range(2):
        land_push_transform()
        float x = scrollpos(app->w * 4)
        land_translate(-x / 4 + app->w * i, 0)
        land_image_draw_scaled(parallax->sky, 0, 0, 160, 45)
        land_pop_transform()
    
    for int layer in range(4):
        for int i in range(2):
            land_push_transform()
            float x = scrollpos(app->w * (4 - layer))
            land_translate(-x / (4 - layer) + app->w * i, 0)

            if layer == 3:
                land_image_draw_scaled(parallax->ground, 0, 200, 20, 20)

            for Item *it in LandArray *parallax->layers[layer]:
                item_draw(it)
                
            land_pop_transform()
