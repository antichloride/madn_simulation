#!/usr/bin/env python3

class Figure:
    def __init__(self, player, current_place):
        self.current_place = current_place
        self.player = player
        self.current_place.players_figure = self

    def updatePlace(self, new_place):
        if new_place is None:
            return 0
        if new_place.players_figure is not None:
            if new_place.players_figure.player == self.player:
                print("Player {}: Field is blocked.".format(self.player.color))
                return 0
            if new_place.players_figure is not None:
                print("Player {}: Hit figure of player {}".format(
                    self.player.color, new_place.players_figure.player.color))
                new_place.players_figure.sendHome()
        self.current_place.players_figure = None
        self.current_place = new_place
        new_place.players_figure = self

        return 1

    def move(self, n):
        return self.updatePlace(self.findPlace(n))

    def findPlace(self, n):
        place = self.current_place
        for i in range(n):
            if place.next_place == None:
                return None
            if place.entrance_to_house_of_player == self.player.houses[0]:
                place = place.entrance_to_house_of_player
            else:
                place = place.next_place
            # Im Haus kein ueperspringen
            if place.isHouse and place.players_figure != None:
                return None
        return place

    def sendHome(self):
        for base in self.player.bases:
            if base.players_figure == None:
                self.updatePlace(base)
                return
