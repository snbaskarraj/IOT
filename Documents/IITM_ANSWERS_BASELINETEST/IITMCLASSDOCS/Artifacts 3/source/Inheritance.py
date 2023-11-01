class CreditCard():
    def __init__(self, card): #Parameretized Constructor
        self.number = card["number"]
        self.yearly_subscription_fee = card["yearly_subscription_fee"]
        self.yearly_subscription_fee_wavier_limit = card["yearly_subscription_fee_wavier_limit"]
        self.yearly_transaction_amount = 0

    def get_number(self):
        return self.number

    def get_subscription_fee(self):
        if self.yearly_transaction_amount >= self.yearly_subscription_fee_wavier_limit:
            return 0
        return self.yearly_subscription_fee

    def update_transaction_amount(self, amount):
        self.yearly_transaction_amount += amount

class CoralCard(CreditCard):
    def __init__(self, card):
        super().__init__(card) #CreditCard's __init__ method call - Parameretized Constructor
        self.partner_brands = ['Lamy', 'Parker', 'New Balance']
        self.partner_discount = 15
        self.partner_spend = 0

    def get_discount(self, brand):
        if brand in self.partner_brands:
            return self.partner_discount
        return 0

    def get_partner_spend(self):
        return self.partner_spend

    def update_partner_discount(self, discount):
        self.partner_discount = discount

    def calculate_transaction_amount(self, brand, amount):
        discount = self.get_discount(brand)
        if discount:
            amount -= amount * (discount / 100)
        return amount

    def update_partner_spend(self, amount):
        self.partner_spend += amount


class GlobeTrotterCard(CreditCard):
    def __init__(self, card):
        super().__init__(card) #CreditCard's __init__ method call - Parameretized Constructor
        self.airport_lounge_limit = 6
        self.lounge_visit_count = 0

    def get_lounge_visit_count(self):
        return self.airport_lounge_limit

    def increment_lounge_visit(self):
        self.lounge_visit_count += 1

    def lounge_visit_free(self):
        return self.lounge_visit_count <= self.airport_lounge_limit

    def lounge_visit(self):
        self.increment_lounge_visit()
        if self.lounge_visit_free():
            return "Enjoy the free lounge visit"
        return "Please pay for the lounge visit"

