import dpkt
import pickle


def pcap2byte(pcap_path):
    """
    :param pcap_path: リストデータに変換したいpcapファイルのパスを入れる
    :return: 全てのパケットに対して、[[bytedata1, 1], [bytedata2, 1]... ... ... ]のようなものを返す。
    """
    #リターンするリストの初期化
    packet_data_list = []
    with open(pcap_path, 'rb') as pcap_file:
        pcr = dpkt.pcap.Reader(pcap_file)
        """
        本来は下記の様にリスト内方表記でやりたいが、
        Ethernetクラスにできないものもあるようなので、
        普通にfor文とappendで作る
        # packet_data_list = [[dpkt.ethernet.Ethernet(buf).data.data.data, 1] for buf in pcr]
        """
        for ts, buf in pcr:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
            except:
                continue
            """
            こういう感じで下の階層のデータに潜っていく
            """
            ip = eth.data
            tcp = ip.data
            try:
                data = tcp.data
            except AttributeError:
                continue
            """
            ここでいったんデータ長が0じゃないか確認、0だったら弾く
            """
            if len(data) == 0:
                continue
            """
            欲しいやつを追加する。
            """
            packet_data_list.append([data, 1])
    return packet_data_list
#
# path = "D:\Documents\Python\hex-chars\Mr.Ateru\pcap_parser\capture_good_packets.pcap"
#
# a = pcap2byte(path)
# with open("labled_good_data.pickle", 'wb') as file:
#     pickle.dump(a, file)
