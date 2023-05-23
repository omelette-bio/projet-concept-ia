#! /usr/bin/env python3

import converter
import os, argparse, sys

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="store_true")
parser.add_argument("-s","--step", help="max number of steps to reach the goal", type=int, default=10)
parser.add_argument("file", help="the file to create the solutions",nargs='?')
args = parser.parse_args()

# affiche l'aide
if args.help:
   os.system("more solutions.txt")
   sys.exit(0)

# tout d'abord, vérifier que le fichier donné est bien un fichier xml

if args.file == None or args.file[-4:] != ".xml":
   print("Error: no file given or file not a xml file")
   sys.exit(1)

# ensuite, créer un dossier pour stocker les solutions

folder_name = os.path.basename(args.file[:-4]) + "_solutions"

try:
   os.makedirs(folder_name, exist_ok=True)
except OSError:
   print(f"Creation of the directory {folder_name} failed")
   sys.exit(1)


# puis, créer un fichier solutions.txt dans le dossier

try:
   solutions = os.open(folder_name+"/solutions.txt", os.O_WRONLY | os.O_CREAT)
except OSError:
   print(f"Creation of the file {folder_name}/solutions.txt failed")
   sys.exit(1)

# deuxième étape: créer les solutions avec le fichier jar

try:
   result = os.popen("java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n "+str(args.step)+" -print 0 -resultsType 1 -crossingRiver 0 -file " + args.file).read()
   print("Solutions ready")
except OSError:
   print("Error while calling the jar file")
   os.close(solutions)
   sys.exit(1)

try:
   os.write(solutions, bytes(result, 'utf-8'))
   os.close(solutions)
except OSError:
   print("Error while writing the solutions in the file")
   os.close(solutions)
   sys.exit(1)

# troisième étape: lire le fichier solutions.txt et créer les fichiers dot

s_read = open(folder_name+"/solutions.txt", "r")
s_list = []
read_solutions = False

for line in s_read:
   if "Number of Solutions:" in line:
      read_solutions = True
   elif read_solutions:
      s_list.append(line.strip())

if read_solutions == False:
   print("No solutions found")
   sys.exit(1)

s_read.close()

os.remove(folder_name+"/solutions.txt")

# maintenant, on a une liste de solutions, on va créer une liste de listes avec les noeuds

numbers = "0123456789"

s_list_mod = []

for i in range(len(s_list)):
   solution = []
   for j in range(len(s_list[i])):
      node = ""
      if s_list[i][j] == "(":
         k = j+1
         while s_list[i][k] != ")":
            if s_list[i][k] in numbers:
               node+=s_list[i][k]
            k += 1
         solution.append(node)
   s_list_mod.append(solution)

# maintenant, on a une liste de listes avec les noeuds, on va créer une liste de listes avec les transitions

s_list_final = []
for i in range(len(s_list_mod)):
   solution = []
   for j in range(len(s_list_mod[i])):
      if j < len(s_list_mod[i])-1:
         transition = ""
         transition+=s_list_mod[i][j]+" -> "+s_list_mod[i][j+1]
         solution.append(transition)
   s_list_final.append(solution)


# maintenant, on va créer les fichiers dot avec le fichier xml et le fichier converter.py

res = converter.xml_to_dot(args.file)

if res == 1:
   print("Error while creating the dot file")
   sys.exit(1)


with open(args.file[:-4] + ".dot", "r") as dot:
   dot_file = dot.read()


# maintenant, on va modifier le fichier dot pour mettre en rouge les transitions des solutions

print("Creating the solutions dot files...")

for i in range(len(s_list_final)):
   dot_temp = dot_file
   for j in range(len(s_list_final[i])):
      if s_list_final[i][j] in dot_file:
         dot_temp = dot_temp.replace(s_list_final[i][j], s_list_final[i][j] + " [color=red]")
   with open(folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions"+str(i)+".dot", "w") as dot:
      dot.write(dot_temp)

# suppression du fichier dot initial
os.remove(args.file[:-4] + ".dot")

print("Done")

# création des fichiers png
print("Creating the solutions png files...")
for i in range(len(s_list_final)):
   os.system("dot -Tpng " + folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions" + str(i) + ".dot -o " + folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions"+str(i)+".png")
   # suppression des fichiers dot
   os.remove(folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions" + str(i) + ".dot")
print("Done")
sys.exit(0)