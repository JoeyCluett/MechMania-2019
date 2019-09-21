from API import Game

class Strategy(Game):

    def __init__(self, game_json):        
        self.STATE = "move_last_player"
        #self.STATE = "barrage"
        Game.__init__(self, game_json)

    """
        FILL THIS METHOD OUT FOR YOUR BOT:
        Method to set unit initializations. Run at the beginning of a game, after assigning player numbers.
        We have given you a default implementation for this method.
        OUTPUT:
            An array of 3 dictionaries, where each dictionary details a unit. The dictionaries should have the following fields
                "health": An integer indicating the desired health for that unit
                "speed": An integer indicating the desired speed for that unit
                "unitId": An integer indicating the desired id for that unit. In this provided example, we assign Ids 1,2,3 if you are player1, or 4,5,6 if you are player2
                "attackPattern": a 7x7 2d integer list indicating the desired attack pattern for that unit
                "terrainPattern": a 7x7 2d boolean list indicating the desired terrain pattern for that unit.
        Note: terrainPattern and attackPattern should be indexed x,y. with (0,0) being the bottom left
        If player_id is 1, UnitIds for the bots should be 1,2,3. If player_id is 2, UnitIds should be 4,5,6
    """
    def get_setup(self):

        units = []

        def create_glass_cannon(player_1_team, player_2_team):
            print("creating glass cannon robot")
            gc = {}            

            atk = \
                [[0] * 7 for j in range(7)]
            atk[3][6] = 5

            gc["speed"] = 6  # zero pts leftover
            gc["health"] = 1 # needs 0 pts
            gc["attackPattern"] = atk

            gc["terrainPattern"] = [[False]*7 for j in range(7)]

            gc["unitId"] = player_1_team
            if self.player_id == 2:
                gc["unitId"] = player_2_team

            return gc

        def create_balanced(player_1_team, player_2_team):
            print("creating balanced robot")
            u = {}

            # 4 attack (10 pts)
            atk = \
                [[0] * 7 for j in range(7)]
            atk[2][4] = 1
            atk[3][4] = 1
            atk[4][4] = 1
            atk[3][5] = 1

            u["attackPattern"] = atk

            u["speed"]  = 1 #4 # 4 pts
            u["health"] = 1 #6 # 9 pts

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            # empty terrain pattern
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            return u

        units.append(create_glass_cannon(1, 4)) # units[0]
        units.append(create_glass_cannon(2, 5)) # units[1]
        units.append(create_glass_cannon(3, 6)) # units[2] the oddball

        return units

    """
        FILL THIS METHOD OUT FOR YOUR BOT:
        Method to implement the competitors strategy in the next turn of the game.
        We have given you a default implementation here.
        OUTPUT:
            A list of 3 dictionaries, each of which indicates what to do on a given turn with that specific unit. Each dictionary should have the following keys:
                "unitId": The Id of the unit this dictionary will detail the action for
                "movement": an array of directions ("UP", "DOWN", "LEFT", or "RIGHT") details how you want that unit to move on this turn
                "attack": the direction in which to attack ("UP", "DOWN", "LEFT", or "RIGHT")
                "priority": The bots move one at a time, so give the priority which you want them to act in (1,2, or 3)
    """
    def do_turn(self):

        print('Debug: player ' + str(self.player_id))

        if self.STATE == "move_last_player":
            print("STATE: move_last_player")

            my_units = self.get_my_units()            
            print('Num units: ' + str(len(my_units)))

            d = []

            for i in range(2):

                o = {
                    "priority": i+2,
                    "attack": "STAY",
                    "unitId": my_units[i].id,
                    "movement": ["STAY"]*my_units[i].speed # default is to stay
                }

                p = my_units[2-i].pos

                if(self.player_id == 1):
                    m = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (5, 5), []), [(5, 5)])
                    if m != None:
                        for ind in range(min(len(m), my_units[i].speed)):
                            o["movement"][ind] = m[ind]
                else:
                    m = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (6, 6), []), [(6, 6)])
                    if m != None:
                        for ind in range(min(len(m), my_units[i].speed)):
                            o["movement"][ind] = m[ind]

                d.append(o)

            if True:
                o = {
                    "priority": i+1,
                    "attack": "STAY",
                    "unitId": my_units[2-i].id,
                    "movement": ["STAY"]*my_units[2-i].speed # default is to stay
                }

                p = my_units[2-i].pos

                if(self.player_id == 1):
                    m = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (5, 5), [])
                    if m != None:
                        for ind in range(min(len(m), my_units[2-i].speed)):
                            o["movement"][ind] = m[ind]
                else:
                    m = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (6, 6), []))
                    if m != None:
                        for ind in range(min(len(m), my_units[2-i].speed)):
                            o["movement"][ind] = m[ind]

                d.append(o)

            print("d length (expecting 3): " + str(len(d)))
            self.STATE = "barrage"
            return d

        elif self.STATE == "barrage":
            print("STATE: barrage")

            #d = []
            my_units = self.get_my_units()
            
            print("\tunit list len: " + str(len(my_units)))

            if self.player_id == 1:
                
                d = []

                for ind in range(len(my_units)):
                    d.append({
                        "priority": ind+1,
                        "movement": ["STAY"]*my_units[ind].speed,
                        "attack": "DOWN",
                        "unitId": my_units[ind].id
                    })

                return d

            else:
                d = []

                for ind in range(len(my_units)):
                    d.append({
                        "priority": ind+1,
                        "movement": ["STAY"]*my_units[ind].speed,
                        "attack": "DOWN",
                        "unitId": my_units[ind].id
                    })

                return d

        else:
            pass

    # given a player and a target position, find the locations on the board where the player can attack the target
    def attacking_tiles(self, player, target_pos):
        all_locs = self.possible_destinations(player)

        # figure out possible attacking squares
        attacking_squares = list()
        for loc in all_locs:
            for direction in {"UP", "LEFT", "RIGHT", "DOWN"}:
                if target_pos in [_[0] for _ in self.get_positions_of_attack_pattern(player.id, direction, loc)]:
                    attacking_squares.append((loc, direction))

        return attacking_squares

    # get a destination path of up, left, down, right pattern to attack a given target
    # returns a tuple where dest[0] is the destination path and dest[1] is the attack direction to do
    def attack_path(self, player, target_pos):
        possible_dests = self.attacking_tiles(player, target_pos)
        if possible_dests is None or len(possible_dests) == 0:
            return None
        else:
            dest = random.choice(possible_dests)
            return (self.path_to(player, dest[0]), dest[1])

    # make sure that the path is clear
    def clean_path(self, player_pos, path, friendly_locs=None):

        def loc_is_friendly(l):
            if friendly_locs != None:
                for loc in friendly_locs:
                    if loc == l:
                        return True
            return False
                
        c_path = list()
        bad = False
        loc = player_pos
        for direction in path:
            if bad is True:
                c_path.append("STAY")
                continue
            if direction == "RIGHT":
                loc = (loc[0]+1, loc[1])
            elif direction == "LEFT":
                loc = (loc[0]-1, loc[1])
            elif direction == "UP":
                loc = (loc[0], loc[1]+1)
            elif direction == "DOWN":
                loc = (loc[0], loc[1]-1)
            
            if 0 <= loc[0] <= 11 and 0 <= loc[1] <= 11 and \
                    self.get_tile(loc).hp == 0 and self.get_unit_at(loc) is None and \
                        not loc_is_friendly(loc):
                c_path.append(direction)
            else:
                c_path.append("STAY")
                bad = True
        return c_path


    # given a player, finds all possible locations he can move to
    def possible_destinations(self, player):
        pos = (player.pos.x, player.pos.y)
        map = [[(i, j) for i in range(12)] for j in range(12)]

        # get all possible locations of the bot
        all_locs = list()
        for col in map:
            for spot in col:
                path = self.path_to(spot, (player.pos.x, player.pos.y))
                if path is not None and len(path) > player.speed:
                    all_locs.append(spot)
        return all_locs

    # for glass cannon
    def snipe_locations(self, target):
        target_location = (target.pos.x, target.pos.y)
        snipe_locations = [(target.pos.x, target.pos.y-3), (target.pos.x, target.pos.y+3),
                           (target.pos.x-3, target.pos.y), (target.pos.x+3, target.pos.y)]

        for loc in snipe_locations:
            print(loc)
            if self.get_tile(loc).type == "INDESTRUCTIBLE":
                snipe_locations.remove(loc)

        return snipe_locations

    # given character's pathing and attack pattern, find all possible attacking_squares
    # NOTE: Best when enemy speed is slow
    def super_attacking_squares(self, target):
        pos = (target.pos.x, target.pos.y)

        all_locs = self.possible_destinations(target)

        # figure out possible attacking squares
        attacking_squares = list()
        for loc in all_locs:
            for direction in {"UP", "LEFT", "RIGHT", "DOWN"}:
                attacking_squares.extend([_[0] for _ in self.get_positions_of_attack_pattern(target.id, direction, loc)])

        return attacking_squares

    # find positions on the board where the player can escape to to AVOID the target at ALL COSTS
    def super_avoid(self, player, target, attacking_squares=None):
        if attacking_squares is None:
            attacking_squares = self.super_attacking_squares(target)

        all_locs = self.possible_destinations(player)
        possible_locs = copy.copy(all_locs)
        for sqr in attacking_squares:
            if sqr in all_locs:
                possible_locs.remove(sqr)

        return possible_locs
