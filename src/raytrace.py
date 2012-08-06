import common
import global land.util3d
import object

typedef LandVector Vector
typedef LandFloat Float

class Triangle:
    Vector a, b, c
    Vector n
    Object *o

class Ray:
    Vector a, u

class Raytracer:
    int w, h
    Vector light
    LandArray *objects
    LandArray **tiles
    unsigned char *rgba

static Float def ray_intersects_triangle_optimized(Ray ray, Triangle tri):
    """
    If the ray originating at pos, running into dir, hits the triangle defined
    by its vertices v0, v1, v2, return 1 and store the point of collision in
    result. Otherwise return 0 and store nothing.

    Triangles are one-sided.
    """

    Vector eu = land_vector_sub(tri.b, tri.a)
    Vector ev = land_vector_sub(tri.c, tri.a)

    float det = eu.x * ev.y - eu.y * ev.x

    # cull if in triangle plane, or hit backface 
    if det <= 0: return 0

    Vector vt = land_vector_sub(ray.a, tri.a)

    Float u = vt.x * ev.y - vt.y * ev.x
    if u < 0 or u > det: return 0

    Vector cu = land_vector_cross(vt, eu)
    
    Float v = -cu.z
    if v < 0 or u + v > det: return 0

    Float t = land_vector_dot(ev, cu)
    if t < 0: return 0

    t /= det
    return t

Raytracer *def raytracer_new(int w, h):
    Raytracer *self; land_alloc(self)
    self->objects = land_array_new()
    self->w = w
    self->h = h
    self->tiles = land_calloc(w / 8 * h / 8 * sizeof *self->tiles)
    self->rgba = land_malloc(w / 4 * h / 4 * 4 * sizeof *self->rgba)
    return self

def raytracer_add_object(Raytracer *self, Object *o):
    land_array_add(self->objects, o)

def raytracer_add_light(Raytracer *self, Vector v):
    self->light = v

def minmax3(float a, b, c, *vmin, *vmax):
    if a < b:
        if a < c:
            *vmin = a
            if b < c:
                *vmax = c
            else:
                *vmax = b
        else:
            *vmin = c
            *vmax = b
    else:
        if a < c:
            *vmin = b
            *vmax = c
        else:
            *vmax = a
            if b < c:
                *vmin = b
            else:
                *vmin = c

unsigned char *def raytracer_trace(Raytracer *self):
    float *zbuffer = land_calloc(self->w * self->h * sizeof *zbuffer)
    unsigned char *rgba = land_calloc(self->w * self->h * 4)

    for Object *o in LandArray *self->objects:
        object_recalc_normals(o)
        for Triangle *tri in LandArray *o->soup:
            float minx, miny, maxx, maxy
            minmax3(tri->a.x, tri->b.x, tri->c.x, &minx, &maxx)
            minmax3(tri->a.y, tri->b.y, tri->c.y, &miny, &maxy)
            int tx1 = (int)(self->w / 2 + minx) >> 3
            int ty1 = (int)(self->h / 2 + miny) >> 3
            int tx2 = (int)(self->w / 2 + maxx) >> 3
            int ty2 = (int)(self->h / 2 + maxy) >> 3
            if tx1 < 0: tx1 = 0
            if ty1 < 0: ty1 = 0
            if tx2 > (self->w >> 3) - 1: tx2 = (self->w >> 3) - 1
            if ty2 > (self->h >> 3) - 1: ty2 = (self->h >> 3) - 1
            for int v in range(ty1, ty2 + 1):
                for int u in range(tx1, tx2 + 1):
                    if not self->tiles[v * (self->w >> 3) + u]:
                        self->tiles[v * (self->w >> 3) + u] = land_array_new()
                    land_array_add(self->tiles[v * (self->w >> 3) + u], tri)

    for int v in range(self->h >> 3):
        for int u in range(self->w >> 3):
            LandArray *triangles = self->tiles[v * (self->w >> 3) + u]
            if not triangles: continue

            Ray ray
            ray.u = land_vector(0, 0, -1)
            unsigned char *p = rgba + u * 8 * 4 + v * 8 * self->w * 4
            float *zp = zbuffer + u * 8 + v * 8 * self->w
            for int y in range(-self->h / 2 + v * 8, -self->h / 2 + v * 8 + 8):
                for int x in range(-self->w / 2 + u * 8, -self->w / 2 + u * 8 + 8):
                    ray.a = land_vector(x + 0.5, y + 0.5, 1024)
                    for Triangle *tri in LandArray *triangles:
                        Float t = ray_intersects_triangle_optimized(ray, *tri)
                        if t > *zp:
                            Float l = land_vector_dot(tri->n, self->light)

                            float d1 = (1.0 + l) / 2.0;
                            float d2 = (1.0 - l) / 8.0;

                            int c = (d1 + d2) * 255
                            if c < 0: c = 0
                            if c > 255: c = 255

                            p[0] = tri->o->r * c
                            p[1] = tri->o->g * c
                            p[2] = tri->o->b * c
                            p[3] = 255
                            *zp = t

                    p += 4
                    zp++
                p += (self->w - 8) * 4
                zp += self->w - 8

    land_free(zbuffer)
    return rgba

def raytracer_draw_lines(Raytracer *r):
    for Object *o in LandArray *r->objects:
        object_draw_lines(o)
