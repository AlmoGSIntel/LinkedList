from ListObject import Node
import types


class LinkedList:

    def __init__(self, *args):
        """args are object you want to add"""
        if len(args) == 1 and isinstance(args[0], types.GeneratorType):
            args = args[0]
        self.root = None
        previous_obj = None
        for enum, i in enumerate(args):
            new_object = Node(i)
            if enum == 0:
                self.root = new_object
                previous_obj = new_object
            else:
                new_object.set_previous(previous_obj)
                previous_obj.set_next(new_object)
                previous_obj = new_object

    def __iter__(self):
        """
        Default generator which returns all Values.
        """
        current_item = self.root
        while current_item is not None:  # Keeps yielding values till it gets to the end of the list.
            yield current_item.current_value
            current_item = current_item.next_obj

    def __objects(self):
        """
        Generator which returns all objects.
        """
        current_item = self.root
        while current_item is not None:  # Keeps yielding objects till it gets to the end of the list.
            yield current_item
            current_item = current_item.next_obj

    def __getitem__(self, item):  # ToDo Add Slice support.
        """ x.__getitem__(y) <==> x[y]
        Add the functionality to get an object by index: LinkedList[5].
        raise a TypeError if got something other than int.
        raise an IndexError if the index is out of range.
        """
        if not isinstance(item, int):  # Int test.
            raise TypeError(f"Needs <class 'int'> object and got {type(item)} instead.")
        if item < 0:
            for enum, i in enumerate(self.reverse()):
                if (enum + 1) == abs(item):  # Goes to the item in the index given using the generator reverse.
                    return i
            raise IndexError("list index out of range")

        for enum, i in enumerate(self):
            if enum == item:  # Goes to the item in the index given using the generator __iter__.
                return i
        raise IndexError("list index out of range")

    def __repr__(self, *args, **kwargs):
        """For end user to see it will return a nice looking list."""
        string_to_return = "LinkedList("
        for i in self.__objects():
            string_to_return = string_to_return + f" {str(i)},"

            if i.next_obj is None:  # Means its the last item.
                string_to_return = string_to_return[:-1]
                string_to_return = string_to_return.replace(" ", "", 1)

        string_to_return = string_to_return + ")"
        return string_to_return

    def __str__(self):
        """For printing in console it will return a string of the elements
         presented as a list with the [] around them with commas between them."""
        string_to_return = "["
        for i in self.__objects():
            string_to_return = string_to_return + f" {str(i)},"

            if i.next_obj is None:  # Means its the last item.
                string_to_return = string_to_return[:-1]
                string_to_return = string_to_return.replace(" ", "", 1)

        string_to_return = string_to_return + "]"
        return string_to_return

    def append(self, value):
        """Append an object to the end of the list with the given value"""
        if self.root is None:  # If the list is empty the root object is None.
            self.root = Node(value)
        else:  # List is not empty so we need to travers is to find the last object and append the new value.
            new_item = Node(value)  # Create a new object which contains the new value.
            last_item = self.last_item()  # Returns the last object of the list
            last_item.set_next(new_item)  # Append the object.
            new_item.set_previous(last_item)

    def remove(self, value):
        """
               Remove first occurrence of value.

               Raises ValueError if the value is not present.
               """
        if self.root is None:  # List is empty.
            raise ValueError("LinkedList.remove(x): x not in list")
        for i in self.__objects():
            if i.current_value == value:
                if i is self.root:
                    self.root = i.next_obj  # Replace the root object with the next in the list.
                    i.__del__()
                    self.root.set_previous(None)
                    break
                elif i is self.root and i.next_obj is None:
                    i.__del__()
                    break
                else:  # Object is not root.
                    if i.next_obj is None:  # Object is the last object.
                        i.previous_obj.set_next(None)
                        i.__del__()
                        break
                    else:  # Object is in the middle of the list.
                        i.previous_obj.set_next(i.next_obj)
                        i.next_obj.set_previous(i.previous_obj)
                        i.__del__()
                        break
        else:
            raise ValueError(f"LinkedList.remove({value}): {value} is not in the list")

    def last_item(self):
        """Returns the last item of the list."""
        current_item = self.root
        while current_item is not None:
            if current_item.next_obj is None:  # Means it is the last item cause next is None.
                return current_item
            else:  # Needs to keep going.
                current_item = current_item.next_obj

    def clear(self):
        """ Remove all items from list. """
        for i in self.__reverse_objects():
            i.__del__()  # Deleting all items and sets the root to None.
        self.root = None

    def copy(self):
        """ Return a shallow copy of the list. """
        copy_of_list = LinkedList()  # Create a new LinkList obj.
        for i in self:
            copy_of_list.append(i)  # Going trough the current LinkList object and append all objects to the new one.
        return copy_of_list

    def count(self, value, as_string=False):
        """ Return number of occurrences of value.
            as_string - If you want to count as if the objects were all as there string variation,IMPORTANT: VALUE MUST
            BE STRING. raise type error if not.
        """
        amount = 0  # Amount of time the value repeat in the list.
        for i in self:
            if as_string:  # Lets the user decide if he want to count as if the objects were strings.
                if not isinstance(value, str):  # Checks if 'value' is a string.
                    raise TypeError(f"If 'as_string' is true, 'value' must be a string: got {type(value)} instead")
                i = str(i)
            if i == value:  # Object is equals to the value the user want to count-->Adding one to "amount".
                amount += 1
        return amount

    def extend(self, iterable):
        """ Extend list by appending elements from the iterable. """
        for i in iterable:  # Going trough the iterable and appending all elements to the list.
            self.append(i)

    def index(self, value):
        """
        Return first index of value.

        Raises ValueError if the value is not present.
        """
        for enum, i in enumerate(self):  # Going trough the list to find the value given.
            if i == value:  # Found it.
                return enum  # Returning the enum value, enum value is the index.
        raise ValueError(f"'{value}' is not in the list.")

    def insert(self, value, index):
        """ Insert object at the index given. """
        if not isinstance(index, int):  # Checks if index is int.
            raise ValueError(f"Index must be <class 'int'>, and got {type(index)} instead.")
        new_item = Node(value)
        if index == 0:  # Item is root.
            new_item.set_next(self.root)
            self.root.set_previous(new_item)
            self.root = new_item
        elif index >= len(self):  # Item is the last item.
            last_item = self.last_item()
            last_item.set_next(new_item)
            new_item.set_previous(last_item)
        else:  # Item is not the first nor the last.
            for enum, i in enumerate(self.__objects()):  # Going trough the list objects.
                if enum == index:  # Got to the index given.
                    i.previous_obj.set_next(new_item)
                    i.set_previous(new_item)
                    new_item.set_previous(i.previous_obj)
                    new_item.set_next(i)
                    break

    def pop(self, index=-1):  # real signature unknown
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """

        if self.root is None:  # Checks if the list empty.
            raise IndexError("List is empty.")
        if index == -1:  # Default option, the last object --> pops the last item.
            for i in self.__objects():
                if i.next_obj is None:  # Means its the last object.
                    item_to_return = i.current_value
                    i.previous_obj.set_next(None)
                    i.__del__()
                    return item_to_return

        elif index == 0:  # User asked for the first object--> pops the first item.
            for i in self.__objects():  # Using a loop so I could change the 'i' object.
                if i is self.root:  # Item in index is root --> root is the first item.
                    item_to_return = self.root.current_value
                    i.next_obj.set_previous(None)
                    self.root = i.next_obj
                    i.__del__()
                    return item_to_return

        else:  # User asked for an index which is not the last nor the first item.
            for enum, i in enumerate(self.__objects()):
                if enum == index:  # Find the index.
                    item_to_return = i.current_value
                    i.previous_obj.set_next(i.next_obj)
                    i.next_obj.set_previous(i.previous_obj)
                    i.__del__()
                    return item_to_return
            else:  # Went trough all the list and didn't find the index.
                raise IndexError("Index out of range.")

    def reverse(self):
        """ Returns a generator of the values from the last to the start """
        current_item = self.last_item()
        while current_item is not None:
            yield current_item.current_value
            current_item = current_item.previous_obj

    def __reverse_objects(self):
        """ Returns a generator of the objects from the last to the start """
        current_item = self.last_item()
        while current_item is not None:
            yield current_item
            current_item = current_item.previous_obj

    def sort(self, key=None, reverse=False):  # ToDo add .sort support.
        """ Uses the sort_func to sort the list."""
        sorted_list = list(item for item in self)
        sorted_list.sort(key=key, reverse=reverse)
        # sorted_link_list = LinkedList(node for node in sorted_list)
        self.clear()
        self.extend(sorted_list)

    def __setitem__(self, key, value):
        """ Set self[key] to value. """
        for enum, i in enumerate(self.__objects()):  # Going trough the list.
            if enum == key:  # Got to the given index.
                i.current_value = value  # Changed the object value.
                break
        else:  # Iterate trough the list and didn't find the index.
            raise IndexError(f"Index '{key}' is out of range.")

    def __len__(self, *args, **kwargs):
        """ Return len(self). """
        length = 0
        for i in self:
            length += 1
        return length

    def __contains__(self, value):
        """ Return key in self. """
        for i in self:  # Iterate the list.
            if value == i:  # Found it.
                return True
        else:  # Didn't find it.
            return False

    def __delitem__(self, key):
        """ Delete self[key]. """
        for enum, i in enumerate(self.__objects()):  # Iterate the list.
            if enum == key:  # Found the index.
                if i is self.root:  # Item the the first item --> self.root
                    i.next_obj.set_previous(None)
                    self.root = i.next_obj
                    i.__del__()
                    break
                elif i.next_obj is None:  # Item is the last item.
                    i.previous_obj.set_next(None)
                    i.set_previous(None)
                    i.__del__()
                    break
                else:  # Item is not the first nor the last.
                    i.previous_obj.set_next(i.next_obj)
                    i.next_obj.set_previous(i.previous_obj)
                    i.set_previous(None)
                    i.__del__()
                    break
        else:  # Iterate trough the list and didn't find the index.
            print(len(self))
            raise IndexError(f"Index '{key}' out of range.")

    def __eq__(self, other, cross_list=False):
        """ Return self==value. """
        for enum, i in enumerate(self):
            try:
                if i != other[enum]:
                    return False
            except IndexError:
                return False
        else:
            return True

    def __ne__(self, other):  # real signature unknown
        """ Return self!=value. """
        if self == other:
            return False
        else:
            return True
