import pickle

def loadpickle(filename):
    with open(filename, 'rb') as data:
        ret = pickle.load(data)
    return ret

def convertdata(data):
    datax = [i[0] for i in data]
    datay = [i[1] for i in data]
    return datax, datay


class NegaPosi:

    base1_data = []
    base1_label = []
    base2_data = []
    base2_label = []

    train_data = []
    train_label = []
    test_data = []
    test_label = []

    def __init__(self, filename, filename2=None):
        self.filename = filename
        bdata = loadpickle(filename)
        base1_data, base1_label = convertdata(bdata)

        if filename:
            self.filename2 = filename2
            bdata = loadpickle(filename2)
            base2_data, base2_label = convertdata(bdata)

        print(base1_data[0])
