from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


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
        pass


class Results(Page):
    pass


page_sequence = [
    Introduction,
    ExceptionPage,
    Offer,
    WaitForProposer,
    Accept,
    ResultsWaitPage,
    Results
]
