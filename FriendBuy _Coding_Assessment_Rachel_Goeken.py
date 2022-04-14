'''
Memory could become an issue if someone does multiple begin commands since the program is utilizing linked lists
Once commit you will be dropping back down to one Node

get, set, unset are all O(1) due to storing the last element as a variable and utilizing python dictionaries (which are
hashmaps)
numequalto is O(log n) due to bisect which is a binary search
'''

import sys
import copy
import bisect as b

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

class DoubleLinkedList():
    def __init__(self):
        self.head = None

    def insert_to_empty_list(self, data):
        if self.head is None:
            new_node = Node(data)
            self.head = new_node

    # Insert element at the end
    def insert_at_end(self, data):
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
            return
        n = self.head
        while n.next is not None:
            n = n.next
        new_node = Node(data)
        n.next = new_node
        new_node.prev = n

    # Delete the elements from the end
    def delete_at_end(self):
        if self.head is None:
            print("The Linked list is empty, no element to delete")
            return
        if self.head.next is None:
            self.head = None
            return
        n = self.head
        while n.next is not None:
            n = n.next
        n.prev.next = None

    # Traversing and Displaying each element of the list debugging
    def display(self):
        if self.head is None:
            return
        else:
            n = self.head
            while n is not None:
                print("Element is: ", n.data)
                n = n.next
        print("\n")

class Database():
    def __init__(self):
        self.allElements = DoubleLinkedList()
        self.allElements.insert_to_empty_list({})
        self.last_node = self.allElements.head

    def begin(self):
        self.allElements.insert_at_end({})
        self.last_node = self.last_node.next
        if self.allElements.head.data != {}:
            self.last_node.data = copy.deepcopy(self.allElements.head.data)


    def rollback(self):
        if self.allElements.head == None or self.allElements.head.next == None:
            return 'NO TRANSACTION'
        else:
            self.last_node = self.last_node.prev
            self.allElements.delete_at_end()

        return ''

    def commit(self):
        if self.allElements.head == None:
            return 'NO TRANSACTIONS'
        else:
            node = self.last_node

            while node.prev:
                prev_node = node.prev
                for i in node.data:
                    value = prev_node.data.get(i, None)
                    if value != None or self.allElements.head == prev_node:
                        prev_node.data[i] = node.data[i]
                self.allElements.delete_at_end()
                node = node.prev

            self.last_node = self.allElements.head

        return ''

    #for debugging
    def print_database(self):
        self.allElements.display()

    # O(1) since keeping track of the last item in the list
    # dictionaries are hashmaps
    def set_name_value(self, name, value):
        if self.allElements.head == None:
            self.allElements.insert_to_empty_list({})
        node = self.last_node
        node.data[name] = value

    #O(1) since keeping track of the last item in the list
    #dictionaries are hashmaps
    def get_name(self, name):
        if self.allElements.head == None:
            return None
        return self.last_node.data.get(name, None)

    def end(self):
        return sys.exit(0)

    def numequalto(self, value):
        arr = list(self.last_node.data.values())

        #handles with binary search so O(log n)
        return(b.bisect_right(arr, value) - b.bisect_left(arr, value))

    # O(1) since keeping track of the last item in the list
    # dictionaries are hashmaps
    def unset_name(self, name):
        self.last_node.data[name] = None

def main():
    database = Database()
    while True:
        val = input("")
        command = val.split(" ")

        #this could also be a switch statement
        if command[0] == 'SET' and len(command) == 3:
            database.set_name_value(command[1], command[2])
        elif command[0] == 'GET' and len(command) == 2:
            print(database.get_name(command[1]))
        elif command[0] == 'UNSET' and len(command) == 2:
            database.unset_name(command[1])
        elif command[0] == 'NUMEQUALTO' and len(command) == 2:
            print(database.numequalto(command[1]))
        elif command[0] == 'BEGIN' and len(command) == 1:
            database.begin()
        elif command[0] == 'COMMIT' and len(command) == 1:
            print(database.commit())
        elif command[0] == 'ROLLBACK' and len(command) == 1:
            print(database.rollback())
        elif command[0] == 'END' and len(command) == 1:
            database.end()
        elif command[0] == 'PRINT' and len(command) == 1:
            database.print_database()
        else:
            print('\nCommand not in the correct format')
            print('Your commands are (they are case sensitive):')
            print('SET name value')
            print('GET name')
            print('UNSET name')
            print('NUMEQUALTO value')
            print('BEGIN')
            print('COMMIT')
            print('ROLLBACK')
            print('END\n')

main()
