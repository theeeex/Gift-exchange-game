from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import os

author = 'XIA Mingxiang'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'giftexchange'
    players_per_group = 2
    num_rounds = 3

    instruction_template = 'giftexchange/Instruction.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(round_number=1)

    def vars_for_admin_report(self):
        highchart_data = []
        for i in self.in_all_rounds():
            highchart_data.extend(i.get_data())
        return {'highcharts_series': highchart_data}

    def get_data(self):
        data = []
        group = self.get_groups()
        for g in group:
            for i in range(0, 9 + 1, 1):
                data.append([i, getattr(g, 'agent_effort_{}'.format(i))])
        return data


def make_field(amount):
    return models.IntegerField(label='How much effort would you return for a wage offer of {}'.format(amount),
                               choices=range(0, 9 + 1, 1), widget=widgets.RadioSelectHorizontal)


class Group(BaseGroup):
    total_return = models.CurrencyField()
    principal_wage_offer = models.IntegerField(label='Fixed Payment (from 0 to 9):', min=0, max=9)
    effort_agent = models.IntegerField()

    agent_effort_0 = make_field(c(0))
    agent_effort_1 = make_field(c(1))
    agent_effort_2 = make_field(c(2))
    agent_effort_3 = make_field(c(3))
    agent_effort_4 = make_field(c(4))
    agent_effort_5 = make_field(c(5))
    agent_effort_6 = make_field(c(6))
    agent_effort_7 = make_field(c(7))
    agent_effort_8 = make_field(c(8))
    agent_effort_9 = make_field(c(9))

    cost_agent = models.CurrencyField()
    money_agent = models.CurrencyField()
    money_principal = models.CurrencyField()

    def set_payoffs(self):
        principal = self.get_player_by_id(1)
        agent = self.get_player_by_id(2)

        self.effort_agent = getattr(self, 'agent_effort_{}'.format(self.principal_wage_offer))
        self.cost_agent = c((self.effort_agent ** 2) * 0.13)
        self.money_agent = c(self.principal_wage_offer)
        self.money_principal = c(1.5 * self.effort_agent)
        self.total_return = self.money_principal

        principal.payoff = self.money_principal - self.money_agent
        agent.payoff = self.money_agent - self.cost_agent


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'principle'
        else:
            return 'agent'









