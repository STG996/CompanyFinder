STACK_LENGTH = 50

class Stack:
    def __init__(self):
        self.__array = ["" for _ in range(STACK_LENGTH)]
        self.__pointer = 0

    def push(self, item):
        self.__pointer += 1
        try:
            self.__array[self.__pointer] = item
        except IndexError:
            print("Stack length exceeded.")

    def peek(self):
        return self.__array[self.__pointer]

    def pop(self):
        item = self.peek()
        self.__array[self.__pointer] = ""
        self.__pointer -= 1
        return item

    def clear(self):
        self.__init__()