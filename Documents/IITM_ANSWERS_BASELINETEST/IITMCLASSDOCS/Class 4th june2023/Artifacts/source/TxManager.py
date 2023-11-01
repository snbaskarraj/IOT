import random
# States of both coordinator and participant during commit protocol
from Transaction import Transaction

INITIAL_STATE = 'Initial State'
UNDECIDED_STATE = 'Undecided State'
READY_STATE = 'Ready State'
COMMIT_STATE = 'Commit State'
ABORT_STATE = 'Abort State'

# Transaction Manager types
COORDINATOR_TYPE = 'Coordinator'
PARTICIPANT_TYPE = 'Participant'

class TxManager:

    # Transaction Manager type is provided at the creation time.
    # The manager stores a list of transactions and sibling nodes which will participate in the distributed commit
    # It also stores a pointer to the coordinator of the group
    # It has a transaction counter to provide each transaction a unique id
    def __init__(self, tm_type):
        self._type = tm_type
        self._transactions = {}
        self._siblings = []
        if tm_type == COORDINATOR_TYPE:
            self._coordinator = self
        else:
            self._coordinator = None
        self._transaction_counter = 0

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, tm_type):
        self._type = tm_type

    # This method adds sibling nodes for each transaction manager
    def add_sibling_nodes(self, sibling_list):
        self._siblings.extend(sibling_list)

    # If a coordinator fails and a new one is relected, this allows to mark the same for the coordinator
    def make_coordinator(self):
        self.type = COORDINATOR_TYPE
        self._coordinator = self

    # If a coordinator fails and a new one is relected, this allows to mark the same for a participant
    def set_coordinator(self, coordinator):
        self._coordinator = coordinator

    # This initiates a transaction in a coordinator or participant
    # A coordinator is not passed the id and will create a local transaction based on the latest counter
    # A participant is passed the id based on what the coordinator created
    # It'll create a local transaction with the same id counter
    def init_transaction(self, id=None, forceDisAgree=False):
        if (id is None):
            self._transaction_counter += 1
            id = self._transaction_counter
        else:
            self._transaction_counter = id
        transaction = Transaction(id, self, forceDisAgree)
        self._transactions[id] = transaction
        return transaction

    # Function to initiate two phase commit protocol
    def initiate_2pc(self, transaction_id):
        if (self.type != COORDINATOR_TYPE):
            print("2pc initiation called on participant node. Bailing out...")
            return -1

        prepare_status = self.trigger_prepare_for_commit(transaction_id)

        # if (prepare_status):
        # EXERCISE FOR THE LEARNER
        # Write code for the second phase based on the algorithm detailed in the video content
        # Get context from how the first phase is implemented and follow the same logic

    # message operations
    # This method will start Phase 1 from the coordinator
    def trigger_prepare_for_commit(self, transaction_id):
        transaction = self._transactions[transaction_id]
        transaction.state = UNDECIDED_STATE
        prepare_status = True

        # The coordinator enters UNDECIDED_STATE and asks all participants to prepare for commit
        for participant in self._siblings:
            result = participant.prepare_for_commit(transaction_id)

            # If any participant returns ABORT, then the prepare is marked as failed
            if (result == 'ABORT'):
                prepare_status = False

        # If prepare was rejected (or timed out) at even a single participant, abort message should be sent to all participants
        # The coordinator will mark its own local transaction as ABORT_STATE and ask all participants to do the same
        if (not prepare_status):
            transaction._state = ABORT_STATE
            for participant in self._siblings:
                participant.abort_commit(transaction_id)
        else:
            transaction._state = READY_STATE
        return prepare_status

    # This method will be called on a participant
    # We have made failure a possibility with 20% probability to naturally highlight all cases on reruns
    # Either all participants can succeed, OR one or more will failed
    # Even a single participant will lead to overall commit failure
    def prepare_for_commit(self, transaction_id):
        transaction = self._transactions[transaction_id]

        # success_choice represents the randomaization of error(s)
        if (False == transaction.forceDisAgree):
            print(f'Participant transaction responded with READY Message')
            transaction._state = READY_STATE
            return 'Ready'
        else:
            print(f'Participant transaction responded with Abort Message')
            transaction._state = ABORT_STATE
            return 'ABORT'

    def abort_commit(self, transaction_id):
        transaction = self._transactions[transaction_id]
        transaction._state = ABORT_STATE
