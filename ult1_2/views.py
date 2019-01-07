from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True
# ult1의 group_matrix 를 가지고 와서 p1과 p2를 swap한다.

    def after_all_players_arrive(self):
        prev_group_matrix = self.session.vars['groupSetting']
        new_group_matrix = []
        for grp in prev_group_matrix:
            if len(grp)!=2:
                new_group=[self.get_player_by_pid(grp[0])]
            else:
                new_group = [self.get_player_by_pid(grp[1]),self.get_player_by_pid(grp[0])]
            new_group_matrix.append(new_group)

        self.subsession.set_group_matrix(new_group_matrix)

# 게임을 여러 라운드 할 경우에는 나머지 라운드의 그룹도 동일하게 설정하도록 한다.
        if Constants.num_rounds > 1:
            for subsession in self.subsession.in_rounds(2, Constants.num_rounds):
                subsession.group_like_round(1)

        def is_displayed(self):
            return self.round_number==1


class Introduction(Page):
    pass

class ExceptionPage(Page):
    def is_displayed(self):
        return self.player.is_exception == True

class Offer(Page):
    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return (self.player.id_in_group == 1 and not(self.player.is_exception))

class WaitForProposer(WaitPage):
    pass

class Accept(Page):
    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.player.is_exception

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [
    ShuffleWaitPage,
    Introduction,
    ExceptionPage,
    Offer,
    WaitForProposer,
    Accept,
    ResultsWaitPage,
    Results
]
