import pcap_parser.pcap2byted as parse
from packet_classifier.stringClassifier import Classifier

filename = "./packet_classifier/seccup_exp.csv"

# cls = Classifier(filename)
# cls.allprocess()

pcappath = "./pcap_parser/sample.pcap"
data = parse.pcap2byte(pcappath)
print(data[0])
cls2 = Classifier(data)
cls2.allprocess()
