from otree.api import Bot, SubmissionMustFail, cu

from . import C, Decide, RoundResults


class PlayerBot(Bot):
    def play_round(self):
        # REQ-0001 rule 3: contributions are bounded by the endowment.
        yield SubmissionMustFail(Decide, dict(contribution=C.ENDOWMENT + cu(1)))
        yield SubmissionMustFail(Decide, dict(contribution=cu(-1)))

        # Alternate free-riding and full contribution so the history table on
        # the decision page has varied content to render.
        amount = cu(0) if self.player.id_in_group % 2 else C.ENDOWMENT
        yield Decide, dict(contribution=amount)
        yield RoundResults
