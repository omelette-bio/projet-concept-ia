import xml.etree.ElementTree as ET
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("file", help="the file to parse")
args = parser.parse_args()



def xml_to_pdf(xml_file):
   tree = ET.parse(xml_file)
   root = tree.getroot()
   transitions = {}
   
   file_name = xml_file[:-4]
   dot_file = file_name + ".dot"
   pdf_file = file_name + ".pdf"

   for i in root:
      for j in i:
         if j.tag == "valmatrix":
            for k in j:
               l = len(k.text)
               debut = k.text[0:l//2].replace(" ", "")
               fin = k.text[l//2:l].replace(" ", "")
               if debut not in transitions:
                  transitions[debut] = []
               transitions[debut].append(fin.strip())
   
   try :
      dot = os.open(dot_file, os.O_WRONLY | os.O_CREAT)
   except:
      print("error while creating the dot file")
   
   #creating the style of the graph
   os.write(dot,bytes("digraph {\n", 'utf-8'))
   os.write(dot, bytes("node[shape=circle, style=filled, fillcolor=white, color=black, fontcolor=black, fontsize=12];\n", 'utf-8'))

   #creating the nodes with the help of the transitions dictionary
   for i in transitions:
      for j in transitions[i]:
         os.write(dot, bytes(i + " -> " + j + "\n", 'utf-8'))
         
   os.write(dot,bytes("}", 'utf-8'))

   os.close(dot)

   # creating the pdf file
   if os.fork() == 0:
      os.execvp("dot", ["dot", "-Tpdf", dot_file, "-o", pdf_file])

   os.wait()
   
   # once the pdf file is created, we delete the dot file
   # os.remove(dot_file)
   
   if os.fork() == 0:
      os.execvp("open", ["open", pdf_file])

def dot_to_xml(dot_file):
   try:
      dot = os.open(dot_file, os.O_RDONLY)
   except:
      print("The file does not exists")
      return

   xml_file = dot_file[:-4] + ".xml"
   # reading the dot file to get the transitions
   transitions = {}
   # splitting the file into a list of words with the help of the spaces and the new lines
   dot_transitions = os.read(dot, 8192).decode('utf-8').split()
   
   for i in range(len(dot_transitions)):
      if dot_transitions[i] == "->":
         if dot_transitions[i-1] not in transitions:
            transitions[dot_transitions[i-1]] = []
         transitions[dot_transitions[i-1]].append(dot_transitions[i+1])

   print(transitions)
   


   

if __name__ == "__main__":
   # if the file given is a xml file
   if args.file[-4:] == ".xml":
      xml_to_pdf(args.file)
   elif args.file[-4:] == ".dot":
      dot_to_xml(args.file)
   else:
      print("The file given is not a xml file")