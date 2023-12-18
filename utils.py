class DictToObj:
    def __init__(self, dictionary):
        # Loop through dictionary items and set attributes
        for key, value in dictionary.items():
            setattr(self, key, value)

    def __repr__(self):
        # Define how the object is represented in string format
        return f'<DictToObj {self.__dict__}>'
