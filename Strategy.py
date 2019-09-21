from API import Game


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
        units = list()

        """ NO TOUCH BELOW """
        # generate our units (BASE STUFF THAT HAS TO EXIST)
        for i in range(3):
            unit = dict()
            unit["attackPattern"] = [[0]*7 for _ in range(7)]
            if self.player_id == 1:
                unit["unitId"] = i+1
            else:
                unit["unitId"] = i+4
            unit["terrainPattern"] = [[False]*7 for _ in range(7)]
            units.append(unit)
        jonah = units[0]
        wyly = units[1]
        obama = units[2]
        """ NO TOUCH ABOVE """

        # set health and speed
        for i in range(3):
            units[i]["health"] = 3
            units[i]["speed"] = 3
        print(unit[0])
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

        for unit in my_units:
            if unit.id == 0 or unit.id == 3:
                jonah = unit
            elif unit.id == 1 or unit.id == 4:
                wyly = unit
            else:
                obama = unit

        decisions = list()

        jonah_decision = {
            "priority": 3,
            "movement": ["DOWN"]*jonah.speed,
            "unitId": jonah.id
        }

        wyly_decision = {
            "priority": 2,
            "movement": ["DOWN"]*wyly.speed,
            "unitId": wyly.id
        }

        obama_decision = {
            "priority": 1,
            "movement": ["DOWN"]*obama.speed,
            "unitId": obama.id
        }

        decisions.append(jonah_decision)
        decisions.append(wyly_decision)
        decisions.append(obama_decision)
        return decisions
