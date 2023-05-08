#! /usr/bin/env python3

import translate
import os, argparse, sys

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="store_true")
parser.add_argument("-s","--step", help="max number of steps to reach the goal", type=int, default=10)
parser.add_argument("file", help="the file to create the solutions",nargs='?')
args = parser.parse_args()

# show the file solutions.txt
if args.help:
   os.system("more solutions.txt")
   sys.exit(0)

# first, we create a folder to store the solutions

folder_name = os.path.basename(args.file[:-4]) + "_solutions"
os.makedirs(folder_name, exist_ok=True)

# program that takes a xml file, check the solutions with the file talosExamples... .jar and create multiple dot files with the solutions

# first step: create a text file to get the results of the jar file

solutions = os.open(folder_name+"/solutions.txt", os.O_WRONLY | os.O_CREAT)

# second step: call the jar file with the xml file and write the results in the text file
# the command is : java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver 0 -file xml_file

result = os.popen("java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n "+str(args.step)+" -print 0 -resultsType 1 -crossingRiver 0 -file " + args.file).read()
print("Solutions ready")

os.write(solutions, bytes(result, 'utf-8'))
os.close(solutions)

# third step: create the dot files with the solutions
# read the text file and search the line Number of solutions: x (x being the number of solutions)
# store all the solutions in a list

s_read = open(folder_name+"/solutions.txt", "r")
s_list = []
read_solutions = False

for line in s_read:
   if "Number of Solutions:" in line:
      read_solutions = True
   elif read_solutions:
      s_list.append(line.strip())

s_read.close()

os.remove(folder_name+"/solutions.txt")

# modify the s_list to create a list of lists with the nodes

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

# now we have a list of lists with the nodes, we create a list of lists with the transitions

s_list_final = []
for i in range(len(s_list_mod)):
   solution = []
   for j in range(len(s_list_mod[i])):
      if j < len(s_list_mod[i])-1:
         transition = ""
         transition+=s_list_mod[i][j]+" -> "+s_list_mod[i][j+1]
         solution.append(transition)
   s_list_final.append(solution)


# create the dot files with the xml and xml2pdf_dot2xml.py file

translate.xml_to_dot(args.file)

with open(args.file[:-4] + ".dot", "r") as dot:
   dot_file = dot.read()


# now we read the dot file and for each transition in s_list_final, we add [color=red] to the transitions

print("Creating the solutions dot files...")

for i in range(len(s_list_final)):
   dot_temp = dot_file
   for j in range(len(s_list_final[i])):
      if s_list_final[i][j] in dot_file:
         dot_temp = dot_temp.replace(s_list_final[i][j], s_list_final[i][j] + " [color=red]")
   with open(folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions"+str(i)+".dot", "w") as dot:
      dot.write(dot_temp)

print("Done")
# now we create the pdf files with the dot files

print("Creating the solutions png files...")
for i in range(len(s_list_final)):
   os.system("dot -Tpng " + folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions" + str(i) + ".dot -o " + folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions"+str(i)+".png")
   # then we delete the dot files
   os.remove(folder_name + "/" + os.path.basename(args.file[:-4]) + "_solutions" + str(i) + ".dot")
print("Done")