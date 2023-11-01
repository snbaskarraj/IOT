# Code Walk through.
from Inheritance import CoralCard, GlobeTrotterCard
from Inheritance2 import ManageCoralCard, ManageGlobeTrotter
from Queue_Demo import Queue1, Queue2
from RectAndSquare import Rectangle, Square, NewSquare
from coupling import ManageCoralCard2, ManageCard


def get_card_details(credit_card):
    print(credit_card.get_number())
    print(credit_card.get_subscription_fee())


def IsARelationShipImplementation():
    # 1. Define a Dictionary to be associated with a coral card...
    # The dictionary has 3 Keys initialized below.
    coral_card_details = {"number": 3408214567342358,
                          "yearly_subscription_fee": 2000,
                          "yearly_subscription_fee_wavier_limit": 300000}

    # 2. Define a Dictionary to be associated with a globe trotter card...
    globe_trotter_card_details = {"number": 4588214567348975,
                                  "yearly_subscription_fee": 5000,
                                  "yearly_subscription_fee_wavier_limit": 500000}

    # __init__(self, card): Create an Instance of Coral Card
    # By passing the basic card details...
    coral_card = CoralCard(coral_card_details)
    global_card = GlobeTrotterCard(globe_trotter_card_details)

    number = coral_card.get_number()
    print(number)

    partner_spend = coral_card.get_partner_spend()
    print(partner_spend)

    number = global_card.get_number()
    print(number)

    limit = global_card.get_lounge_visit_count()
    print(limit)



# get_card_details(coral_card)
# get_card_details(global_card)


def HasARelationShipImplementation():
    coral_card_details = {"number": 3408214567342358,
                          "yearly_subscription_fee": 2000,
                          "yearly_subscription_fee_wavier_limit": 300000,
                          "owner": "Kapil Dev"}

    manage_card = ManageCoralCard(coral_card_details)

    number = manage_card.card.get_number()
    print(number)

    manage_card.update_discount_amount()
    manage_card.record_new_transaction("Lamy", 8000)


def QueueHasAList():
    my_queue = Queue1()
    my_queue.enque(4)
    my_queue.enque(14)
    my_queue.enque(24)
    print(my_queue.data_list)


def QueueIsAList():
    my_queue = Queue2()
    my_queue.enque(4)
    my_queue.enque(14)
    my_queue.enque(24)
    print(my_queue)


def RectIsASquare():
    small_square = Square(5)
    print(small_square.get_area())
    small_square.set_length(6)
    print(small_square.get_area())


def RectIsSquareBaseClassNotHonoured():
    small_square = NewSquare(5)
    print(small_square.get_area())
    small_square.set_length(6)
    print(small_square.get_area())
    small_square.set_width(7)
    print(small_square.get_area())


def TightCoupling():
    globe_trotter_card_details = {"number": 4588214567348975,
                                  "yearly_subscription_fee": 5000,
                                  "yearly_subscription_fee_wavier_limit": 500000,
                                  "owner": "Kapil"}

    manage_card = ManageCoralCard2(globe_trotter_card_details)


def LooseCoupling():
    coral_card_details = {"number": 3408214567342358,
                          "yearly_subscription_fee": 2000,
                          "yearly_subscription_fee_wavier_limit": 300000}

    coral_card = CoralCard(coral_card_details)
    manage_card1 = ManageCard(coral_card, "Kapil")


# Press the green button in the gutter to run the sc
#
#
#
#
# ript.
if __name__ == '__main__':
    # Inheritance
    #IsARelationShipImplementation()
    #HasARelationShipImplementation()

    # Case study-1
    QueueIsAList() # Inheritance
    QueueHasAList() # Composition

    # Case study-2
    RectIsASquare()
    RectIsSquareBaseClassNotHonoured()

    # Coupling
    # TightCoupling()
    # LooseCoupling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
