STACK_LENGTH = 50

class Stack:
    def __init__(self):
        self.__array = [None for _ in range(STACK_LENGTH)]
        self.__pointer = -1

    def push(self, item):
        self.__pointer += 1
        try:
            self.__array[self.__pointer] = item
        except IndexError:
            print("Stack length exceeded.")
            self.__pointer -= 1 # ask ms elina what the correct procedure is

    def peek(self):
        return self.__array[self.__pointer]

    def pop(self):
        item = self.peek()
        self.__array[self.__pointer] = None
        self.__pointer -= 1
        return item

    def clear(self):
        self.__init__()