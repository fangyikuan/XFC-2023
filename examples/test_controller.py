# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.
import numpy as np

from src.kesslergame import KesslerController
from typing import Dict, Tuple


class TestController(KesslerController):
    def __init__(self):
        self.eval_frames = 0

    def relative_vec(self, ships, game):
        num_asteroids = len(game['asteroids'])
        ship = ships['position']
        vecs = np.zeros(shape=(num_asteroids,4))
        # relative vecs x, y, r, angle, speedx, speedy
        for i in range(num_asteroids):
            vecs[i,0] = game['asteroids'][i]['position'][0] - ship[0]
            vecs[i, 1] = game['asteroids'][i]['position'][1] - ship[1]
            vecs[i,2] = np.sqrt(vecs[i,0]**2+vecs[i, 1]**2)
            vecs[i, 3] = np.arctan(vecs[i, 1]/vecs[i, 0])
            vecs[i, 3] = vecs[i, 3] / 3.14 * 180
        return vecs
    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        """
        Method processed each time step by this controller.
        """
        vec = self.relative_vec(ship_state, game_state)
        vec = vec[vec[:,2].argsort()]
        ship = ship_state['position']
        mean = np.mean(vec[0:10,:2], axis=0)
        target = np.argmin(vec[:, 2])
        ## heading
        turn_rate = vec[target, 3] - ship_state['heading']
        turn_rate = turn_rate
        ## speed
        thrust = vec[target, 2] * np.cos(180-vec[target, 3]+ship_state['heading'])
        fire = True
        # targets = np.argwhere(vec[:,2] < 100)
        # if len(targets) == 0:
        #     fire = False
        #     thrust = np.sum(mean * np.cos(ship_state["heading"]))
        #     target = np.argmin(vec[:, 2])
        #     turn_rate = 1.1 * vec[target, 3]
        # else:
        #     target = np.argmin(vec[:,2])
        #     fire = True
        #     turn_rate =2 * vec[target, 3]
        #     thrust = 0
        #     # thrust = vec[target, :2] * np.cos(ship_state["heading"]-vec[target, 3])
        #     # thrust = np.sqrt()

        self.eval_frames +=1

        return thrust, turn_rate, fire



    # def center(self, num=10):


    @property
    def name(self) -> str:
        return "Test Controller"
