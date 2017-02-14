from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Namun Cho'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'ult1'
    players_per_group = 2
    endowment = c(1000)
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    proposed_amount = models.CurrencyField(min=0,max=Constants.endowment)

    accept_reject = models.BooleanField() # true:accept, false:reject

    def role(self):
        if self.id_in_group == 1:
            return 'Proposer'
        if self.id_in_group == 2:
            return 'Responder'
