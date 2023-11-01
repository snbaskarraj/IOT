from Inheritance import CoralCard
class ManageCoralCard2:
    def __init__(self, card):
        self.card = CoralCard(card)
        # This is tight coupling.
        # When we create an object of ManageCoralCard, it get an object of CoralCard
        self.owner = card["owner"]


class ManageCard:
    def __init__(self, credit_card, owner):
        self.card = credit_card
        # This is loose coupling.
        # When we create an object of ManageCard, it get an object either of CoralCard or GlobeTrotterCard
        self.owner = owner
