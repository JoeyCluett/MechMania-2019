from API import Game
import copy

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
        units[2] = create_balanced(3, 6)

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
        my_units = self.get_my_units()
        enemy_units = self.get_enemy_units()

        #TODO: Create priority kill system
        target = enemy_units[0]

        print(self.snipe_locations(target))
        #decision = [{
        d = [{
            "priority": i+1,
            "movement": ["UP"]*my_units[i].speed,
            "attack": "STAY",
            "unitId": my_units[i].id
            } for i in range(len(my_units))]

        for i in range(3):
            print(self.super_avoid(my_units[i], target))

        #d[0]["priority"], d[2]["priority"] = d[2]["priority"], d[0]["priority"]

        return d

    # for glass cannon
    def snipe_locations(self, target):
        target_location = (target.pos.x, target.pos.y)
        snipe_locations = [(target.pos.x, target.pos.y-3), (target.pos.x, target.pos.y+3),
                           (target.pos.x-3, target.pos.y), (target.pos.x+3, target.pos.y)]

        for loc in snipe_locations:
            if self.get_tile_at(loc).type == "INDESTRUCTIBLE":
                snipe_locations.remove(loc)

        return snipe_locations

    def possible_destinations(self, player):
        pos = (player.pos.x, player.pos.y)
        map = [[(i, j) for i in range(12)] for j in range(12)]

        # get all possible locations of the bot
        all_locs = list()
        for col in map:
            for row in col:
                if self.path_to((col, row), pos) is None:
                    all_locs.append((col, row))
        return all_locs

    # given character's speed and attack pattern, find all possible attacking_squares
    # NOTE: Best when enemy speed is slow
    def super_attacking_squares(self, target):
        pos = (target.pos.x, target.pos.y)

        all_locs = self.possible_destinations(target)

        # figure out possible attacking squares
        attacking_squares = list()
        for loc in all_locs:
            for direction in {"UP","LEFT","RIGHT","DOWN"}:
                attacking_squares.extend(self.get_positions_of_attack_pattern(target.id, direction, loc))

        return attacking_squares

    def super_avoid(self, player, target, attacking_squares=None):
        if attacking_squares is None:
            attacking_squares = self.super_attacking_squares(target)

        all_locs = self.possible_destinations(player)
        possible_locs = copy.copy(all_locs)
        for sqr in attacking_squares:
            if sqr in all_locs:
                possible_locs.remove(sqr)

        return possible_locs