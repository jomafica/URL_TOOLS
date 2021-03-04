import re, time, os.path, re
import pandas as pd
from argparse import ArgumentParser, ArgumentTypeError

def path():
    direct = "\\Result"
    currentdir = os.getcwd()
    path = currentdir + direct

    try:
       os.mkdir(path)
    except FileExistsError:
        print ("Directory already exist: " + direct)
    else:
        print ("Directory created at: " + path )
    return path
def fileName():
    named_tuple = time.localtime() 
    save_path = path()
    FO_name = time.strftime("Output_%m-%d-%Y_%H-%M-%S", named_tuple)
    cname_FO = os.path.join(save_path, FO_name + ".xlsx")
    return cname_FO
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
def search_find():
    linc = []
    for l1 in ltuple2:
        for l2 in ltuple:
            regex = re.search(re.escape(l1), l2)
            if not regex:
                pass
            else:
                linc.append(l1)
    return linc
def list_diff(listInc,lsttuple2):
    listinc2 = []
    diff_list = Diff(listInc, lsttuple2)
    for i in diff_list:
        listinc2.append(i)
    return listinc2
def create_excel(MSTinv,SMLinv,inlist,ninlist,fileNa):
    writer = pd.ExcelWriter(fileNa, engine='xlsxwriter')
    #First sheet
    df = pd.DataFrame({'Master INV': MSTinv})
    df.to_excel(writer, sheet_name='Current Data', index=False)
    df = pd.DataFrame({'Small INV': SMLinv})
    df.to_excel(writer, sheet_name='Current Data', startcol=1, index=False)
    #Second sheet
    df = pd.DataFrame({'IN_LIST': inlist})
    df.to_excel(writer, sheet_name='Final results', index=False)
    df = pd.DataFrame({'NOT_IN_LIST': ninlist})
    df.to_excel(writer, sheet_name='Final results', startcol=1, index=False)
    writer.save()
    print("\nFile " + fileNa + " created")
def valid_ext(ext):
    regex = re.search(r'\.txt', ext)
    if not regex:
        raise ArgumentTypeError('mode must add the extension txt')
    return ext
def args():
    args = ArgumentParser()
    args.add_argument('MasterList', help='Name the Master file plus the extension', type=valid_ext)
    args.add_argument('SmallList', help='Name the Small file plus the extension', type=valid_ext)
    return args.parse_args()

if __name__  == "__main__":

    arugments = args()
    Mfile = arugments.MasterList
    Sfile = arugments.SmallList

    ltuple = open_Mfile(Mfile) # Change name for the Master INV
    ltuple2 = open_sfile(Sfile) # Small INV
    file_name = fileName() #Generate File name
    list_inc = search_find()
    linc2 = list_diff(list_inc,ltuple2)
    create_excel(ltuple,ltuple2,list_inc,linc2,file_name)

