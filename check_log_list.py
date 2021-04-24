class Stack:

    def __init__(self, stack=None):
        self.stack = stack.copy() if stack else list()

    def push(self, element):
        self.stack.insert(0, element)

    def pop(self):
        value = self.stack[0]
        self.stack.remove(value)
        return value

    def peek(self):
        value = self.stack[0]
        return value

    def __len__(self):
        return len(self.stack)


def check_log_in_sequence(pattern_list, target_list):
    """
    :param pattern_list: list of elements sequence to be found in target_list
    :param target_list: target_list
    :return: True if sequence found in target_list, False otherwise
    """

    sequence_found = False
    target_list_stack = Stack(target_list)
    helper = 0
    while len(target_list_stack) >= len(pattern_list):
        if pattern_list == target_list_stack.stack[:len(pattern_list)]:
            sequence_found = True
            indexes = [helper + idx for idx in range(len(pattern_list))]
            print(f"{pattern_list} sequence found in {target_list} on indexes {indexes}")
            return sequence_found
        else:
            target_list_stack.pop()
            helper += 1
    print(f"{pattern_list} sequence NOT found in {target_list}")
    return sequence_found






