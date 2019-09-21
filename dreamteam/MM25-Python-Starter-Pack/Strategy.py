from API import Game
import copy
import random
import sys
class Strategy(Game):

    def __init__(self, game_json):        
        #self.STATE = "move_last_player"
        #self.STATE = "barrage"
        #self.STATE = "advance_one"
        #self.STATE = "prep_scatter"
        self.STATE = "prep_wyly_flakbot"

        self.CURRENT_TURN = 0
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
            print("creating glass cannon robot", file=sys.stderr)
            gc = {}            

            atk = \
                [[0] * 7 for j in range(7)]
            atk[3][6] = 1

            gc["speed"] = 6  # zero pts leftover
            gc["health"] = 1 # needs 0 pts
            gc["attackPattern"] = atk

            gc["terrainPattern"] = [[False]*7 for j in range(7)]

            gc["unitId"] = player_1_team
            if self.player_id == 2:
                gc["unitId"] = player_2_team

            return gc

        def create_balanced(player_1_team, player_2_team):
            print("creating balanced robot", file=sys.stderr)
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

        def create_scattershot(player_1_team, player_2_team):
            print("creating scattershot robot", file=sys.stderr)
            u = {}

            atk = \
                [[0] * 7 for j in range(7)]
            
            # 9 atk = 9 pts
            atk[1][4] = 1
            atk[2][4] = 1
            atk[3][4] = 1
            atk[4][4] = 1
            atk[5][4] = 1

            atk[2][5] = 1
            atk[3][5] = 1
            atk[4][5] = 1

            atk[3][6] = 1

            u["attackPattern"] = atk
            u["speed"]  = 6 # 6 spd = 9 pts
            u["health"] = 5 # 5 hlth = 6 pts
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            return u

        def create_wyly_flakbot(player_1_team, player_2_team):
            print("creating 'Wyly Flakbot' robot", file=sys.stderr)
            u = {}

            atk = \
                [[0] * 7 for j in range(7)]
            
            # 8 atk = 12 pts
            atk[3][4] = 2
            atk[2][5] = 2
            atk[4][5] = 2
            atk[3][6] = 2

            u["attackPattern"] = atk
            u["speed"]  = 1 # 1 spd = 0 pts
            u["health"] = 7 # 7 hlth = 12 pts
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            return u

        def create_wyly_flakbot_center(player_1_team, player_2_team):
            print("creating 'Wyly Flakbot Center' robot", file=sys.stderr)
            u = {}

            atk = \
                [[0] * 7 for j in range(7)]
            
            # 8 atk = 12 pts
            atk[3][5] = 2
            atk[2][5] = 2
            atk[4][5] = 2
            atk[3][6] = 2

            u["attackPattern"] = atk
            u["speed"]  = 1 # 1 spd = 0 pts
            u["health"] = 7 # 7 hlth = 12 pts
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            return u

        def create_wyly_flakbot_left(player_1_team, player_2_team):
            print("creating 'Wyly Flakbot Left' robot", file=sys.stderr)
            u = {}

            atk = \
                [[0] * 7 for j in range(7)]
            
            # 8 atk = 12 pts
            atk[2][4] = 2
            atk[2][5] = 2
            atk[4][5] = 2
            atk[3][6] = 2

            u["attackPattern"] = atk
            u["speed"]  = 1 # 6 spd = 9 pts
            u["health"] = 5 # 5 hlth = 6 pts
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            return u

        def create_wyly_flakbot_right(player_1_team, player_2_team):
            print("creating 'Wyly Flakbot Right' robot", file=sys.stderr)
            u = {}

            atk = \
                [[0] * 7 for j in range(7)]
            
            # 8 atk = 12 pts
            atk[4][4] = 2
            atk[2][5] = 2
            atk[4][5] = 2
            atk[3][6] = 2

            u["attackPattern"] = atk
            u["speed"]  = 1 # 1 spd = 0 pts
            u["health"] = 7 # 7 health = 12 pts
            u["terrainPattern"] = [[False]*7 for j in range(7)]

            u["unitId"] = player_1_team
            if self.player_id == 2:
                u["unitId"] = player_2_team

            return u

        #units.append(create_scattershot(3, 6)) # units[0]
        #units.append(create_scattershot(1, 4)) # units[1]
        #units.append(create_scattershot(2, 5)) # units[2] the oddball

        #units.append(create_wyly_flakbot(1, 4))
        #units.append(create_wyly_flakbot(2, 5))
        #units.append(create_wyly_flakbot(3, 6))

        units.append(create_wyly_flakbot_center(1, 4))
        units.append(create_wyly_flakbot_left(2, 5))
        units.append(create_wyly_flakbot_right(3, 6))

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

        print('Debug: player ' + str(self.player_id), file=sys.stderr)
        print("    STATE: " + self.STATE, file=sys.stderr)
        print("    Turn #" + str(self.CURRENT_TURN), file=sys.stderr)

        self.CURRENT_TURN += 1

        if self.STATE == "move_last_player":

            my_units = self.get_my_units()            
            #print('Num units: ' + str(len(my_units)))

            d = []
            avoid_list = []

            if True:
                o = {
                    "priority": 1,
                    "attack": "STAY",
                    "unitId": my_units[2].id,
                    "movement": ["STAY"]*my_units[2].speed # default is to stay
                }

                p = my_units[2].pos

                if self.player_id == 1:
                    m, L = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (5, 5), []))
                    avoid_list.append(L)
                    if m is not None:
                        for ind in range(min(len(m), my_units[2].speed)):
                            o["movement"][ind] = m[ind]
                else:
                    m, L = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (6, 6), []))
                    avoid_list.append(L)
                    if m is not None:
                        for ind in range(min(len(m), my_units[2].speed)):
                            o["movement"][ind] = m[ind]

                d.append(o)

            for i in range(2):

                o = {
                    "priority": i+2,
                    "attack": "STAY",
                    "unitId": my_units[i].id,
                    "movement": ["STAY"]*my_units[i].speed # default is to stay
                }

                p = my_units[i].pos

                if(self.player_id == 1):
                    m, L = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (5, 5), []), avoid_list)
                    avoid_list.append(L)
                    if m != None:
                        for ind in range(min(len(m), my_units[i].speed)):
                            o["movement"][ind] = m[ind]
                else:
                    m, L = self.clean_path((p.x, p.y), self.path_to((p.x, p.y), (6, 6), []), avoid_list)
                    avoid_list.append(L)
                    if m != None:
                        for ind in range(min(len(m), my_units[i].speed)):
                            o["movement"][ind] = m[ind]

                d.append(o)

            d = self.clean_final_decision(d)
            print(str(d), file=sys.stderr)
            self.STATE = "barrage"
            return d

        elif self.STATE == "advance_one":

            my_units = self.get_my_units()

            d = [{
                "priority": i+1,
                "movement": ["STAY"]*my_units[i].speed,
                "attack": "STAY",
                "unitId": 3-i
            } for i in range(len(my_units))]
            
            if self.player_id == 2:
                for i in range(len(d)):
                    for j in range(5):
                        d[i]["movement"][j] = "UP"
                        #d[i]["movement"][1] = "UP"
                    d[i]["unitId"] += 3
                    d[i]["attack"] = "LEFT"
            else:
                for i in range(len(d)):
                    for j in range(5):
                        d[i]["movement"][j] = "DOWN"
                        #d[i]["movement"][1] = "DOWN"
                    d[i]["attack"] = "RIGHT"

            self.STATE = "move_center"

            d = self.clean_final_decision(d)
            print(str(d), file=sys.stderr)
            return d

        elif self.STATE == "move_center":

            my_units = self.get_my_units()

            d = [{
                "priority": i+1,
                "movement": ["STAY"]*my_units[i].speed,
                "attack": "STAY",
                "unitId": 3-i
            } for i in range(len(my_units))]
            
            if self.player_id == 2:
                for i in range(len(d)):
                    for j in range(3):
                        d[i]["movement"][j] = "LEFT"
                    d[i]["unitId"] += 3
                    d[i]["attack"] = "LEFT"
            else:
                for i in range(len(d)):
                    for j in range(3):
                        d[i]["movement"][j] = "RIGHT"
                    d[i]["attack"] = "RIGHT"

            self.STATE = "barrage"
            d = self.clean_final_decision(d)
            print(str(d), file=sys.stderr)
            return d

        elif self.STATE == "barrage":

            my_units = self.get_my_units()
            
            if self.player_id == 1:
                
                d = []

                for ind in range(len(my_units)):
                    d.append({
                        "priority": ind+1,
                        "movement": ["STAY"]*my_units[ind].speed,
                        "attack": "RIGHT",
                        "unitId": my_units[ind].id
                    })

                    #d[ind]["movement"][0] = "DOWN"
                    #d[ind]["movement"][1] = "UP"
                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)


                d = self.clean_final_decision(d)
                #return 1/0
                return d

            else:
                d = []

                for ind in range(len(my_units)):
                    d.append({
                        "priority": ind+1,
                        "movement": ["STAY"]*my_units[ind].speed,
                        "attack": "LEFT",
                        "unitId": my_units[ind].id
                    })

                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

        elif self.STATE == "prep_scatter":

            my_units = self.get_my_units()

            if self.player_id == 1:
                
                d = [{
                    "priority": 1,
                    "movement": ["DOWN"]*6,
                    "attack": "DOWN",
                    "unitId": 3
                },
                {
                    "priority": 2,
                    "movement": ["DOWN"]*5 + ["STAY"],
                    "attack": "UP",
                    "unitId": 1
                },
                {
                    "priority": 3,
                    "movement": ["DOWN"]*6,
                    "attack": "RIGHT",
                    "unitId": 2
                }]


                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                self.STATE = "move_scatter"
                return d

            else:

                d = [{
                    "priority": 1,
                    "movement": ["UP"]*6,
                    "attack": "UP",
                    "unitId": 6
                },
                {
                    "priority": 2,
                    "movement": ["UP"]*5 + ["STAY"],
                    "attack": "DOWN",
                    "unitId": 4
                },
                {
                    "priority": 3,
                    "movement": ["UP"]*6,
                    "attack": "LEFT",
                    "unitId": 5
                }]

                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                self.STATE = "move_scatter"
                return d

        elif self.STATE == "move_scatter":

            if self.player_id == 1:
                
                d = [{
                    "priority": 1,
                    "movement": ["RIGHT"] + ["STAY"]*5,
                    "attack": "DOWN",
                    "unitId": 3
                },
                {
                    "priority": 2,
                    "movement": ["RIGHT"] + ["STAY"]*5,
                    "attack": "UP",
                    "unitId": 1
                },
                {
                    "priority": 3,
                    "movement": ["RIGHT"] + ["STAY"]*5,
                    "attack": "RIGHT",
                    "unitId": 2
                }]


                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

            else:

                d = [{
                    "priority": 1,
                    "movement": ["LEFT"] + ["STAY"]*5,
                    "attack": "UP",
                    "unitId": 6
                },
                {
                    "priority": 2,
                    "movement": ["LEFT"] + ["STAY"]*5,
                    "attack": "DOWN",
                    "unitId": 4
                },
                {
                    "priority": 3,
                    "movement": ["LEFT"] + ["STAY"]*5,
                    "attack": "LEFT",
                    "unitId": 5
                }]

                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

        elif self.STATE == "prep_wyly_flakbot":
            
            if self.player_id == 1:
                
                d = [{
                    "priority": 1,
                    "movement": ["DOWN"],
                    "attack": "DOWN",
                    "unitId": 3
                },
                {
                    "priority": 2,
                    "movement": ["DOWN"],
                    "attack": "STAY",
                    "unitId": 1
                },
                {
                    "priority": 3,
                    "movement": ["LEFT"],
                    "attack": "STAY",
                    "unitId": 2
                }]

                self.STATE = "move_wyly_flakbot"
                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

            else:

                d = [{
                    "priority": 1,
                    "movement": ["UP"],
                    "attack": "STAY",
                    "unitId": 6
                },
                {
                    "priority": 2,
                    "movement": ["UP"],
                    "attack": "STAY",
                    "unitId": 4
                },
                {
                    "priority": 3,
                    "movement": ["RIGHT"],
                    "attack": "STAY",
                    "unitId": 5
                }]

                self.STATE = "move_wyly_flakbot"
                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

        elif self.STATE == "move_wyly_flakbot":

            if self.player_id == 1:

                d = [{
                    "priority": 2,
                    "movement": ["RIGHT"],
                    "attack": "RIGHT",
                    "unitId": 3
                },
                {
                    "priority": 1,
                    "movement": ["RIGHT"],
                    "attack": "RIGHT",
                    "unitId": 1
                },
                {
                    "priority": 3,
                    "movement": ["RIGHT"],
                    "attack": "RIGHT",
                    "unitId": 2
                }]
                
                if not self.wyly_flakbot_can_move((), "RIGHT"):
                    d[0]["attack"] = "UP"
                    d[2]["attack"] = "DOWN"

                    for i in d:
                        i["movement"] = ["STAY"]

                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d

            else:
                
                d = [{
                    "priority": 2,
                    "movement": ["LEFT"],
                    "attack": "LEFT",
                    "unitId": 6
                },
                {
                    "priority": 1,
                    "movement": ["LEFT"],
                    "attack": "LEFT",
                    "unitId": 4
                },
                {
                    "priority": 3,
                    "movement": ["LEFT"],
                    "attack": "LEFT",
                    "unitId": 5
                }]

                if not self.wyly_flakbot_can_move((), "LEFT"):
                    d[0]["attack"] = "DOWN"
                    d[2]["attack"] = "UP"

                    for i in d:
                        i["movement"] = ["STAY"]

                d = self.clean_final_decision(d)
                print(str(d), file=sys.stderr)
                return d
        else:
            print('#### Unknown state')
            raise Exception("If you see this message, something went wrong")

    def wyly_flakbot_can_move(self, pos, dir):
        if dir == "UP":
            return \
                self.get_unit_at((pos[0]-1, pos[1]+1)) is None and \
                self.get_unit_at((pos[0], pos[1]+1)) is None and \
                self.get_unit_at((pos[0]+1, pos[1]+1)) is None
        elif dir == "LEFT":
            return \
                self.get_unit_at((pos[0]-1, pos[1]+1)) is None and \
                self.get_unit_at((pos[0]-1, pos[1]+0)) is None and \
                self.get_unit_at((pos[0]-1, pos[1]-1)) is None
        elif dir == "RIGHT":
            return \
                self.get_unit_at((pos[0]+1, pos[1]+1)) is None and \
                self.get_unit_at((pos[0]+1, pos[1]+0)) is None and \
                self.get_unit_at((pos[0]+1, pos[1]-1)) is None
        elif dir == "DOWN":
            return \
                self.get_unit_at((pos[0]-1, pos[1]-1)) is None and \
                self.get_unit_at((pos[0]+0, pos[1]-1)) is None and \
                self.get_unit_at((pos[0]+1, pos[1]-1)) is None
        else:
            raise Exception("you shouldn't be here")

    ################### HELPER FUNCTIONS #################

    def clean_final_decision(self, decision_list):
        clean_error = False
        my_units = self.get_my_units()
        if len(decision_list) != len(my_units):
            clean_error = True
            print("decision list doesn't match total units!!!!!")

        priorities = list()
        movements = list()
        attacks = list()
        unitIds = list()

        for decision in decision_list:
            for req in {"priority", "movement", "attack", "unitId"}:
                if req not in decision:
                    clean_error = True
                    print(f"decision {decision} does not have requirement {req}", file=sys.stderr)
                    break

            # individual cleaning
            if decision["unitId"] < 1 or decision["unitId"] > 6 or decision["unitId"] in unitIds:
                clean_error = True
                print("Invalid unitId. Guessing...", file=sys.stderr)
                #raise Exception(f"dec: {decision} - dec_list: {decision_list}")
                for id in {1, 2, 3}:
                    if self.player_id == 2:
                        id += 3
                    if id not in unitIds:
                        decision["unitId"] = id
                        break

            unit = self.get_unit(decision["unitId"])
            if unit is None:
                raise Exception("get unit is hard")

            if decision["priority"] < 1 or len(my_units) < decision["priority"] or decision["priority"] in priorities:
                clean_error = True
                #print(f"Invalid priority {decision['priority']} in decision {decision}.", file=sys.stderr)
                for pri in sorted([i+1 for i in range(len(my_units))]):
                    if pri not in priorities:
                        decision["priority"] = pri
                        print(f"updating priority to be {pri}", file=sys.stderr)
                        break

            if len(decision["movement"]) < 1 or len(decision["movement"]) > unit.speed:
                clean_error = True
                print(f"Invalid movement {decision['movement']} in decision {decision}.", file=sys.stderr)
                path = ["STAY"]*unit.speed
                decision["movement"] = path

            if decision["attack"] not in {"LEFT", "RIGHT", "UP", "DOWN", "STAY"}:
                print(f"Invalid attack {decision['attack']} in decision {decision}.", file=sys.stderr)
                decision["attack"] = "STAY"

            # group cleaning (and below)
            priorities.append(decision["priority"])
            movements.append(decision["movement"])
            attacks.append(decision["attack"])
            unitIds.append(decision["unitId"])

        if clean_error:
            print(f"remaining units: {len(my_units)}", file=sys.stderr)
            print(f"priorities: {priorities}", file=sys.stderr)
            print(f"movements: {movements}", file=sys.stderr)
            print(f"attacks: {attacks}", file=sys.stderr)
            print(f"unitIds: {unitIds}", file=sys.stderr)
            print("==========CLEAN ERROR===========", file=sys.stderr)

        return decision_list

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
            if friendly_locs != None and not l in friendly_locs:
                print('\t-- avoiding friendly unit')
                return True
            return False
        
        c_path = list()
        bad = False
        loc = player_pos
        for direction in path:
            if bad is True:
                print('\t-- waiting, i give up on life')
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
                print('\t-- staying')
                c_path.append("STAY")
                bad = True
        return c_path, loc

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
