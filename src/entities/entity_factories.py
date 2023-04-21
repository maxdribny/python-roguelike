from entities.entity import Entity

player = Entity(0, 0, "@", (255, 255, 255), "Player", blocks_movement=True)

orc = Entity(0, 0, "o", (63, 127, 63), "Orc", blocks_movement=True)
troll = Entity(0, 0, "T", (0, 127, 0), "Troll", blocks_movement=True)
