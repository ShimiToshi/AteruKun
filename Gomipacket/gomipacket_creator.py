import random
import pickle

def create_gomi(byte_length):
    return bytes([int(random.random()*256) for i in range(byte_length)])


with open("D:\Documents\Python\hex-chars\Mr.Ateru\pcap_parser\labled_good_data.pickle", 'rb') as file:
    data = pickle.load(file)


gomi_data_list = [[create_gomi(len(i[0])), 0] for i in data]
with open(r"D:\Documents\Python\hex-chars\Mr.Ateru\pcap_parser\labled_bad_data.pickle", 'wb') as file:
    pickle.dump(gomi_data_list, file)
print(gomi_data_list)