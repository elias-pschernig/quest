import itemtype
import actor

class Item:
    int kind
    float x, y
    float angle

Item *def item_new(int kind, float x, y, angle):
    if not kind:
        return None
    Item *self; land_alloc(self)
    self->kind = kind
    self->x = x
    self->y = y
    self->angle = angle
    return self

def item_place(Item *i):
    if not i:
        return
    int x = i->x / tile_w
    int y = i->y / tile_h
    x %= app->actors->w
    app->actors->tilemap[y * app->actors->w + x].item = i

def item_remove(Item *i):
    if not i:
        return
    int x = i->x / tile_w
    int y = i->y / tile_h
    x %= app->actors->w
    app->actors->tilemap[y * app->actors->w + x].item = None


def item_draw(Item *self):
    int d = round(self->angle * 8 / (2 * pi) - 2)
    d &= 7
    LandImage *im = item_types[self->kind]->images[d]
    int w = land_image_width(im)
    int h = land_image_height(im)
    land_image_draw(im, self->x - w / 2, self->y - h)
    #land_color(1, 0, 0, 1)
    #land_rectangle(self->x - w / 2, self->y - h, self->x + w / 2, self->y)

def item_draw_shadow(Item *self):
    int d = round(self->angle * 8 / (2 * pi) - 2)
    d &= 7
    LandImage *im = item_types[self->kind]->shadows[d]
    int w = land_image_width(im)
    int h = land_image_height(im)
    land_image_draw_scaled(im, self->x - w / 2, self->y - h / 4 - h / 8, 1, 0.5)
