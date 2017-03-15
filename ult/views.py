from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShuffleWaitPage:

    # 예외처리 해야 하는 사람이 있어 그루핑을 수동 셔플링 했다.
    def after_all_players_arrive(self):

        players = self.subsession.get_players()

        random.shuffle(players) # 그룹 셔플.

        new_group=[]

        # 예외자를 뽑아내서 따로 그룹 만든다.
        for p in players:
            if p.is_exception:
                new_group.append([p])
                players.remove(p)

        #예외자가 나오는 경우 반드시 짝수가 된다.
        while players:
            new_group.append([players.pop(),players.pop()])

        self.subsession.set_group_matrix(new_group)

    def is_displayed(self):
        return self.round_number==1

class Introduction(Page):
    pass

class ExceptionPage:
    def is_displayed(self):
        return self.player.is_exception == True

class Offer:

    def is_displayed(self):
        return (self.player.id_in_group == 1 and not(self.player.is_exception))

class WaitForProposer(WaitPage):
    pass

class Accept:

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.player.is_exception

class ResultsWaitPage:

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass
