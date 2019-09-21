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

            d = [
            {
                "priority": 2,
                "movement": ["STAY"]*my_units[0].speed,
                "attack": "STAY",
                "unitId": my_units[0].id
            },
            {
                "priority": 3,
                "movement": ["STAY"]*my_units[1].speed,
                "attack": "STAY",
                "unitId": my_units[1].id
            }] # need to fill out

            o = {
                "priority": 1,
                "attack": "STAY",
                "unitId": my_units[2].id,
                "movement": ["STAY"]*my_units[2].speed # default is to stay
            }

            p = my_units[2].pos

            if(self.player_id == 1):
                m = self.path_to((p.x, p.y), (6, 6), [])
                if m != None:
                    for ind in range(len() if len(m) < my_units[2].speed else my_units[2].speed):
                        o["movement"][ind] = m[ind]
            else:
                m = self.path_to((p.x, p.y), (6, 6), [])
                if m != None:
                    for ind in range(len() if len(m) < my_units[2].speed else my_units[2].speed):
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
                
                d = [{
                    "priority": 1,
                    "movement": ["STAY"]*my_units[0].speed,
                    "attack": "DOWN",
                    "unitId": my_units[0].id
                },
                {
                    "priority": 2,
                    "movement": ["STAY"]*my_units[1].speed,
                    "attack": "DOWN",
                    "unitId": my_units[1].id
                },
                {
                    "priority": 3,
                    "movement": ["STAY"]*my_units[2].speed,
                    "attack": "DOWN",
                    "unitId": my_units[2].id
                }]

                return d

            else:
                d = [{
                    "priority": 1,
                    "movement": ["STAY"]*my_units[0].speed,
                    "attack": "UP",
                    "unitId": my_units[0].id
                },
                {
                    "priority": 2,
                    "movement": ["STAY"]*my_units[1].speed,
                    "attack": "UP",
                    "unitId": my_units[1].id
                },
                {
                    "priority": 3,
                    "movement": ["STAY"]*my_units[2].speed,
                    "attack": "UP",
                    "unitId": my_units[2].id
                }]

                return d

        else:
            pass

        """
        d = [{
            "priority": i+1,
            "movement": ["STAY"]*my_units[i].speed,
            "attack": "UP",
            "unitId": my_units[i].id
        } for i in range(len(my_units))]
        """

        return d
