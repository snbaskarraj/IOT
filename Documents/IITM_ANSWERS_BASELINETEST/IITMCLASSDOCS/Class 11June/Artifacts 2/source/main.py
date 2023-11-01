# Code Walk through.
from termcolor import colored
from naive_store import DataStore
from lock_store import LockDataStore
from vector_clock_store import VectorClockDataStore


# Basic Implementation of the 2 Nodes DataStores where one of the node informs the other
# node when the operation is complete.
# operations Supported by the Store -> Add and Multiply.

# Naive Strategy - Nodes Sends a message to another node when the event is done.
def naive_strategy():
    # Setting up the stores for 2 nodes

    # Creating a Store for node1, say s1
    s1 = DataStore({})
    # Initialize the data in the store
    s1.set_data('x', 5)

    # Creating a Store for node2, say s2
    s2 = DataStore({})
    # Initialize the data in the store
    s2.set_data('x', 5)

    # Run without overlap
    # At any given point of time only onr store is performing the operation
    s1.add('x', 2)
    s2.receive_event('x', s1.get_data('x'))
    s2.multiply('x', 3)
    s1.receive_event('x', s2.get_data('x'))
    s1_value = s1.get_data('x')
    s2_value = s2.get_data('x')
    # Everything would work fine in this case since all replicas received an update before a new write
    print(f'Correct Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')

    # Run with overlap

    # Resetting the value of 'x' key to 5
    s1.set_data('x', 5)
    s2.set_data('x', 5)
    #s1_value = 0
    #s2_value = 0

    s1.add('x', 2) # 5 + 2 = 7
    s2.multiply('x', 3) # 5 *3 = 15
    s2.receive_event('x', s1.get_data('x')) # value updated to 7
    s1.receive_event('x', s2.get_data('x')) # value 7 is sent back again
    s1_value = s1.get_data('x')
    s2_value = s2.get_data('x')
    # One of the writes would be lost in this case as there are concurrent writes.
    # The final value would also depend on the order of events received after the concurrent writes
    print(f'Incorrect Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')

# Lock Strategy - Nodes locks when a write operation is done across all nodes to maintain consistency.
def lock_strategy():
    # Setting up the stores for 2 nodes

    # Creating a Store for node1, say s1
    s1 = LockDataStore({})
    # Initialize the data in the store
    s1.set_data('x', 5)

    # Creating a Store for node2, say s2
    s2 = LockDataStore({})
    # Initialize the data in the store
    s2.set_data('x', 5)

    # Let each store know what are it's replica
    s1.add_replicas([s2])
    s2.add_replicas([s1])

    # In case of concurrent writes, the second one will not be able to lock the data to write to it
    # It'll return failure.
    # In normal cases, there is a wait mechanism on the lock, and failure after a wait timeout
    add_result = s1.add('x', 2)
    if add_result == -1:
        print('Failed to acquire locks, please retry')
    mul_result = s2.multiply('x', 3)
    if mul_result == -1:
        print('Failed to acquire locks, please retry')

    s1_value = s1.get_data('x')
    s2_value = s2.get_data('x')
    # Everything would work fine in this case since all replicas receive the same update under lock
    print(f'Correct Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')

# Vector lock Strategy - To utilize the system resources effectively we are creating a simple counter ( in real world
# mapped to a time stamp ) which helps the system decide to update replicas and also notify the system for concurrent
# writes.
# Every write would implicitly publish the data to the peers.
def vector_clock_strategy():
    # Setting up the stores for 2 nodes

    # Creating a Store for node1, say s1 and use it as a key to the vector clock
    s1 = VectorClockDataStore({}, 's1')
    # Initialize the data in the store
    s1.set_data('x', 5)

    # Creating a Store for node2, say s2 and use it as a key to the vector clock
    s2 = VectorClockDataStore({}, 's2')
    # Initialize the data in the store
    s2.set_data('x', 5)

    # Let each store know what are it's replica
    s1.add_replicas([s2])
    s2.add_replicas([s1])

    # Initialize the counter/clock to zero on each node
    s1.reset_vector_clock()
    s2.reset_vector_clock()

    # Run without overlap
    print(f'Initial: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s1.add('x', 2)
    print(f'After add in s1: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s2.receive_event('x', s1.get_data('x'), s1.vector_clock)
    print(
        colored(
            f'After update in s2 for the add event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}',
            'blue'))
    s2.multiply('x', 3)
    print(f'After multiply in s2: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s1.receive_event('x', s2.get_data('x'), s2.vector_clock)
    print(
        colored(
            f'After update in s1 for the multiply event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}',
            'blue'))
    s1_value = s1.get_data('x')
    s2_value = s2.get_data('x')
    # Everything would work fine in this case since all replicas received an update before a new write
    print(f'Correct Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}\n')

    # Resetting the value of 'x' key to 5 and resetting the clocks
    s1.set_data('x', 5)
    s2.set_data('x', 5)
    s1.reset_vector_clock()
    s2.reset_vector_clock()

    # Run with overlap
    print(f'Initial: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s1.add('x', 2)
    print(f'After add in s1: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s2.multiply('x', 3)
    print(f'After multiply in s2: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
    s2.receive_event('x', s1.get_data('x'), s1.vector_clock)
    print(
        colored(
            f'After update in s2 for the add event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}',
            'blue'))
    s1.receive_event('x', s2.get_data('x'), s2.vector_clock)
    print(
        colored(
            f'After update in s1 for the multiply event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}',
            'blue'))
    s1_value = s1.get_data('x')
    s2_value = s2.get_data('x')
    # One of the writes would be lost in this case as there are concurrent writes.
    # However due to clash in vector clocks, the system can flag this to the application or take a predefined decision
    # In this case, it chose to implement the write based on the first receiver event
    # The final value would also depend on the order of events received after the concurrent writes
    # Last Write Wins
    print(f'Incorrect Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #naive_strategy()
    #lock_strategy()
    vector_clock_strategy()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
