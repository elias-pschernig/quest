import actor

global int wave_ticks
static char info[256] = ""
static int primes[10] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}

def wave_restart():
    wave_ticks = 0

    #actor_new(app->actors, 320, 60, AT_HUNTER)
    #actor_new(app->actors, 340, 60, AT_DOG)
    #actor_new(app->actors, 300, 60, AT_HEALER)
    #actor_new(app->actors, 320, 80, AT_KNIGHT)
    #actor_new(app->actors, 320, 40, AT_MAGE)

    #actor_new(app->actors, 0, 0, AT_DRAKE)

char const *def wave_info():
    return info

def wave_tick():
    float x = land_rnd(0, app->w)
    float y = land_rnd(0, app->h)

    int wave = wave_ticks / 3600

    int s = (wave_ticks - wave * 3600) / 60

    if wave_ticks % 60 == 0:
        if s == 0:
            sprintf(info, "Wave %d (Prime %d)", 1 + wave, primes[wave])

        if s == 51:
            item_place(item_new(IT_CHEESE, x, y, land_rnd(0, 2 * pi)))
            
        if wave == 0:
            if s == 0:
                actor_new(app->actors, 320, 60, AT_HUNTER)
                actor_new(app->actors, 340, 60, AT_DOG)
            if s == 10 or s == 25 or s == 40 or s == 55:
                actor_new(app->actors, x, y, AT_WOLF)

        if wave > 0 and wave < 5:
            if s % 10 == 0:
                actor_new(app->actors, x, y, AT_WOLF)

        if wave >= 5 and wave < 9:
            if s == 0:
                actor_new(app->actors, x, y, AT_WOLF)
            if s == 20:
                actor_new(app->actors, x, y, AT_BAT)
            if s == 40:
                actor_new(app->actors, x, y, AT_GROLL)

        if wave == 1:
            if s == 0:
                actor_new(app->actors, 300, 60, AT_HEALER)
           
        if wave == 2:
            if s == 0:
                actor_new(app->actors, 320, 80, AT_KNIGHT)
            if s % 10 == 1:
                actor_new(app->actors, x, y, AT_WOLF)
            
        if wave == 3:
            if s == 0:
                actor_new(app->actors, 320, 40, AT_MAGE)
            if s % 10 == 1:
                actor_new(app->actors, x, y, AT_BAT)
            
        if wave == 4:
            if s == 0:
                pass
            if s % 10 == 1:
                actor_new(app->actors, x, y, AT_GROLL)

        if wave == 5:
            if s == 0:
                actor_new(app->actors, x, y, AT_PAPAGROLL)
        if wave == 6:
            if s == 0:
                actor_new(app->actors, x, y, AT_DRAKE)
        if wave == 7:
            if s == 1:
                actor_new(app->actors, x, y, AT_BAT)
            if s == 2:
                actor_new(app->actors, x, y, AT_BAT)
            if s == 3:
                actor_new(app->actors, x, y, AT_BAT)

            if s == 20 or s == 40:
                actor_new(app->actors, x, y, AT_GROLL)
           
        if wave == 8:
            if s == 0:
                actor_new(app->actors, x, y, AT_DRAKE)
            if s == 30:
                actor_new(app->actors, x, y, AT_DRAKE)
           
        if wave == 9:
            if s == 50:
                actor_new(app->actors, 940, 60, AT_DRAGON)
            if s == 5:
                actor_new(app->actors, x, y, AT_PAPAGROLL)
            if s % 10 == 2:
                actor_new(app->actors, x, y, AT_GROLL)

    if wave_ticks < 3600 * 10 - 1: wave_ticks++
