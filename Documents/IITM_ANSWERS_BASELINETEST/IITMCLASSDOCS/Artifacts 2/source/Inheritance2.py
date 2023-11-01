from Inheritance import CoralCard, GlobeTrotterCard
class ManageCoralCard:
    def __init__(self, card_details):
        coral_card_object = CoralCard(card_details) # Create an instance of CoralCard
        self.card = coral_card_object # Property card is assigned with coral_card (object)
        owner_variable = card_details["owner"]  # Property is assigned with string
        self.owner = owner_variable  # Property is assigned with owner_variable (string)

    def update_discount_amount(self):
        # self.card.get_partner_spend()
        # self.card => Object of Coral Card
        # self.card.<Functions / Attributes on that Object>
        partner_spend_amount = self.card.get_partner_spend() # Method call from property (Object)
        if partner_spend_amount > 200000 and partner_spend_amount <= 300000:
            self.card.update_partner_discount(18)
            print("Partner discount is not at 18%")
        elif partner_spend_amount > 300000 and partner_spend_amount < 400000:
            self.card.update_partner_discount(20)
            print("Partner discount is not at 20%")
        else:
            print("No change in Partner discount")

    def record_new_transaction(self, brand, amount):
        updated_amount = self.card.calculate_transaction_amount(brand, amount)
        if updated_amount < amount:
            self.card.update_partner_spend(updated_amount)
        self.card.update_transaction_amount(updated_amount)

class ManageGlobeTrotter:
    def __init__(self, card):
        self.card = GlobeTrotterCard(card)
        self.owner = card["owner"]

    def new_lounge_visit(self):
        return self.card.lounge_visit()

