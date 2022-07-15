class Obj(object):
    def __init__(self, data):
        data = data
        for tag in data:
            for atr in data[tag]:
                if atr == 'health':
                    setattr(self, 'max_health', data[tag][atr])
                setattr(self, atr, data[tag][atr])

class Room(object):
    def __init__(self, data):
        for tag in data:
            setattr(self, tag, data[tag])
