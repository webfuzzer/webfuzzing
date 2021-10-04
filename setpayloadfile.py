from glob import glob

DICTLIST = glob(".\\src\\payloads\\*")
for FILE in DICTLIST:
    PAYLOADSLILELIST = glob(f"{FILE}\\*")
    tmppay = set()
    for read in PAYLOADSLILELIST:
        with open(read, 'r', encoding='UTF-8') as fr:
            for pay in fr.readlines():
                tmppay.add(pay)
    with open(f'{FILE}\\payloads.txt', 'w+', encoding='UTF-8') as fw:
        fw.writelines(tmppay)