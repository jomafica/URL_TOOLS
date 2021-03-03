
import re, time, os.path, re

def path():
    direct = "\\Result"
    currentdir = os.getcwd()
    path = currentdir + direct

    try:
       os.mkdir(path)
    except FileExistsError:
        print ("Directory already exist")
    else:
        print ("Directory created" )
    return path

# Define local path and file name
named_tuple = time.localtime() 
save_path = path()
FO_name = time.strftime("IN_%m-%d-%Y_%H-%M-%S", named_tuple)
FO2_name = time.strftime("NOT_IN_%m-%d-%Y_%H-%M-%S", named_tuple)
cname_FO = os.path.join(save_path, FO_name+".txt")
cname_FO2 = os.path.join(save_path, FO2_name+".txt")

# Create output
FO = open(cname_FO, 'w+')
FO2 = open(cname_FO2, 'w+')

def open_Mfile(file_name):
    list_tuple = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            list_tuple.append(line.strip())
    return list_tuple
def open_sfile(file_name):
    list_tuple1 = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            list_tuple1.append(line.strip())
    return list_tuple1
def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

if __name__== "__main__":

    ltuple = open_Mfile("ipSN.txt") # Change name for the Master INV
    ltuple2 = open_sfile("ip.txt") # Small INV
    linc = []

    for l1 in ltuple2:
        for l2 in ltuple:
            regex = re.search(re.escape(l1), l2)
            if not regex:
                pass
            else:
                linc.append(l1)
                FO.write("%s\n" %(l2))

    diff_list = Diff(linc, ltuple2)
    for i in diff_list:
        FO2.write("%s\n" %(i.strip()))

    FO.close()
    FO2.close()

