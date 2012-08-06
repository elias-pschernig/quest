import actor

def ai_tick(Actor *self):

    if self->special == 900:
        special(self)
    
    # if no target, target closest enemy
    if not self->target:
        float mind = 0
        Actor *closest = None
        for Actor *a in LandArray *app->actors->array:
            if a->kind->enemy:
                continue
            float d = actor_distance(self, a)
            if not closest or d < mind:
                mind = d
                closest = a
        self->target = closest

    if not self->target:
        return
