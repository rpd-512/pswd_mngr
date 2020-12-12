import os
import sqlite3
import hidepass
import hashlib
import string
import random
from texttable import Texttable
from pyperclip import copy
from time import sleep

def startup():
    global dbPath, clrScr, acc_pswd
    if(os.name == "nt"):
        clrScr = "cls"
        dbPath = ""
    else:
        clrScr = "clear"
        dbPath = os.path.expanduser("~")+"/.pswd_mngr/"
    if(os.path.exists(dbPath+".pswds.db")):
        conn = sqlite3.connect(dbPath+".pswds.db")
        datab = conn.execute('select * from app_det;')
        for i in datab:
            acc_pswd=i[0]
        while(True):
            try:
                pswd = hidepass.getpass(prompt="Enter master password: ")
            except (KeyboardInterrupt):
                print("\n!!Cancelled!!")
                sleep(3)
                exit()
            hash_pswd = (hashlib.md5((pswd+"314159265358979323846264338327").encode())).hexdigest()
            if(hash_pswd != acc_pswd):
                print("!! Wrong password !!")
                sleep(3)
                exit()
            else:
                os.system(clrScr)
                print("Type \"\\h\" for help, \"\\a\" for about")
                break
    else:
        print("\nWelcome to your very own password manager!!")
        while(True):
            try:
                mst_pswd = hidepass.getpass(prompt="Please create your master password  : ")
                rem_pswd = hidepass.getpass(prompt="Please re-enter your master password: ")
            except(KeyboardInterrupt):
                print("\n!!Cancelled!!")
                sleep(3)
                exit()
            if(mst_pswd == rem_pswd):
                os.mkdir(dbPath)
                conn = sqlite3.connect(dbPath+".pswds.db")
                conn.execute("create table app_det (pswd text);")
                conn.execute("""create table pwd_det (
                    siteId integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    site text,
                    mail text,
                    uname text,
                    pswd text
                    );""")
                hash_pswd = (hashlib.md5((mst_pswd+"314159265358979323846264338327").encode())).hexdigest()
                execdb = "insert into app_det (pswd) values ('"+hash_pswd+"');"
                conn.execute(execdb)
                conn.commit()
                conn.close()
                print("Congrats!! Master Password is set! Lets Get started!")
                sleep(3)
                os.system(clrScr)
                startup()
                break
            else:
                print("!Password Mismatch!\n\n")
def cmp():
    print("Changing master password. Press ctrl+c to cancel")
    global conn, acc_pswd
    try:
        pswd = hidepass.getpass(prompt="Enter current master password: ")
    except (KeyboardInterrupt):
        print("\n!!Cancelled!!")
        return 0
    hash_pswd = (hashlib.md5((pswd+"314159265358979323846264338327").encode())).hexdigest()
    if(hash_pswd != acc_pswd):
        print("!! Wrong password !!")
        pass
    else:
        while(True):
            try:
                mst_pswd = hidepass.getpass(prompt="\nEnter new master password   : ")
                rem_pswd = hidepass.getpass(prompt="re-enter new master password: ")
            except (KeyboardInterrupt):
                print("\n!!Cancelled!!")
                return 0
            if(mst_pswd == rem_pswd):
                hash_pswd = (hashlib.md5((mst_pswd+"314159265358979323846264338327").encode())).hexdigest()
                conn.execute("update app_det set pswd = '"+hash_pswd+"'")
                conn.commit()
                print("\nMaster password updated\n")
                startup()
                break
            else:
                print("!Password Mismatch!\n\n")
def genrand():
    rawData = string.ascii_letters + string.digits + string.punctuation
    rand_pswd = ''.join(random.choice(rawData) for i in range(20))
    return rand_pswd

def encr(txt):
    if(txt.replace(" ","") == ""):
        return txt
    try:
        txt = txt[::-1]
        enc_txt = ""
        for i in txt:
            enc_txt += chr(ord(i)+5)
        enc_txt = enc_txt.encode().hex()
        return enc_txt
    except:
        return txt

def decr(txt):
    if(txt.replace(" ","") == ""):
        return txt
    try:
        txt = bytes.fromhex(txt).decode('utf-8')
        txt = txt[::-1]
        dec_txt = ""
        for i in txt:
            dec_txt += chr(ord(i)-5)
        return dec_txt
    except:
        return txt
def see(site,data):
    global conn
    site = site.replace(" ","").lower()
    if (len(site) == 0 and data != "all"):
        print("\nMissing operand!! use help for better understanding of the command")
        return 0
    else:
        if(data == "all"):
            print("\nShowing all results")
            cursor = conn.execute("select * from pwd_det")
        elif(data == "site"):
            print("\nSearching for data containing site name: '"+site+"'")
            cursor = conn.execute("select * from pwd_det where site like '%"+site+"%'")
        elif(data == "mail"):
            print("\nSearching for data containing email address: '"+site+"'")
            cursor = conn.execute("select * from pwd_det where mail like '%"+site+"%'")
        elif(data == "name"):
            print("\nSearching for data containing user name: '"+site+"'")
            cursor = conn.execute("select * from pwd_det where uname like '%"+site+"%'")
        elif(data == "enid"):
            print("\nSearching for data containing Entry ID: '"+site+"'")
            cursor = conn.execute("select * from pwd_det where siteId like '%"+site+"%'")
        t = Texttable()
        t.set_cols_align(['c','c','c','c','c'])
        data_ret = [['','','','','']]
        ntfnd = False
        for i in cursor:
            ntfnd = True
            dec_pswd = decr(i[4])
            data_ret.append([i[0], i[1], i[2], i[3],dec_pswd])
        if(ntfnd == True):
            t.add_rows(data_ret)
            t.header(['Entry ID', 'Site/App name', 'Mail ID' , 'Username', 'Password'])
            print(t.draw())
        else:
            print("\nNot Found")
def ent():
    global conn
    try:
        print("\nCreate new entry. (press ctrl+c to cancel, leave blank if something is not applicable)\n")
        def_pass = genrand()
        stnm = str(input("Enter site/app name : "))
        mlid = str(input("Enter mail id used  : "))
        usnm = str(input("Enter user name used: "))
        pswd = hidepass.getpass(prompt="Enter/Create your password  (suggested: '"+def_pass+"', leave blank to use suggetion) : ")
        if(pswd.replace(" ","") == ""):
            pswd = def_pass
        elif(stnm.replace(" ","") == ""):
            stnm = " "
        elif(mlid.replace(" ","") == ""):
            mlid = " "
        elif(usnm.replace(" ","") == ""):
            usnm = " "
        pswd = str(encr(pswd))
        conn.execute("INSERT INTO pwd_det (site,mail,uname,pswd) VALUES ('"+stnm+"','"+mlid+"','"+usnm+"','"+pswd+"')")
        conn.commit()
        pswd = decr(pswd)
        t = Texttable()
        t.set_cols_align(['c','c','c','c'])
        print("\nData created \n")
        t.add_rows([['Site/App name', 'Mail ID' , 'Username', 'Password'],[stnm,mlid,usnm,pswd]])
        print(t.draw())
    except (KeyboardInterrupt):
        print("\n!!Cancelled!!\n")
def dlt(txt):
    global conn, acc_pswd
    avlb = False
    try:
        id = int(txt[4:len(txt)])
    except:
        print("Missing or Invalid operand")
        return 0
    id = str(id)
    cur = conn.execute("select * from pwd_det where siteId = "+id+";")
    for i in cur:
        avlb = True
        stid,stnm,mlid,usnm,pswd = i[0],i[1],i[2],i[3],decr(i[4])
    if(avlb == False):
        print("No data found regarding Entry ID "+id+". Try using see command to check for available Entry ID's.")
        return 0
    print("Are you sure you want to delete this?")
    t = Texttable()
    t.set_cols_align(['c','c','c','c','c'])
    t.add_rows([['Site ID','Site/App name', 'Mail ID' , 'Username', 'Password'],[stid,stnm,mlid,usnm,pswd]])
    print(t.draw())
    try:
        mst_pswd = hidepass.getpass(prompt="Type master password for confirmation (press ctrl-c to cancel): ")
    except(KeyboardInterrupt):
        print("\n!!Cancelled!!")
        return 0
    hash_pswd = (hashlib.md5((mst_pswd+"314159265358979323846264338327").encode())).hexdigest()
    if(hash_pswd != acc_pswd):
        print("!! Wrong password !!")
        return 0
    conn.execute("delete from pwd_det where siteId = "+id)
    conn.commit()
    print("\nData Deleted")
def updt(txt):
    global conn, acc_pswd
    avlb = False
    try:
        id = int(txt[5:len(txt)])
    except:
        print("Missing or Invalid operand")
        return 0
    id = str(id)
    cur = conn.execute("select * from pwd_det where siteId = "+id+";")
    for i in cur:
        avlb = True
        stid,stnm,mlid,usnm,pswd = i[0],i[1],i[2],i[3],decr(i[4])
    if(avlb == False):
        print("No data found regarding Entry ID "+id+". Try using see command to check for available Entry ID's.")
        return 0
    print("Updating the following data (Press ctrl-c to cancel, leave blank for making no changes, if data is actually blank, press spacebar and then enter):")
    t = Texttable()
    t.set_cols_align(['c','c','c','c','c'])
    t.add_rows([['Site ID','Site/App name', 'Mail ID' , 'Username', 'Password'],[stid,stnm,mlid,usnm,pswd]])
    print(t.draw())
    try:
        updt_stnm = str(input("Update site name (currently: '"+stnm+"'): "))
        updt_mlid = str(input("Update mail id   (currently: '"+mlid+"'): "))
        updt_usnm = str(input("Update user name (currently: '"+usnm+"'): "))
        updt_pswd = str(input("Update password  (currently: '"+pswd+"'): "))
    except (KeyboardInterrupt):
        print("\n!!Cancelled!!")
        return 0
    if(updt_stnm == ""):
        updt_stnm = stnm
    if(updt_mlid == ""):
        updt_mlid = mlid
    if(updt_usnm == ""):
        updt_usnm = usnm
    if(updt_pswd == ""):
        updt_pswd = pswd
    
    conn.execute("update pwd_det set site='"+updt_stnm+"',mail='"+updt_mlid+"',uname='"+updt_usnm+"',pswd='"+encr(updt_pswd)+"' where siteId = "+id)
    conn.commit()
    print("\nData updated")
def cpy(txt):
    global conn
    avlb = False
    tocopy = (txt[5:9])
    crct = ['site','name','mail','pswd']
    if(len(tocopy) == 0 or tocopy not in crct):
        print("Missing or Invalid operand.")
        return 0
    try:
        id = str(int(txt[9:len(txt)]))
    except:
        print("Entry ID should be a number only")
        return 0
    cur = conn.execute("select * from pwd_det where siteId = "+id)
    for i in cur:
        avlb = True 
        stnm,mlid,usnm,pswd = i[1],i[2],i[3],decr(i[4])
    if(avlb):
        if(tocopy == 'site'):
            cp = stnm
        elif(tocopy == 'mail'):
            cp = mlid
        elif(tocopy == 'name'):
            cp = usnm
        elif(tocopy == 'pswd'):
            cp = pswd
        copy(cp)
        print(tocopy+" copied to clip board")
    else:
        print("No data found regarding Entry ID "+id+". Try using see command to check for available Entry ID's.")
def reset():
    global acc_pswd, dbPath
    print("WARNING!! YOU WON'T BE ABLE TO RECOVER ANY PASSWORD AFTER YOU RESET!!")
    try:
        mst_pswd = hidepass.getpass(prompt="Type master password for confirmation (press ctrl-c to cancel): ")
    except(KeyboardInterrupt):
        print("\n!!Cancelled!!")
        return 0
    hash_pswd = (hashlib.md5((mst_pswd+"314159265358979323846264338327").encode())).hexdigest()
    if(hash_pswd != acc_pswd):
        print("!! Wrong password !!")
        return 0
    os.remove(dbPath+'.pswds.db')
    print("!!DELETED!!")
    sleep(3)
    os.system("clear")
    exit()
startup()
try:
    conn.close()
except:
    pass
conn = sqlite3.connect(dbPath+".pswds.db")
while(True):
    try:
        inp = input("password_manager:~$ ").lower()
        if(inp == "\\h" or "help" in inp):
            print("""\n|HELP|
            -> cmp   - change master password
            -> grp   - generate a random password
            -> clear - clear screen
            -> exit  - exit the program
            -> ent   - new entry
            -> see   - shows all details related to provided data. try the following:
                        (O) see site <site url or app name>
                        (O) see mail <mail id>
                        (O) see name <username>
                        (O) see enid <entry id>
                        (O) see all
            -> dlt   - delete an entry. use it as follows:
                        (O) dlt <entry id>
                       get entry id via `see` command
            -> updt  - updates an entry. use it as follows:
                        (O) updt <entry id>
                       get entry id via `see` command
            -> copy  - copies related data according to Entry ID. try the following:
                        (O) copy site <entry id>
                        (O) copy mail <entry id>
                        (O) copy name <entry id>
                        (O) copy pswd <entry id>
                       get entry id via `see` command
            -> reset - deletes all the data and resets everything.
            -> \\h    - help
            -> \\a    - about\n""")
        elif(inp == "\\a"):
            print("""\n|ABOUT|
            This is a CLI, python based password manager created by Rhiddhi Prasad Das.
            Github : https://github.com/rpd-512/
            Twitter: https://twitter.com/RhiddhiD
            Fiverr : https://www.fiverr.com/rpd_512
            Email  : rhiddhiprasad@gmail.com
            """)
        elif(inp == "cmp"):
            cmp()
        elif(inp == "clear"):
            os.system(clrScr)
        elif(inp == "grp"):
            rand_pswd = genrand()
            print("\nPassword generated: "+rand_pswd)
            try:
                ques = input("Copy the genterated password (Y\\N)? ")
            except (KeyboardInterrupt):
                ques = "n"
            if(ques.lower() == "y"):
                copy(rand_pswd)
                print("Password Copied to clipboard")
            else:
                print("\nNot copied")
        elif(inp[0:3] == "see"):
            if(inp[4:8] == "site"):
                site = (inp[9:len(inp)])
                see(site,"site")
            elif(inp[4:8] == "mail"):
                site = (inp[9:len(inp)])
                see(site,"mail")
            elif(inp[4:8] == "name"):
                site = (inp[9:len(inp)])
                see(site,"name")
            elif(inp[4:8] == "enid"):
                try:
                    site = str(int(inp[9:len(inp)]))
                    see(site,"enid")
                except:
                    print("Entry ID should be a number")
            elif(inp[4:8] == "all"):
                see("","all")
            else:
                print("Missing or Invalid operand")
        elif(inp == "ent"):
            ent()
        elif(inp[0:3] == "dlt"):
            dlt(inp)
        elif(inp[0:4] == "updt"):
            updt(inp)
        elif(inp[0:4] == "copy"):
            cpy(inp)
        elif(inp == "reset"):
            reset()
        elif(inp == "exit"):
            print("Bye !!")
            sleep(3)
            exit()
        elif(inp.replace(" ","") == ""):
            pass
        else:
            print("Invalid input")
    except (KeyboardInterrupt):
        print("\nBye !!")
        sleep(3)
        exit()
##----------------------------------------------EOF-----------------------------------------------##
