#!/usr/bin/env python3

from figure import Figure

class Player:

    def __init__(self,pid,start_place,bases,house_places,color):
        self.start_place = start_place
        self.houses = house_places
        self.bases = bases
        self.figures = [Figure(self,base) for base in self.bases]
        self.color = color
        self.pid = pid
        self.tries = 3

        self.start_place.player = self
        for house in self.houses:
            house.player = self
        for base in self.bases:
            base.player = self

    def hasSevTries(self):
        if self.tries != 0:
            return True
        if self.figInBase()+self.figInHouse() == 4 and self.isHouseInOrder():
            self.tries = 3
            return True
        return False

    def figInBase(self):
        return sum([fig.current_place.isBase for fig in self.figures])

    def figInHouse(self):
        return sum([fig.current_place.isHouse for fig in self.figures])

    def isHouseInOrder(self):
        foundOccSlot = False
        foundEmptySlotAfter = False
        for house in self.houses:
            if not foundOccSlot:
                foundOccSlot = house.players_figure != None
            if foundOccSlot:
                if not foundEmptySlotAfter:
                    foundEmptySlotAfter =  house.players_figure == None
        return not foundEmptySlotAfter

    def moveOut(self):
        self.tries = 0

        for fig in self.figures:
            if fig.current_place.isBase: break
        if not fig.current_place.isBase:
            print("Player {}: Base is empty.".format(self.color))
            return 0
        return fig.updatePlace(self.start_place)

    def startIsBlocked(self):
        if self.start_place.players_figure != None:
            return  self.start_place.players_figure.player == self
        return False

    def hit(self,dice):
        for fig in self.figures:
            place = fig.findPlace(dice)
            if place != None:
                if place.players_figure != None:
                    if place.players_figure.player != self:
                        fig.updatePlace(place)
                        return 1
        return 0

    def findFigureAndMove(self,dice):
        if not self.isHouseInOrder():
            print("Player {}: Order House".format(self.color))
            for house in self.houses:
                if house.players_figure != None:
                    dest = house.players_figure.findPlace(dice)
                    if house.players_figure.updatePlace(dest):
                        return 1

        # Find Figure closest to house
        place = self.start_place.prev_place
        while place.prev_place != self.start_place:
            if place.players_figure != None:
                if place.players_figure.player == self:
                    dest = place.players_figure.findPlace(dice)
                    if place.players_figure.updatePlace(dest):
                        return 1
            place = place.prev_place
        return 0
