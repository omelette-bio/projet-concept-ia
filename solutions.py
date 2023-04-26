import xml2pdf_dot2xml, os, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="the file to create the solutions")
args = parser.parse_args()

# file that takes a xml file, check the solutions with the file talosExamples... .jar and create multiple dot files with the solutions

# first step: create a text file to get the results of the jar file

solutions = os.open("solutions.txt", os.O_WRONLY | os.O_CREAT)

# second step: call the jar file with the xml file and write the results in the text file
# the command is : java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver 0 -file xml_file

result = os.popen("java -cp talosExamples-0.4-SNAPSHOT-jar-with-dependencies.jar StateGraph -n 10 -print 0 -resultsType 1 -crossingRiver 0 -file " + args.file).read()

os.write(solutions, bytes(result, 'utf-8'))
os.close(solutions)

# third step: create the dot files with the solutions
# read the text file and search the line Number of solutions: x (x being the number of solutions)
# store all the solutions in a list

s_read = open("solutions.txt", "r")
s_list = []
read_solutions = False

for line in s_read:
   if "Number of Solutions:" in line:
      read_solutions = True
   elif read_solutions:
      s_list.append(line.strip())

s_read.close()

# modify the s_list to create a list of lists with the nodes, nodes are seperated by ( and )

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

xml2pdf_dot2xml.xml_to_pdf(args.file)

with open(args.file[:-4] + ".dot", "r") as dot:
   dot_file = dot.read()


# now we read the dot file and for each transition in s_list_final, we add [color=red] to the transitions

for i in range(len(s_list_final)):
   dot_temp = dot_file
   for j in range(len(s_list_final[i])):
      if s_list_final[i][j] in dot_file:
         dot_temp = dot_temp.replace(s_list_final[i][j], s_list_final[i][j] + " [color=red]")
   with open(args.file[:-4] + "_solutions"+str(i)+".dot", "w") as dot:
      dot.write(dot_temp)

# now we create the pdf files with the dot files

for i in range(len(s_list_final)):
   os.system("dot -Tpdf " + args.file[:-4] + "_solutions"+str(i)+".dot -o " + args.file[:-4] + "_solutions"+str(i)+".pdf")