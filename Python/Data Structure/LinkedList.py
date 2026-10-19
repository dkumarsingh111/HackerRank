class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def print(self):
        temp = self.head
        while (temp):
            print(temp.data, end=" ")
            temp = temp.next


if __name__ == "__main__":

    llist = LinkedList()

    llist.head = Node(10)
    middle = Node(20)
    last = Node(30)
    new = Node(40)

    llist.head.next = middle
    middle.next = last
    last.next = new

    print("The LinkedList Elements Are:")
    llist.print()

    # print(llist.head.data)
    # print(llist.head.next.data)
    # print(llist.head.next.next.data)
    # print(llist.head.next.next.next.data)
    