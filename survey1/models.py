from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'survey1'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.BooleanField(initial=None,
        choices=[
            [True,"그렇다"],
            [False,"아니다"]
        ],
        widget=widgets.RadioSelectHorizontal()
    )
    q2 = models.BooleanField(initial=None,
        choices=[
            [True,"그렇다"],
            [False,"아니다"]
        ],
        widget=widgets.RadioSelectHorizontal()
    )

    def setProperty(self):
        self.participant.vars['q1']=self.q1
        self.participant.vars['q2']=self.q2
