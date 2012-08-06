import raytrace
import graphics

class ItemType:
    int id
    int w, h
    char const *graphics
    LandImage *images[8]
    LandImage *shadows[8]
    Raytracer *traces[8]
    Raytracer *shadow_traces[8]

enum:
    IT_NONE
    IT_MOUNTAIN
    IT_CLOUD
    IT_CLOUD2
    IT_WALL
    IT_WALL2
    IT_CHEESE
    IT_ARROW
    IT_MAGIC_MISSILE
    IT_HEAL
    IT_FIREBALL
    IT_COUNT

global ItemType *item_types[IT_COUNT]

static ItemType *global_current
static int thread_data[8]
static LandThread *thread[8]

static def cb(void *data):
    ItemType *self = global_current
    int *ip = data
    int i = *ip
    Land4x4Matrix t = land_4x4_matrix_identity()
    t = land_4x4_matrix_mul(land_4x4_matrix_rotate(1, 0, 0, pi * -0.333), t)
    t = land_4x4_matrix_mul(t, land_4x4_matrix_rotate(0, 0, 1, 2 * pi * (i & 7) / 8))
    t = land_4x4_matrix_mul(t, land_4x4_matrix_scale(32, 32, 32))
    self->traces[i] = graphics_parse(self->graphics, self->w * 4, self->h * 4,
        t, (i >> 3) / 2.0 - 1.0)

    t = land_4x4_matrix_identity()
    t = land_4x4_matrix_mul(t, land_4x4_matrix_rotate(0, 0, 1, 2 * pi * (i & 7) / 8))
    t = land_4x4_matrix_mul(t, land_4x4_matrix_scale(32, 32, 32))
    self->shadow_traces[i] = graphics_parse(self->graphics, self->w * 4, self->h * 4,
        t, (i >> 3) / 2.0 - 1.0)

def item_type_render(ItemType *self):
    global_current = self
   
    for int i in range(8):
        thread_data[i] = i
        thread[i] = land_thread_new(cb, thread_data + i)
    for int i in range(8):
        land_thread_destroy(thread[i])
    for int i in range(8):
        self->images[i] = land_image_new(self->w, self->h)
        land_image_set_rgba_data(self->images[i],
            self->traces[i]->rgba)

        unsigned char *p = self->shadow_traces[i]->rgba
        for int y in range(self->h):
            for int x in range(self->w):
                p[0] = p[1] = p[2] = 0
                p[3] /= 4
                p += 4
        
        self->shadows[i] = land_image_new(self->w, self->h)
        land_image_set_rgba_data(self->shadows[i],
            self->shadow_traces[i]->rgba)

ItemType *def item_type_new(char const *script, int w, h, id):
    ItemType *self; land_alloc(self)
    self->id = id
    item_types[id] = self
    self->w = w
    self->h = h

    self->graphics = script

    item_type_render(self)

    return self

def items_init():
    item_type_new("""
/olive
ry
2.5P
-z
1.5x.2rz1.5P
""", 64, 64, IT_MOUNTAIN)

    item_type_new("""
/lightcyan
2S
zy2x1.5S
1x-1y1S
""", 64, 64, IT_CLOUD)

    item_type_new("""
/lightblue
.6s
2S
zy2x1.5S
1x-1y1S
""", 64, 64, IT_CLOUD2)

    item_type_new("""
/peru
.1rz
1B
""", 32, 32, IT_WALL)

    item_type_new("""
/brown
.1rz
3szB
""", 32, 64, IT_WALL2)

    item_type_new("""
/gold
.5sz1.1rzT
""", 16, 16, IT_CHEESE)

    item_type_new("""
/moccasin
.5rx10sz.1R
""", 16, 16, IT_ARROW)

    item_type_new("""
/hotpink
.5rx5szry.2C
""", 16, 16, IT_MAGIC_MISSILE)

    item_type_new("""
/white
.5S
""", 16, 16, IT_HEAL)

    item_type_new("""
/orange
S
""", 16, 16, IT_FIREBALL)
