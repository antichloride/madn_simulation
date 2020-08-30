#!/usr/bin/env python3

from player import Player
from place import Place
import numpy as np
from tkinter import Canvas

WIDTH = 360
HEIGHT = 260
DELAY = 1000


class Field(Canvas):
    def __init__(self, number_of_players):
        super().__init__(
            width=WIDTH, height=HEIGHT, background="white", highlightthickness=0
        )
        self.start_places = []
        self.houses = [[] for i in range(4)]
        self.number_of_players = number_of_players
        self.bases = [[] for i in range(4)]
        self.house_entrances = []
        self.winner = None

        self._build_field()
        self._init_players()
        self.drawField()
        self.after(DELAY, self.onTimer)
        self.pack()

    def onTimer(self):
        self.delete("all")
        self.create_text(
            WIDTH - 60, 50, text="Player: {}".format(self.current_player.color)
        )
        self.move()
        self.create_text(WIDTH - 60, 20, text="Wurf: {}".format(self.dice))
        self.drawField()
        if self.winner != None:
            with open("res.txt", "a") as f:
                f.write(self.winner + "\n")
            self.__init__(3)
        self.after(DELAY, self.onTimer)

    def move(self):
        self.dice = np.random.randint(1, 7)

        if self.current_player.hasSevTries():
            print(
                "Player {}: Try number {}".format(
                    self.current_player.color, 4 - self.current_player.tries
                )
            )
            if self.dice == 6:
                self.current_player.moveOut()
                print("Player {}: Move Out".format(self.current_player.color))
                return
            else:
                self.current_player.tries -= 1
                if self.current_player.tries == 0:
                    self.nextPlayer()
                return

        if self.current_player.startIsBlocked():
            if self.current_player.start_place.players_figure.move(self.dice):
                self.nextPlayer()
                return

        if self.dice == 6:
            if self.current_player.moveOut():
                return

        if self.current_player.hit(self.dice):
            return

        self.current_player.findFigureAndMove(self.dice)

        self.nextPlayer()

    def nextPlayer(self):
        if self.current_player.figInHouse() == 4:
            self.winner = self.current_player.color
        if self.dice == 6:
            return
        if self.current_pid == self.number_of_players - 1:
            self.current_pid = 0
        else:
            self.current_pid += 1
        self.current_player = self.players[self.current_pid]

    def _build_field(self):
        width = 260
        height = 260

        cs = 20  # circle size
        pd = 2  # pading
        fpd = 10  # frame padding

        self.width = width
        self.height = height
        self.cs = cs
        self.pd = pd
        self.fpd = fpd

        start_positions = np.array(
            [
                [fpd + 4 * (cs + pd), height - (fpd + cs)],
                [fpd, fpd + 4 * (cs + pd)],
                [width - (fpd + 4 * (cs + pd) + cs), fpd],
                [width - (fpd + cs), height - (fpd + 4 * (cs + pd) + cs)],
            ]
        )
        pos = [[0, 0]]
        for i in range(4):
            pos.append([pos[-1][0], pos[-1][1] - (cs + pd)])
        for i in range(4):
            pos.append([pos[-1][0] - (cs + pd), pos[-1][1]])
        pos.append([pos[-1][0], pos[-1][1] - (cs + pd)])
        pos = np.array(pos)

        base_pos = np.array(
            [
                [-3 * (cs + pd), 0],
                [-4 * (cs + pd), 0],
                [-3 * (cs + pd), -(cs + pd)],
                [-4 * (cs + pd), -(cs + pd)],
            ]
        )

        house_pos = np.array(
            [
                [cs + pd, -(cs + pd)],
                [cs + pd, -2 * (cs + pd)],
                [cs + pd, -3 * (cs + pd)],
                [cs + pd, -4 * (cs + pd)],
            ]
        )

        current_place = None

        # Make Loop
        for corner in range(4):

            pos_corner = self.transformCoord(
                pos, corner * np.pi / 2, start_positions[corner]
            )
            base_pos_corner = self.transformCoord(
                base_pos, corner * np.pi / 2, start_positions[corner]
            )
            house_pos_corner = self.transformCoord(
                house_pos, corner * np.pi / 2, start_positions[corner]
            )

            self.bases[corner] = [
                Place(isBase=True, pos=base_pos_corner[i]) for i in range(4)
            ]

            next_place = Place(current_place, isStart=True, pos=pos_corner[0])
            if current_place != None:
                current_place.next_place = next_place
            current_place = next_place
            self.start_places.append(current_place)

            for i in range(9):
                next_place = Place(current_place, pos=pos_corner[i + 1])
                current_place.next_place = next_place
                current_place = next_place

            # Make House
            house = Place(isHouse=True, pos=house_pos_corner[0])
            self.houses[corner].append(house)
            for i in range(3):
                next_house_place = Place(
                    house, isHouse=True, pos=house_pos_corner[i + 1]
                )
                house.next_place = next_house_place
                house = next_house_place
                self.houses[corner].append(house)

        self.start_places[0].prev_place = current_place
        current_place.next_place = self.start_places[0]

        # Link entrances and houses
        for pid in range(4):
            self.start_places[pid].prev_place.entrance_to_house_of_player = self.houses[
                pid
            ][0]
            self.houses[pid][0].prev_place = self.start_places[pid].prev_place

    def transformCoord(self, pos, rot_angle, bias):
        c, s = np.cos(rot_angle), np.sin(rot_angle)
        R = np.array([[c, -s], [s, c]])
        return R.dot(pos.T).T + bias

    def _init_players(self):

        colors = ["blue", "red", "green", "yellow"]

        self.players = [
            Player(i, self.start_places[i], self.bases[i], self.houses[i], colors[i])
            for i in range(self.number_of_players)
        ]
        self.current_pid = 0
        self.current_player = self.players[0]

    def _loopPlaces(self):
        places = [self.start_places[0]]
        current = places[-1].next_place
        while current != self.start_places[0]:
            places.append(current)
            current = current.next_place
        return places

    def drawField(self):

        for place in self._loopPlaces():
            if place.player != None:
                outer_color = place.player.color
            # elif place.entrance_to_house_of_player != None:
            # outer_color = place.entrance_to_house_of_player.player.color
            else:
                outer_color = "black"
            if place.players_figure != None:
                inner_color = place.players_figure.player.color
            else:
                inner_color = "white"
            self.create_oval(
                place.pos[0],
                place.pos[1],
                place.pos[0] + self.cs,
                place.pos[1] + self.cs,
                fill=inner_color,
                outline=outer_color,
            )

        for pid in range(4):
            for place in self.bases[pid]:
                if place.player != None:
                    outer_color = place.player.color
                else:
                    outer_color = "black"
                if place.players_figure != None:
                    inner_color = place.players_figure.player.color
                else:
                    inner_color = "white"
                self.create_oval(
                    place.pos[0],
                    place.pos[1],
                    place.pos[0] + self.cs,
                    place.pos[1] + self.cs,
                    fill=inner_color,
                    outline=outer_color,
                )

        for pid in range(4):
            for place in self.houses[pid]:
                if place.player != None:
                    outer_color = place.player.color
                else:
                    outer_color = "black"
                if place.players_figure != None:
                    inner_color = place.players_figure.player.color
                else:
                    inner_color = "white"
                self.create_oval(
                    place.pos[0],
                    place.pos[1],
                    place.pos[0] + self.cs,
                    place.pos[1] + self.cs,
                    fill=inner_color,
                    outline=outer_color,
                    dash=(3, 2),
                )
