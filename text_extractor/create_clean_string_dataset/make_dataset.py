import pickle

filename = [r'D:\Documents\Python\hex-chars\Mr.Ateru\text_extractor\text2send_%s' % num for num in range(1, 8)]
fulltext = []
for n in filename:
    with open(n, 'r', encoding='utf-8') as file:
        data = file.readlines()
        data = ''.join(data)
        data = data.split(' ')
        fulltext.append(data)
zenbu = []
for j in range(7):
    aaa = fulltext[j]
    aaa = ' '.join(aaa)
    split = [aaa[i:i+20] for i in range(0, len(aaa), 20)]
    split = [' '.join(i) for i in split]
    zenbu.extend(split)

###############
import random
def create_gomi(byte_length):
    return bytes([int(random.random()*256) for i in range(byte_length)])


zenbu = [i.encode('utf-8') for i in zenbu]
gomi_zenbu = [[create_gomi(len(i)), 0] for i in zenbu]
print(gomi_zenbu)

###############
zenbu = [[i, 1] for i in zenbu]
with open(r"D:\Documents\Python\hex-chars\Mr.Ateru\DATA4train_test\plaintxt10words.pickle", 'wb') as file:
    pickle.dump(zenbu, file)

with open(r"D:\Documents\Python\hex-chars\Mr.Ateru\DATA4train_test\plaintxt10words_gomi.pickle", 'wb') as file:
    pickle.dump(gomi_zenbu, file)