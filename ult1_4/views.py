from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    # 예외처리 해야 하는 사람이 있어 그루핑을 수동 셔플링 했다.
    def after_all_players_arrive(self):

        players = self.subsession.get_players()

        random.shuffle(players) # 그룹 셔플.
        print(len(players))
        new_group=[]
        # 예외자를 뽑아내서 따로 그룹 만든다.
        for p in players:
            if p.is_exception:
                print("exception player")
                print(p.id)
                print(p.is_exception)
                new_group.append([p])
                players.remove(p)

        print(len(players))
        print(new_group)
        #예외자가 나오는 경우 반드시 짝수가 된다.
        while players:
            new_group.append([players.pop(),players.pop()])

        self.subsession.set_group_matrix(new_group)

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

class Payoff(Page):
    pass


page_sequence = [
    ShuffleWaitPage,
    Introduction,
    ExceptionPage,
    Offer,
    WaitForProposer,
    Accept,
    ResultsWaitPage,
    Results,
    Payoff
]
