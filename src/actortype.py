import raytrace
import graphics
import itemtype

enum:
    AT_HUNTER
    AT_DOG
    AT_HEALER
    AT_DRAKE
    AT_DRAGON
    AT_GROLL
    AT_PAPAGROLL
    AT_KNIGHT
    AT_MAGE
    AT_BAT
    AT_WOLF
    AT_COUNT

global char const *actor_names[AT_COUNT] = {
    "Hunter",
    "Dog",
    "Healer",
    "Drake",
    "Dragon",
    "Groll",
    "Papa Groll",
    "Knight",
    "Mage",
    "Bat",
    "Wolf",
    }

int levels[AT_COUNT] = {
    4,
    1,
    4,
    19,
    29,
    5,
    23,
    6,
    4,
    3,
    2
    }

class ActorType:
    int w, h
    int level
    int initial_hp
    int initial_damage
    char const *graphics
    LandImage *images[40]
    LandImage *shadows[40]
    Raytracer *traces[40]
    Raytracer *shadow_traces[40]
    bool enemy

    int projectile
    float projectile_speed

    int id

global ActorType *actor_type[AT_COUNT]

static ActorType *global_current
static int thread_data[8]
static LandThread *thread[8]

static def cb(void *data):
    ActorType *self = global_current
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

def actor_render(ActorType *self):
    global_current = self
    for int j in range(5):
        for int i in range(8):
            thread_data[i] = j * 8 + i
            thread[i] = land_thread_new(cb, thread_data + i)
        for int i in range(8):
            land_thread_destroy(thread[i])
        for int i in range(8):
            self->images[j * 8 + i] = land_image_new(self->w, self->h)
            land_image_set_rgba_data(self->images[j * 8 + i],
                self->traces[j * 8 + i]->rgba)

            unsigned char *p = self->shadow_traces[j * 8 + i]->rgba
            for int y in range(self->h):
                for int x in range(self->w):
                    p[0] = p[1] = p[2] = 0
                    p[3] /= 4
                    p += 4
            
            self->shadows[j * 8 + i] = land_image_new(self->w, self->h)
            land_image_set_rgba_data(self->shadows[j * 8 + i],
                self->shadow_traces[j * 8 + i]->rgba)
            

ActorType *def actor_type_new(int w, h, kind):
    ActorType *self; land_alloc(self)
    self->w = w
    self->h = h
    self->level = levels[kind]
    self->initial_hp = 10 * pow(2, (self->level - 1) / 5.0)
    self->initial_damage = pow(2, (self->level - 1) / 5.0)

    # FIXME: levelling isn't implemented right now, so insane damage makes no
    # sense for low level player
    if self->initial_damage > 7:
        self->initial_damage = 7
    
    self->id = kind
    actor_type[kind] = self

    land_clear(1, 1.0 * kind / AT_COUNT, 1, 1)
    land_flip()
    char s[100]
    sprintf(s, "raytracing %d/%d (%s)", kind, AT_COUNT, actor_names[kind])
    land_display_title(s)
    return self  

ActorType *def actor_hunter_new():
    ActorType *self = actor_type_new(32, 32, AT_HUNTER)
    self->projectile = IT_ARROW
    self->projectile_speed = 3
    self->graphics = """
/turquoise
.5z
.75S
(.1trz
(x .5rx .25s2sz-.5zR)
(-x .5rx .25s2sz-.5zR))
(z  .5x -.5z .2trx .25s2sz.5zR)
(z -.5x -.5z -.2trx .25s2sz.5zR)
-z
/pink S
/sienna
(-.1z-.1y S)
.75y
(-.5x.4/whiteS .25y.2/blackS)
( .5x.4/whiteS .25y.2/blackS)"""
    actor_render(self)
    return self

ActorType *def actor_knight_new():
    ActorType *self = actor_type_new(32, 32, AT_KNIGHT)
    self->graphics = """
/silver
.5z
.75S
(.1trz
(x .5rx -.25z (/silver.25s2szR)/palegreen-.5z.05szR)
(-x .5rx -.25z(/silver2sz.25R)/lightcyan-.5z-.4y8sy.1B))
/silver
(z  .5x -.5z .2trx .25s2sz.5zR)
(z -.5x -.5z -.2trx .25s2sz.5zR)
-z
/pink S
/silver
(-.1z-.1y S)
.75y
(-.5x.4/whiteS .25y.2/blackS)
( .5x.4/whiteS .25y.2/blackS)"""
    actor_render(self)
    return self

ActorType *def actor_healer_new():
    ActorType *self = actor_type_new(32, 32, AT_HEALER)
    self->projectile = IT_HEAL
    self->projectile_speed = 5
    self->graphics = """
/white
.5z
.75S
(.1trz
(x .5rx .25s2sz-.5zR)
(-x .5rx .25s2sz-.5zR))
(z  .5x -.5z .2trx .25s2sz.5zR)
(z -.5x -.5z -.2trx .25s2sz.5zR)
-z
/pink S
/black
(
-.1y(rzH) (-.5z.2szR) /white -.9z.2szR
) #hair
.75y
(-.5x.4/whiteS .25y.2/blackS)
( .5x.4/whiteS .25y.2/blackS)"""
    actor_render(self)
    return self


ActorType *def actor_mage_new():
    ActorType *self = actor_type_new(32, 32, AT_MAGE)
    self->projectile = IT_MAGIC_MISSILE
    self->projectile_speed = 4
    self->graphics = """
/orchid
.5z
.75S
(.1trz
(x .5rx .25s2sz-.5zR)
(-x .5rx -.25z(2sz.25R)/yellow-.5z-.4y8sy.1R))
/orchid
(z  .5x -.5z .2trx .25s2sz.5zR)
(z -.5x -.5z -.2trx .25s2sz.5zR)
-z
/pink S
/maroon
(
-.1y(.75szrzH) (-.5z.2szR) /plum -z.4szrx.5zC
) #hair
.75y
(-.5x.4/whiteS .25y.2/blackS)
( .5x.4/whiteS .25y.2/blackS)"""
    actor_render(self)
    return self

ActorType *def actor_drake_new():
    ActorType *self = actor_type_new(64, 64, AT_DRAKE)
    self->projectile = IT_FIREBALL
    self->projectile_speed = 5
    self->enemy = True
    self->graphics = """
1.7s
-.2y
/chartreuse
.75S #body
(-y2sy.5rx.3C) # tail
# wings
(.5x .2try x .5rx .7s.25sy B)
(-.5x -.2try -x .5rx .7s.25sy B)
# feet
(-.5z .3y
(z  .5x -.2trx .25s2sz.5zR)
(z -.5x -.2trx .25s2sz.5zR))
(-.5z -.3y
(z -.5x .2trx .25s2sz.5zR)
(z .5x .2trx .25s2sz.5zR))
-z
.5y
S
(1.2rx(1.2z.2C) 8{-.1rx(1.2z.2C)} )
(.2zy1.5sy.7S)
# eyes
.8y
-.4z
(-.6x.3/whiteS .25y.2/blackS)
( .6x.3/whiteS .25y.2/blackS)
"""
    actor_render(self)
    return self

ActorType *def actor_dragon_new():
    ActorType *self = actor_type_new(112, 112, AT_DRAGON)
    self->projectile = IT_FIREBALL
    self->projectile_speed = 5
    self->enemy = True
    self->graphics = """
2.5s
-.5y
/deeppink
.75S #body
(-y3sy.5rx.3C) # tail
# wings
(.5x .2try .2rz 3{(x.5ry4sz.25C)-.2rz})
(-.5x -.2try .2rz 3{(-x-.5ry4sz.25C)-.2rz})
# feet
(-.5z .3y
(z  .5x -.2trx .25s2sz.5zC)
(z -.5x -.2trx .25s2sz.5zC))
(-.5z -.3y
(z -.5x .2trx .25s2sz.5zC)
(z .5x .2trx .25s2sz.5zC))
-z
.5y
S
(1.2rx(1.2z.2C) 8{-.1rx(1.2z.2C)} )
(.2zy1.5syS) #nose
# eyes
.8y
-.4z
(-.6x.3/whiteS .25y.2/blackS)
( .6x.3/whiteS .25y.2/blackS)
"""
    actor_render(self)
    return self

ActorType *def actor_dog_new():
    ActorType *self = actor_type_new(20, 20, AT_DOG)
    self->graphics = """
0.5s
-.2y.7z
/peru
.75S #body
(-y2sy.5rx.3S) # tail
# feet
(-.5z .3y
(z  .5x -.2trx .25s2sz.5zR)
(z -.5x -.2trx .25s2sz.5zR))
(-.5z -.3y
(z -.5x .2trx .25s2sz.5zR)
(z .5x .2trx .25s2sz.5zR))
-z
.5y
S # head
(.2zy1.5sy.7S) # nose


# ears
(-.3y-.6z
(-.6x.4S)
(.6x.4S)
)
# eyes
.8y
-.4z
(-.6x.3/whiteS .25y.2/blackS)
( .6x.3/whiteS .25y.2/blackS)
"""
    actor_render(self)
    return self

ActorType *def actor_groll_new():
    ActorType *self = actor_type_new(32, 32, AT_GROLL)
    self->enemy = True
    self->graphics = """
.2tz
S
/red
.8y
(-.5x.3S)
(.5x.3S)
"""
    actor_render(self)
    return self

ActorType *def actor_papagroll_new():
    ActorType *self = actor_type_new(64, 64, AT_PAPAGROLL)
    self->enemy = True
    self->graphics = """
2s
.2tz
S
/red
.8y
(-.5x.3S)
(.5x.3S)
"""
    actor_render(self)
    return self

ActorType *def actor_bat_new():
    ActorType *self = actor_type_new(32, 32, AT_BAT)
    self->enemy = True
    self->graphics = """
/maroon
.2tz
S
(-.5y
(x.3try.1szryH)
(-x-.3try.1szryH))
/yellow
.8y
(-.5x.3S)
(.5x.3S)
"""
    actor_render(self)
    return self

ActorType *def actor_wolf_new():
    ActorType *self = actor_type_new(32, 32, AT_WOLF)
    self->enemy = True
    self->graphics = """
0.8s
-.2y.7z
/wheat
.75S #body
(-y2sy.5rx.3S) # tail
# feet
(-.5z .3y
(z  .5x -.2trx .25s2sz.5zR)
(z -.5x -.2trx .25s2sz.5zR))
(-.5z -.3y
(z -.5x .2trx .25s2sz.5zR)
(z .5x .2trx .25s2sz.5zR))
-z
.5y
S # head
(.2zy-.5rx.7C) # nose


# ears
(-.3y-z
(-.3xry.5C)
(.3xry.5C)
)
# eyes
.8y
-.4z
(-.6x.3/tomato S .25y.2/blackS)
( .6x.3/springgreen S .25y.2/blackS)
"""
    actor_render(self)
    return self

def actor_types_init():
    actor_papagroll_new()
    actor_dragon_new()
    actor_wolf_new()
    actor_bat_new()
    actor_mage_new()
    actor_hunter_new()
    actor_knight_new()
    actor_healer_new()
    actor_dog_new()
    actor_groll_new()
    actor_drake_new()
