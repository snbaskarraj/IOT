from abc import ABC, abstractmethod


class OfferManager:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, topic, offername):
        for subscriber in self.subscribers:
            subscriber.update(topic, offername)


class OfferLauncher:
    def __init__(self):
        self.offer = OfferManager()
        self.offer_name = None
        self.offer_state = "Off"

    def launch_offer(self, offer_name):
        if self.offer_state == "On":
            return
        self.offer_name = offer_name
        self.offer_state = "On" # Subject is changed
        self.offer.notify("Offer starting now!", self.offer_name) # Notifies the subscribers

    def close_offer(self):
        if self.offer_state == "Off":
            return
        self.offer_state = "Off"
        self.offer.notify("Offer closed.", self.offer_name)


class Subscriber(ABC):
    @abstractmethod
    def update(self, topic, offername):
        pass


class SubscriberWithContactNumber(Subscriber):
    def __init__(self, contact_num):
        self.contact_num = contact_num
        self.message = None

    def update(self, topic, offername):
        self.message = topic + " " + offername
        print(f"{self.message} to subscriber with contact number {self.contact_num}")


class SubscriberWithEmail(Subscriber):
    def __init__(self, contact_email):
        self.contact_email = contact_email
        self.message = None

    def update(self, topic, offername):
        self.message = topic + " " + offername
        print(f"{self.message} to subscriber with email id {self.contact_email}")


if __name__ == "__main__":
    # Subject
    offer_launcher = OfferLauncher()

    # Observers with Phone numbers
    subscriber1 = SubscriberWithContactNumber(92877427)
    subscriber2 = SubscriberWithContactNumber(92817478)
    subscriber3 = SubscriberWithContactNumber(97438777)

    # Observers with Email Address
    subscriber4 = SubscriberWithEmail("subs4@gmail.com")
    subscriber5 = SubscriberWithEmail("subs5@gmail.com")
    subscriber6 = SubscriberWithEmail("subs6@gmail.com")

    # Attempt to change the state of a subject
    offer_manager = offer_launcher.offer

    offer_manager.subscribe(subscriber1)
    offer_manager.subscribe(subscriber2)
    offer_manager.subscribe(subscriber3)
    offer_manager.subscribe(subscriber4)
    offer_manager.subscribe(subscriber5)
    offer_manager.subscribe(subscriber6)

    offer_launcher.launch_offer("Flat 50% off on all garments")
    print()
    offer_launcher.close_offer()
    print()

    offer_launcher.offer.unsubscribe(subscriber4)

    offer_launcher.launch_offer("Buy 2 get 1 free on all stationary items")
    print()
    offer_launcher.close_offer()
    print()

    offer_launcher.offer.unsubscribe(subscriber1)

    offer_launcher.launch_offer("Buy 2 get 1 free on all stationary items")
    print()
    offer_launcher.close_offer()
    print()
