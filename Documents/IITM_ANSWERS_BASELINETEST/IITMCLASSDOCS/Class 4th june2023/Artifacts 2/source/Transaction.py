# States of both coordinator and participant during commit protocol
INITIAL_STATE = 'Initial State'
UNDECIDED_STATE = 'Undecided State'
READY_STATE = 'Ready State'
COMMIT_STATE = 'Commit State'
ABORT_STATE = 'Abort State'

class Transaction:
    def __init__(self, id, tx_manager, forceDisAgree=False):
        self._id = id
        self._tx_manager = tx_manager
        self._state = INITIAL_STATE
        self.forceDisAgree = forceDisAgree

    def __str__(self):
        return f'Transaction id = {self._id}, with state \'{self._state}\''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
