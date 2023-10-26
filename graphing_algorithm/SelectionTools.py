class KnowledgeItem:
    def __init__(self, params: list[str], graphs: list[str]):
        self.params: list[str] = params
        self.graphs: list[str] = graphs


class KnowledgeBase:
    def __init__(self):
        self.items: list[KnowledgeItem] = []

    # def as_dict(self) -> dict:
    #     return {}
    #


class EncodedItem:
    """
    Class representing an Encoded Item. DTO with an as_dict method for dictionary representation.
    """
    def __init__(self, word: str, parent: str, value: str):
        """
        Initialize the encoded item.
        :param word: Encoded word.
        :param parent: Parent for grouping.
        :param value: Decoded graphing parameter.
        """
        self.word = word
        self.parent = parent
        self.value = value

    def as_dict(self) -> dict:
        return {k: v for (k, v) in zip(['word', 'parent', 'value'], self.word, self.parent, self.value)}


class ValueDictionary:
    """
    Class representing the value dictionary. Contains a list of Encoded Items and methods for working with them.
    """
    def __init__(self):
        """
        Initializes the Value Dictionary with an empty Encoded Item list
        """
        self.items: list[EncodedItem] = []

    def add_item(self, new_value: EncodedItem) -> None:
        """
        Adds the Encoded Item to the dictionary
        :param new_value: Encoded Item to add
        """
        self.items += new_value

    def add_word(self, word: str, parent: str, value: str) -> None:
        """
        Adds the Encoded Item to the dictionary
        :param word: Word of item
        :param parent: Parent of item
        :param value: Value of item
        """
        self.items += EncodedItem(word, parent, value)

    def clear(self) -> None:
        """
        Clears the dictionary
        """
        self.items = []

    def add_all(self, new_values: list[EncodedItem]) -> None:
        """
        Adds all Encoded Items in the given list to the dictionary
        :param new_values: Encoded Items list
        """
        self.items += new_values

    def __getitem__(self, item: str):
        """
        Returns a list of each item
        :param item: Search parameter (word)
        :return: Returns a list of matching Encoded Items as dictionaries
        """
        return [x.as_dict() for x in self.items if x.word.lower() == item.lower()]

    def get_all(self) -> list[dict]:
        """
        Gets all items from the dictionary as a list of dictionary items.
        :return:
        """
        return [i.as_dict() for i in self.items]

    def add_from_csv(self, filename) -> None:
        """
        Reads the given csv file, assumes that the file will be in the following format:

        [Word], [Parent], [Value]
        :param filename: File to read from
        """
        import csv
        with open(filename) as file:
            reader = csv.reader(file)
            for line in reader:
                self.add_word(line[0], line[1], line[2])

    def write_to_csv(self, filename):
        """
        Writes all the items in the current dictionary to a given file in CSV format
        :param filename: File to write to
        """
        import csv
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            for item in self.items:
                writer.writerow([item.word, item.parent, item.value])

    def add_from_json(self, filename: str):
        """
        Reads the given json file, assumes that the file will be in the following format:

        [{'word': [Word],

        'parent': [Parent],

        'value': [Value], ...}]
        :param filename: File to read from
        """
        import json
        with open(filename) as file:
            json = json.load(file)
            for item in json:
                self.add_word(item['word'], item['parent'], item['value'])

    def write_to_json(self, filename: str):
        """
        Writes all the items in the current dictionary to a given file in JSON format
        :param filename: File to write to
        """
        import json
        with open(filename) as file:
            json.dump(self.get_all(), file)

