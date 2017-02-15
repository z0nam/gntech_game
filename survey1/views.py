from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class Survey(Page):
    form_model = models.Player
    form_fields = ['q1','q2']

    def before_next_page(self):
        self.player.setProperty()


class WaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


page_sequence = [
    Introduction,
    Survey,
    WaitPage
]
