import actor

def special(Actor *a):
    if not a: return

    if a->special < 900: return

    a->special = 0

    if a->kind->id == AT_HEALER:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if not b->kind->enemy:
                b->hp = b->max_hp

    if a->kind->id == AT_KNIGHT:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if b->kind->enemy:
                b->target = a

    if a->kind->id == AT_DOG:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if b->kind->enemy:
                b->target = None
                b->tx = (a->x + b->x) / 2
                b->ty = (a->y + b->y) / 2
                b->walking = True

    if a->kind->id == AT_HUNTER:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if b->kind->enemy:
                b->frozen = 300

    if a->kind->id == AT_MAGE:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if b->kind->enemy:
                b->hp -= 7
                if b->hp < 1:
                    b->hp = 1
                b->frozen = 60
               
    if a->kind->id == AT_PAPAGROLL:
        for Actor *b in LandArray *app->actors->array:
            if b->dead: continue
            if b->kind->id == AT_GROLL:
                b->hp = b->max_hp
