from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Wage(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1

    form_model = 'group'
    form_fields = ['principal_wage_offer']


class Effort(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2

    form_model = 'group'
    def get_form_fields(self):
        return ['agent_effort_{}'.format(i) for i in range(0, 9 + 1, 1)]


class ResultWaitPage(WaitPage):

    title_text = 'Please Wait'
    body_text = 'Waiting for the other participant.'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [Introduction, Effort, Wage, ResultWaitPage, Results]
