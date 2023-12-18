
class EncodedItem:
    """
    Class representing an Encoded Item. DTO with an as_dict method for dictionary representation.
    """
    def __init__(self, word: str, parent: str, values: list[str]):
        """
        Initialize the encoded item.
        :param word: Encoded word.
        :param parent: Parent for grouping.
        :param value: Decoded graphing parameter.
        """
        self.word: str = word
        self.parent: str = parent
        self.values: list[str] = values

    def as_dict(self) -> dict:
        return {'word':self.word, 'parent':self.parent, 'values':self.values}


class ValueDictionary:
    """
    Class representing the value dictionary. Contains a list of Encoded Items and methods for working with them.
    """
    def __init__(self, filename=None):
        """
        Initializes the Value Dictionary with an empty Encoded Item list
        """
        self.items: list[EncodedItem] = []
        if filename is not None:
            self.load_from_json(filename)

    def add_item(self, new_value: EncodedItem) -> None:
        """
        Adds the Encoded Item to the dictionary
        :param new_value: Encoded Item to add
        """
        self.items.append(new_value)

    # def add_word(self, word: str, parent: str, value: list[str]) -> None:
    #     """
    #     Adds the Encoded Item to the dictionary
    #     :param word: Word of item
    #     :param parent: Parent of item
    #     :param value: Value of item
    #     """
    #     self.items.append(EncodedItem(word, parent, value))
        
    def search_matches(self, problem_statement: str) -> list[str]:
        """Find all matches for the given problem statement

        Args:
            problem_statement (str): Given problem statement

        Returns:
            list[str]: List of words found in the value base
        """
        cleaned_statement = ""
        for letter in problem_statement:
            if letter.isalpha() or letter.isspace():
                cleaned_statement += letter
            
        words = cleaned_statement.split()
        return [word for word in words if word.lower() in self]
    
    def match_parents(self, items: list[str]) -> list[str]:
        return_list = []
        for item in items:
            parent = self[item].parent
            if parent != '' and parent not in return_list:
                return_list.append(parent)
            elif parent == '':
                return_list.append(item)
        return return_list

    def clear(self) -> None:
        """
        Clears the dictionary
        """
        self.items = []

    # def add_all(self, new_values: list[EncodedItem]) -> None:
    #     """
    #     Adds all Encoded Items in the given list to the dictionary
    #     :param new_values: Encoded Items list
    #     """
    #     self.items += new_values
        
    def decode(self, word: str) -> tuple[str]:
        if word in self:
            return tuple(self[word].values)
        return None
    
    def __getitem__(self, word:str) -> EncodedItem:
        """
        Returns the first item found
        :param item: Search parameter (word)
        :return: Returns the first item found
        """
        for item in self.items:
            if word.lower() == item.word.lower():
                return item
        return None
    
    def __contains__(self, key: str):
        return key.lower() in [item.word.lower() for item in self.items]

    def get_all(self) -> list[dict]:
        """
        Gets all items from the dictionary as a list of dictionary items.
        :return:
        """
        return [i.as_dict() for i in self.items]

    def load_from_csv(self, filename) -> None:
        """
        Reads the given csv file, assumes that the file will be in the following format:

        [Word], [Parent], [Value]
        :param filename: File to read from
        """
        import csv
        with open(filename) as file:
            reader = csv.reader(file)
            for line in reader:
                self.add_item(EncodedItem(line[0], line[1], line[2]))

    def write_to_csv(self, filename):
        """
        Writes all the items in the current dictionary to a given file in CSV format
        :param filename: File to write to
        """
        import csv
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            for item in self.items:
                writer.writerow([item.word, item.parent, str(item.values)])

    def load_from_json(self, filename: str):
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
                self.add_item(EncodedItem(item['word'], item['parent'], item['value']))

    def write_to_json(self, filename: str):
        """
        Writes all the items in the current dictionary to a given file in JSON format
        :param filename: File to write to
        """
        import json
        with open(filename) as file:
            json.dump(self.get_all(), file)


class KnowledgeItem:
    """
    Class representing an Knowledge Item. DTO with an as_dict method for dictionary representation.
    """
    def __init__(self, params: list[str], graphs: list[str]):
        self.params: tuple[str] = tuple(params)
        self.graphs: tuple[str] = tuple(graphs)
        
    def as_dict(self) -> dict:
        return {self.params:self.graphs}
    
    def as_pair(self) -> tuple(tuple[str]):
        return (self.params, self.graphs)


class KnowledgeBase:
    def __init__(self, filename:str=None):
        self.items: list[KnowledgeItem] = []
        if filename is not None:
            self.load_from_json(filename)

    def load_from_json(self, filename:str) -> None:
        import json
        with open(filename) as file:
            json = json.load(file)
            for item in json:
                self.add_item(params=item['params'], graphs=item['graphs'])
                
    def add_item(self, params: list[str], graphs: list[str]) -> None:
        self.items.append(KnowledgeItem(params, graphs))

    
    def lower_list(self, ls:list[str]) -> list[str]:
        return [item.lower() for item in ls]
    
    def get_all_dict(self) -> dict:        
        return {k:v for k, v in [i.as_pair() for i in self.items]}
    
    def combinate(self, tupes: list[tuple]) -> list[tuple[str]]:
        from itertools import product
        
        axes = [list(tupe) for tupe in tupes]
        for axis in axes:
            axis.append('')
        return list(product(*axes))
        

    def recommend(self, vd:ValueDictionary, items:list[str]):
        from itertools import permutations
        
        axes = vd.match_parents(items)
        
        decoded = [vd.decode(axis) for axis in axes]
        
        combs = self.combinate(decoded)
        
        # perms = list(permutations(combs))
        perms = []
        for comb in combs:
            perms += [perm for perm in permutations(comb)]
        
        filtered = []
        for perm in perms:
            filtered.append(tuple(filter(lambda perm: perm != '', perm)))

        filtered = list(set(filtered))
        
        knowledge = self.get_all_dict()

        recommend = [knowledge[perm] for perm in filtered if perm in knowledge]
        return recommend


