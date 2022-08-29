import time,random,os

nodes=2 #change here and below
victim="SS"

#dont edit start
if True:
   start=time.time()
   if os.path.exists(os.getcwd()+r"\Wordlist"+victim):pass
   else:
      os.mkdir("Wordlist"+victim)
      for x in range(1,nodes+1):os.mkdir(os.getcwd()+r"\Wordlist"+victim+r"\node"+str(x))
   with open("parent_wordlist.txt","r") as openagain:alist2=[py.split("\n")[0] for py in openagain.readlines()]
   random.shuffle(alist2)

   all_files_seperated=[]
   attempts=len(alist2)
   attempts_pernode=int(6794000/nodes)
   files_pernode=50
   attempts_perfile=int(attempts_pernode//files_pernode)
   for obj in range(files_pernode*nodes):all_files_seperated.append(alist2[obj*attempts_perfile:(obj+1)*attempts_perfile])
   wordlist1=all_files_seperated[:files_pernode-1]
   wordlist2=all_files_seperated[files_pernode-1:]
#dont edit end



random.shuffle(wordlist1)
random.shuffle(wordlist2)

for x,y in enumerate(wordlist1):
   with open(os.getcwd()+r"\Wordlist"+victim+r"\node1\wl"+str(x+1)+".txt","w")as file:
      for r in y:file.write(r+"\n")

for x,y in enumerate(wordlist2):
   with open(os.getcwd()+r"\Wordlist"+victim+r"\node2\wl"+str(x+51)+".txt","w")as file:
      for r in y:file.write(r+"\n")

print("Taken: ",time.time()-start," seconds.")