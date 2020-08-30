#!/usr/bin/env python3

class Place:

    def __init__(
                self,
                prev_place=None,
                next_place=None,
                entrance_to_house_of_player = None,
                players_figure = None,
                isHouse = False,
                isBase = False,
                isStart = False,
                pos = [None,None],
                player = None
                ):
        self.prev_place = prev_place
        self.next_place = next_place
        self.entrance_to_house_of_player = entrance_to_house_of_player
        self.players_figure =  players_figure 
        self.isHouse = isHouse
        self.isBase = isBase
        self.isStart = isStart
        self.pos = pos
        self.player = player
