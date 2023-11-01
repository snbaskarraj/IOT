# Code Walk through.
from termcolor import colored
from TxManager import TxManager, COORDINATOR_TYPE, PARTICIPANT_TYPE


def initiate2PCPhase1WithParticipantsInAgreement():
    # Initiate transaction manager on three nodes
    txm_coord = TxManager(COORDINATOR_TYPE)
    txm_part1 = TxManager(PARTICIPANT_TYPE)
    txm_part2 = TxManager(PARTICIPANT_TYPE)

    # Add sibling nodes in each manager
    txm_coord.add_sibling_nodes([txm_part1, txm_part2])
    txm_part1.add_sibling_nodes([txm_coord, txm_part2])
    txm_part2.add_sibling_nodes([txm_coord, txm_part1])

    txm_part1.set_coordinator(txm_coord)
    txm_part2.set_coordinator(txm_coord)

    # Initialize transactions
    coord_tx = txm_coord.init_transaction()
    tx_id = coord_tx.id
    part1_tx = txm_part1.init_transaction(tx_id)
    part2_tx = txm_part2.init_transaction(tx_id)

    print('Initial Transaction State:')


    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')
    print('\n')

    txm_coord.initiate_2pc(tx_id)

    print('\nTransaction State After First Phase:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')

def initiate2PCPhase1WithFirstParticipantNotInAgreement():
    # Initiate transaction manager on three nodes
    txm_coord = TxManager(COORDINATOR_TYPE)
    txm_part1 = TxManager(PARTICIPANT_TYPE)
    txm_part2 = TxManager(PARTICIPANT_TYPE)

    # Add sibling nodes in each manager
    txm_coord.add_sibling_nodes([txm_part1, txm_part2])
    txm_part1.add_sibling_nodes([txm_coord, txm_part2])
    txm_part2.add_sibling_nodes([txm_coord, txm_part1])

    txm_part1.set_coordinator(txm_coord)
    txm_part2.set_coordinator(txm_coord)

    # Initialize transactions
    coord_tx = txm_coord.init_transaction()
    tx_id = coord_tx.id
    part1_tx = txm_part1.init_transaction(tx_id, True)
    part2_tx = txm_part2.init_transaction(tx_id)

    print('Initial Transaction State:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')
    print('\n')

    txm_coord.initiate_2pc(tx_id)

    print('\nTransaction State After First Phase:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')

def initiate2PCPhase1WithSecondParticipantNotInAgreement():
    # Initiate transaction manager on three nodes
    txm_coord = TxManager(COORDINATOR_TYPE)
    txm_part1 = TxManager(PARTICIPANT_TYPE)
    txm_part2 = TxManager(PARTICIPANT_TYPE)

    # Add sibling nodes in each manager
    txm_coord.add_sibling_nodes([txm_part1, txm_part2])
    txm_part1.add_sibling_nodes([txm_coord, txm_part2])
    txm_part2.add_sibling_nodes([txm_coord, txm_part1])

    txm_part1.set_coordinator(txm_coord)
    txm_part2.set_coordinator(txm_coord)

    # Initialize transactions
    coord_tx = txm_coord.init_transaction()
    tx_id = coord_tx.id
    part1_tx = txm_part1.init_transaction(tx_id)
    part2_tx = txm_part2.init_transaction(tx_id, True)

    print('Initial Transaction State:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')
    print('\n')

    txm_coord.initiate_2pc(tx_id)

    print('\nTransaction State After First Phase:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')

def initiate2PCPhase1WithBothParticipantsNotInAgreement():
    # Initiate transaction manager on three nodes
    txm_coord = TxManager(COORDINATOR_TYPE)
    txm_part1 = TxManager(PARTICIPANT_TYPE)
    txm_part2 = TxManager(PARTICIPANT_TYPE)

    # Add sibling nodes in each manager
    txm_coord.add_sibling_nodes([txm_part1, txm_part2])
    txm_part1.add_sibling_nodes([txm_coord, txm_part2])
    txm_part2.add_sibling_nodes([txm_coord, txm_part1])

    txm_part1.set_coordinator(txm_coord)
    txm_part2.set_coordinator(txm_coord)

    # Initialize transactions
    coord_tx = txm_coord.init_transaction()
    tx_id = coord_tx.id
    part1_tx = txm_part1.init_transaction(tx_id, True)
    part2_tx = txm_part2.init_transaction(tx_id, True)

    print('Initial Transaction State:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')
    print('\n')

    txm_coord.initiate_2pc(tx_id)

    print('\nTransaction State After First Phase:')
    print(f'Coordinator Tx: {coord_tx}')
    print(f'Participant 1 Tx: {part1_tx}')
    print(f'Participant 2 Tx: {part2_tx}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initiate2PCPhase1WithParticipantsInAgreement()

    initiate2PCPhase1WithFirstParticipantNotInAgreement()

    initiate2PCPhase1WithSecondParticipantNotInAgreement()

    # Excersise - Both are not in agreement.
    #initiate2PCPhase1WithBothParticipantsNotInAgreement()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
