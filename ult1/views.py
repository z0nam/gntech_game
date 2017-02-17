from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True
# utl1에서는 취향 질문에 따라 역할을 배정한다. 질문은 binary choice q1, q2
# 일단 q1에 기반하여 매칭한 뒤, 남는 사람들을 q2로 매칭하고 그래도 남는 사람들은
# 임의배정하는 알고리즘을 사용하기로 함.


    def after_all_players_arrive(self):
        rnd_num = random.randint(1,2)  #이 값이 q1- 1이 맡게 될 group id임.
        logging.debug("rnd_num={}".format(rnd_num))

        players = self.subsession.get_players() # 일단 플레이어를 모두 모은다.

        q1_1_players = [p for p in players if p.participant.vars['q1']==True]
        q1_2_players = [p for p in players if p.participant.vars['q1']==False]

        group_matrix = []

        count1 = len(q1_1_players)
        count2 = len(q1_2_players)

        if count1 < count2:
            smallerGroup = q1_1_players
            largerGroup = q1_2_players
        else:
            smallerGroup = q1_2_players
            largerGroup = q1_1_players

        while smallerGroup:
            if rnd_num == 1:
                new_group = [
                    q1_1_players.pop(),
                    q1_2_players.pop()
                ]
            else:
                new_group = [
                    q1_2_players.pop(),
                    q1_1_players.pop()
                ]
            group_matrix.append(new_group)

        # 이 과정을 거치면 둘 중 더 많은 놈이 남는다. 따라서 q2에 기반하여 동일한 내용을 반복한다.

        rnd_num = random.randint(1,2)

        q2_1_players = [p for p in largerGroup if p.participant.vars['q2'] == True]
        q2_2_players = [p for p in largerGroup if p.participant.vars['q2'] == False]

        count1 = len(q2_1_players)
        count2 = len(q2_2_players)

        if count1 < count2:
            smallerGroup = q2_1_players
            largerGroup = q2_2_players
        else:
            smallerGroup = q2_2_players
            largerGroup = q2_1_players

        while smallerGroup:
            if rnd_num == 1:
                new_group = [
                    q2_1_players.pop(),
                    q2_2_players.pop()
                ]
            else:
                new_group = [
                    q2_2_players.pop(),
                    q2_1_players.pop()
                ]
            group_matrix.append(new_group)

            # 이러고도 남는 아이들은 어쩔 수 없이 랜덤으로 배치한다.
        while largerGroup:
            if len(largerGroup) > 1:
                new_group = [
                    largerGroup.pop(),
                    largerGroup.pop()
                ]
            # 만일 한 명만 남았다면 이 사람은 예외 처리를 해야 한다. 이것을 처리하기 위해서는 크게 두 가지 방식이 있다. (1) 게임 밖에서 처리하는 방식. 즉, 이때는 참가자가 홀수일 경우 추첨을 해서 한 사람 빼고 나머지 짝수 인원으로만 하게 해서 절대 이런 상황이 나오지 않게 하는 것인데, 경험상 좋지 않다. (2) 예외처리를 하는 방법. 코딩이 복잡해지는데, 예외 플래그를 만들어서 체크하는 수 밖에 없을 듯하다.
            elif len(largerGroup) == 1:
                largerGroup.pop().is_exception = True
            group_matrix.append(new_group)

        self.subsession.set_group_matrix(group_matrix)

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
