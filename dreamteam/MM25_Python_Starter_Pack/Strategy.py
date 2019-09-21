from API import Game
import copy
import random

class Strategy(Game):

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
        units = [{}, {}, {}]

        def create_glass_cannon(player_1_team, player_2_team):
            print("creating glass cannon robot")
            gc = {}            

            atk = \
                [[0] * 7 for j in range(7)]
            atk[3][6] = 5

            gc["speed"] = 6 # zero pts leftover
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

            u["speed"]  = 4 # 4 pts
            u["health"] = 6 # 9 pts

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            # empty terrain pattern
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            return u

        def create_puncher_bot(player_1_team, player_2_team):
            print("creating the bots from KNOCKOUT")
            u = {}

            # 3 attack (6 pts)
            atk = \
                [[0] * 7 for j in range(7)]
            atk[3][4] = 3

            u["attackPattern"] = atk
            u["speed"] = 5
            u["health"] = 7
            u["terrainPattern"] = [[False]*7 for _ in range(7)]

            return u

        def create_tank(player_1_team, player_2_team):
            print("creating super tank")
            u = {}


        """
        for i in range(3):
            #unit = {"health": 5, "speed": 5}
            unit={}
            
            unit["health"] = 5 # 6 pts
            unit["speed"] = 5  # 6 pts
            atk = \
                [[0] * 7 for j in range(7)]
            
            # if you are player1, unitIds will be 1,2,3. If you are player2, they will be 4,5,6
            unit["unitId"] = i + 1
            if self.player_id == 2:
                unit["unitId"] += 3
            
            unit["terrainPattern"] = [[False]*7 for j in range(7)]

            # diamond shape in front of the bot            
            atk[3][4] = 2
            atk[3][6] = 2
            atk[2][4] = 2
            atk[4][4] = 2
            unit["attackPattern"] = atk

            units.append(unit)
        """

        units[0] = create_glass_cannon(1, 4)
        units[1] = create_balanced(2, 5)
        units[2] = create_puncher_bot(3, 6)
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
        #raise Exception("got this far")
        my_units = self.get_my_units()
        enemy_units = self.get_enemy_units()
        #TODO: Create priority kill system
        target = enemy_units[0]
        attack_path = self.attack_path(my_units[0], (target.pos.x, target.pos.y))
        direction = "STAY"
        d = [{
            "priority": i+1,
            "movement": self.clean_path((my_units[i].pos.x, my_units[i].pos.y), ["UP"]*my_units[i].speed),
            "attack": "STAY",
            "unitId": my_units[i].id
            } for i in range(len(my_units))]

        # CHOOSE A PATH
        path_dict = {}

        for z in range(len(my_units)):
            if self.player_id == 1:
                if random.randint(0, 1):
                    path_dict[z] = (["DOWN", "RIGHT", "DOWN", "RIGHT", "DOWN", "RIGHT", "DOWN", "RIGHT","DOWN", "RIGHT"], "STAY")
                else:
                    path_dict[z] = (["RIGHT", "DOWN", "RIGHT", "DOWN", "RIGHT", "DOWN", "RIGHT", "DOWN", "RIGHT", "DOWN"], "STAY")
            elif self.player_id == 2:
                if random.randint(0, 1):
                    path_dict[z] = (["UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT"], "STAY")
                else:
                    path_dict[z] = (["LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP", "LEFT", "UP"], "STAY")
            else:
                raise Exception("wat")


        for z in range(len(my_units)):
            if my_units[z]["unitId"] == 3 or my_units[z]["UnitId"] == 6:
                dec = self.decision_puncher(my_units[z])

        #path_dict[0] = (["STAY"]*my_units[0].speed, "STAY")

        #path_dict[1] = (["STAY"]*my_units[1].speed, "STAY")

        #path_dict[2] = (["STAY"]*my_units[2].speed, "STAY")

        # END CHOOSE A PATH

        for z in range(len(my_units)):
            d[z]["priority"] = z+1  # priority

        for z in range(len(my_units)):
            d[z]["movement"] = \
                self.clean_path(
                    (my_units[z].pos.x, my_units[z].pos.y),
                    path_dict[z][0][:my_units[z].speed]
                )

        for z in range(len(my_units)):
            d[z]["attack"] = path_dict[z][1]


        #d[0]["priority"], d[2]["priority"] = d[2]["priority"], d[0]["priority"]

        return d

    #JANK
    def decision_puncher(self, puncher):
        puncher_loc = (puncher.pos.x, puncher.pos.y)
        if self.player_id == 1:

            # top left
            if self.get_tile((4, 5)).hp > 0:
                path = self.path_to(puncher_loc, (5, 5))
                clean_path = self.clean_path(puncher_loc, path)
                if clean_path is None:
                    return {
                        "priority": 1,
                        "movement": ["STAY"]*puncher.speed,
                        "attack": "STAY",
                        "unitId": puncher.id
                    }
                else:
                    c_p, puncher_loc = clean_path

            else:
                pass

        else:
            # bottom right
            pass
        dec = {
            "movement": self.path_to((puncher.pos.x, puncher.pos.y), )
        }

    ########### HELPER FUNCTIONS ###############

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
    # real shame this BREAKS THE GAME
    def attack_path(self, player, target_pos):
        possible_dests = self.attacking_tiles(player, target_pos)
        if possible_dests is None or len(possible_dests) == 0:
            return None
        else:
            dest = random.choice(possible_dests)
            return self.path_to(player, dest[0]), dest[1]

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
                loc = (loc[0] + 1, loc[1])
            elif direction == "LEFT":
                loc = (loc[0] - 1, loc[1])
            elif direction == "UP":
                loc = (loc[0], loc[1] + 1)
            elif direction == "DOWN":
                loc = (loc[0], loc[1] - 1)

            if 0 <= loc[0] <= 11 and 0 <= loc[1] <= 11 and \
                    self.get_tile(loc).hp == 0 and self.get_unit_at(loc) is None and \
                    not loc_is_friendly(loc):
                c_path.append(direction)
            else:
                c_path.append("STAY")
                bad = True
        return (c_path, loc)

    # given a player, finds all possible locations he can move to
    def possible_destinations(self, player):
        pos = (player.pos.x, player.pos.y)
        map = [[(i, j) for i in range(12)] for j in range(12)]

        # get all possible locations of the bot
        all_locs = list()
        for col in map:
            for spot in col:
                path = self.path_to(spot, (player.pos.x, player.pos.y))
                if path is not None and len(path) < player.speed:
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
