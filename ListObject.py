
class Node:
    def __init__(self, current_value):
        self.current_value = current_value
        self.next_obj = None
        self.previous_obj = None

    def __str__(self):
        if isinstance(self.current_value, str):
            return f"'{self.current_value}'"
        else:
            return str(self.current_value)

    def set_next(self, node_obj):
        self.next_obj = node_obj

    def set_previous(self, node_obj):
        self.previous_obj = node_obj

    def get_current_value(self):
        return self.current_value

    def remove_next(self):
        self.next_obj = None

    def remove_previous(self):
        self.previous_obj = None

    def __del__(self):
        self.set_next(None)
        self.current_value = None
        del self
