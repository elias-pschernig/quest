import raytrace
import graphics

class Actor:
    char const *graphics
    LandImage *images[40]
    Raytracer *traces[40]

static Actor *global_current
static int thread_data[8]
static LandThread *thread[8]

static def cb(void *data):
    Actor *self = global_current
    int *ip = data
    int i = *ip
    Land4x4Matrix t = land_4x4_matrix_identity()
    t = land_4x4_matrix_mul(land_4x4_matrix_rotate(1, 0, 0, pi * -0.333), t)
    t = land_4x4_matrix_mul(t, land_4x4_matrix_rotate(0, 0, 1, 2 * pi * (i & 7) / 8))
    #t = land_4x4_matrix_mul(t, land_4x4_matrix_rotate(1, 0, 0, pi * -0.25))
    t = land_4x4_matrix_mul(t, land_4x4_matrix_scale(32, 32, 32))
    self->traces[i] = graphics_parse(self->graphics, 128, 128, t,
        (i >> 3) / 2.0 - 1.0)

def actor_render(Actor *self):
    global_current = self
    for int j in range(5):
        for int i in range(8):
            thread_data[i] = j * 8 + i
            thread[i] = land_thread_new(cb, thread_data + i)
        for int i in range(8):
            land_thread_destroy(thread[i])
        for int i in range(8):
            self->images[j * 8 + i] = land_image_new(32, 32)
            land_image_set_rgba_data(self->images[j * 8 + i],
                self->traces[j * 8 + i]->rgba)

Actor *def actor_new():
    Actor *self; land_alloc(self)
    return self

Actor *def actor_human_new():
    Actor *self = actor_new()
    self->graphics = """
/turquoise
.75S
(x .5rx .25s2sz-.5zR)
(-x .5rx .25s2sz-.5zR)
(z  .5x .2trx .25s2sz-.5zR)
(z -.5x -.2trx .25s2sz-.5zR)
-z
/pink S
/sienna
(-.1z-.1y S)
.75y
(-.5x.4/whiteS .25y.2/blackS)
( .5x.4/whiteS .25y.2/blackS)"""
    actor_render(self)
    return self
