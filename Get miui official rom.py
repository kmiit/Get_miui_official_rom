import requests, re, os
try:
 from tqdm import tqdm
except:
 os.system("pip install tqdm")

def GET_PHONE_LIST():
 print("If it appears \"list index out of range\", please try again")
 MAIN = "https://hub.fastgit.org/mooseIre/update_miui_ota/blob/master/README.md"
 print("\nGetting supported phone list...\n")
 a = requests.get(MAIN)
 b = re.findall(r"<tbody>(.+?)</tbody>", a.text, re.S)
 d = re.findall(r"<td align=\"center\">(.+?)</td>", b[0], re.S)
 model = []
 develop = []
 stable = []
 for l in range(0, len(d), 3):
  model.append(d[l])
 for l in range(1, len(d), 3):
  develop.append(d[l])
 for l in range(2, len(d), 3):
  stable.append(d[l])
 dd = []
 ss = []
 for l in range(len(develop)):
  tempd = re.findall(r"<a href=\"(.+?)\">Develop</a>", develop[l], re.S)
  dd.append(tempd[0])
 for l in range(len(stable)):
  temps = re.findall(r"<a href=\"(.+?)\">Stable</a>", stable[l], re.S)
  ss.append(temps[0])
 return model, dd, ss
 
def GET_ROM_LIST(LIST):
 for l in range(len(LIST[0])):
  print(l, LIST[0][l])
 a = int(input("\nPlease choose your phone: "))
 print("You choosed: ", LIST[0][a])
 b = int(input ("\nPlease input the kind you need(1.Develop, 2.Stable) : "))
 print("You choosed: ", LIST[0][a], "Stable" if b == 2 else "Develop")
 print("Getting rom list...\n")
 c = requests.get(LIST[b][a])
 d = re.findall(r"rel=\"nofollow\">(.+?)</a>", c.text, re.S)
 dd = re.findall(r"<td><a href=\"(.+?)\" rel=\"nofollow\">", c.text, re.S)
 for l in range(len(d)):
  print(l, d[l])
 e = int(input("Please choose the version you want to download(0 is the latest version): "))
 print("Prepare to download ", d[e])
 print("The address is:\n", dd[e])
 a = input("Enter to download in this program(File will be saved in the same path as this python file),and any key to quit")
 return 1-bool(a), d[e], dd[e]
  
def DOWNLOAD(FILENAME, ADDRESS):
 FILE = requests.get(ADDRESS,stream = True)
 content_size = int(FILE.headers['Content-Length']) / 1024 
 if os.name == "nt" :
  path = os.getcwd()+ "\\" + FILENAME
 else:
  path = os.getcwd()+ "/" + FILENAME
 print("File path:  ",path)
 with open(path, "wb") as file:
  print("File total size is:  ", content_size, "Mb")
  for data in tqdm(iterable = FILE.iter_content(1024), total = content_size, unit = 'k', desc = FILENAME):
   file.write(data)


def main():
 LIST = GET_PHONE_LIST()
 JD = GET_ROM_LIST(LIST)
 if JD[0]:
  DOWNLOAD(JD[1], JD[2])
 else:
  exit("exit")
if __name__ == "__main__" :
 main()