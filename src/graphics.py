import common
import object
import color

static class ParserState:
    float value
    bool negative
    int place
    Land4x4Matrix m
    int st
    Land4x4Matrix stack[16]
    float red, green, blue, alpha

static def reset(ParserState *s):
    s->value = 0
    s->negative = False
    s->place = 0

static def finish(ParserState *s):
    if s->place == 0:
        s->value = 1
        s->place = 1
    if s->negative:
        s->value = -s->value
        s->negative = False

Raytracer *def graphics_parse(char const *script, int w, h,
        Land4x4Matrix matrix, double dt):
    """
    S sphere
    C cone
    B box
    R rod
    x/y/z translate
    s/sx/sy/sz scale
    rx/ry/rz rotate
    () preserve transformation
    t multiply number with time
    <number> value for following command
    <name> color    
    """
    Raytracer *r = raytracer_new(w, h)
    LandVector light = land_vector(0, 0, 1)
    light = land_vector_rotate(light, land_vector(0, 1, 0), pi / 4)
    light = land_vector_rotate(light, land_vector(0, 1, 0), pi / 4)
    light = land_vector_rotate(light, land_vector(0, 0, 1), pi / 4)
    raytracer_add_light(r, light)
    char c
    ParserState s
    memset(&s, 0, sizeof s)
    s.m = matrix
    s.alpha = 1
    for int i = 0 while (c = script[i]) with i++:
        char n = script[i + 1]
        if c == '-':
            s.negative = True
        elif c == '.':
            s.place = -1
        elif c == 't':
            finish(&s)
            s.value *= dt
        elif c >= '0' and c <= '9':
            float v = c - '0'
            s.value += pow(10, s.place) * v
            if s.place < 0:
                s.place--
            else:
                s.place++
        elif c == '(':
            s.stack[s.st++] = s.m
        elif c == ')':
            s.m = s.stack[--s.st]
        elif c == 'x' or c == 'y' or c == 'z':
            finish(&s)
            float x = c == 'x' ? s.value : 0
            float y = c == 'y' ? s.value : 0
            float z = c == 'z' ? s.value : 0
            Land4x4Matrix m = land_4x4_matrix_translate(x, y, z)
            s.m = land_4x4_matrix_mul(s.m, m)
            reset(&s)
        elif c == 'r' and (n == 'x' or n == 'y' or n == 'z'):
            finish(&s)
            LandVector a = land_vector(1, 0, 0)
            if c == 'y': a = land_vector(0, 1, 0)
            if c == 'z': a = land_vector(0, 0, 1)
            Land4x4Matrix m = land_4x4_matrix_rotate(a.x, a.y, a.z, pi * s.value)
            s.m = land_4x4_matrix_mul(s.m, m)
            reset(&s)
            i++
        elif c == 's':
            finish(&s)
            float x = s.value
            float y = s.value
            float z = s.value
            if n == 'x':
                i++
                y = z = 1
            if n == 'y':
                i++
                x = z = 1
            if n == 'z':
                i++
                y = x = 1

            Land4x4Matrix m = land_4x4_matrix_scale(x, y, z)
            s.m = land_4x4_matrix_mul(s.m, m)
            reset(&s)

        elif c == 'S':
            finish(&s)
            Object *o = object_sphere(16, 16)
            object_rgba(o, s.red, s.green, s.blue, s.alpha)
            Land4x4Matrix t = land_4x4_matrix_mul(s.m, land_4x4_matrix_scale(
                s.value, s.value, s.value))
            object_transform(o, &t)
            raytracer_add_object(r, o)
            reset(&s)
        elif c == 'R':
            finish(&s)
            Object *o = object_cylinder(16, True, True)
            object_rgba(o, s.red, s.green, s.blue, s.alpha)
            Land4x4Matrix t = land_4x4_matrix_mul(s.m, land_4x4_matrix_scale(
                s.value, s.value, s.value))
            object_transform(o, &t)
            raytracer_add_object(r, o)
            reset(&s)
        elif c == '/':
            for int ic = 0 while colors[ic].name with ic++:
                if not strncmp(colors[ic].name, script + i + 1,
                        strlen(colors[ic].name)):
                    i += strlen(colors[ic].name)
                    s.red = colors[ic].r / 255.0
                    s.green = colors[ic].g / 255.0
                    s.blue = colors[ic].b / 255.0
                    break
    unsigned char *rgba = land_malloc(w * h * 4)
    raytracer_trace(r, rgba)
    unsigned char *p2 = r->rgba
    for int y in range(h >> 2):
        for int x in range(w >> 2):
            int cr = 0, cg = 0, cb = 0, ca = 0
            for int v in range(4):
                for int u in range(4):
                    unsigned char *p = rgba + (y * 4 + v) * w * 4 + (x * 4 + u) * 4
                    cr += p[0]
                    cg += p[1]
                    cb += p[2]
                    ca += p[3]

            p2[0] = cr >> 4
            p2[1] = cg >> 4
            p2[2] = cb >> 4
            p2[3] = ca >> 4
            p2 += 4
    land_free(rgba)
    return r

