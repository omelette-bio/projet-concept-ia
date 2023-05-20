#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse, os, sys

def xml_to_dot(xml_file):
   tree = ET.parse(xml_file)
   root = tree.getroot()
   transitions = {}
   
   file_name = xml_file[:-4]
   if __name__ == "__main__":
      if args.save == "default":
         dot_file = file_name + ".dot"
      
      else:
         dot_file = args.save + ".dot"
   
   else:
      dot_file = file_name + ".dot"
      
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
   os.write(dot, bytes("\tnode[shape=circle, style=filled, fillcolor=white, color=black, fontcolor=black, fontsize=12];\n", 'utf-8'))

   # crée le graphe à partir du dictionnaire de transitions
   for i in transitions:
      for j in transitions[i]:
         os.write(dot, bytes("\t"+i + " -> " + j + "\n", 'utf-8'))
         
   os.write(dot,bytes("}", 'utf-8'))

   os.close(dot)






# fonction pour séparer les nombres avec des espaces
def seperate_number(number):
   number_str = ""
   for i in range(len(number)):
      number_str += number[i]
      if i < len(number)-1:
         number_str += " "
   return number_str


def dot_to_xml(dot_file):
   try:
      dot = os.open(dot_file, os.O_RDONLY)
   except:
      print("The file does not exists")
      return

   if args.save == "default":
      xml_file = dot_file[:-4] + ".xml"
   else:
      xml_file = args.save + ".xml"
   
   # reading the dot file to get the transitions
   transitions = {}
   # splitting the file into a list of words with the help of the spaces and the new lines
   dot_transitions = os.read(dot, 8192).decode('utf-8').split()
   
   for i in range(len(dot_transitions)):
      if dot_transitions[i] == "->":
         if dot_transitions[i-1] not in transitions:
            transitions[dot_transitions[i-1]] = []
         transitions[dot_transitions[i-1]].append(dot_transitions[i+1])

   # now we have the transitions in a dictionary, we can create the xml file
   xml = os.open(xml_file, os.O_WRONLY | os.O_CREAT)
   os.write(xml, bytes("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n", 'utf-8'))
   os.write(xml, bytes("<instance format=\"Talos\">\n", 'utf-8'))
   os.write(xml, bytes("\t<values>\n", 'utf-8'))
   os.write(xml, bytes("\t\t<valmatrix>\n", 'utf-8'))
   for i in transitions:
      # seperating the number in i with a space
      for j in transitions[i]:
         os.write(xml, bytes("\t\t\t<data>" + seperate_number(i) + " " + seperate_number(j) + "</data>\n", 'utf-8'))
   os.write(xml, bytes("\t\t</valmatrix>\n", 'utf-8'))
   os.write(xml, bytes("\t</values>\n", 'utf-8'))
   os.write(xml, bytes("</instance>\n", 'utf-8'))
   
   os.close(xml)


   

if __name__ == "__main__":
   parser = argparse.ArgumentParser(add_help=False)
   parser.add_argument("--save", help="select the file to save to",default="default", type=str)
   parser.add_argument("-h","--help", action="store_true")
   parser.add_argument("file", help="the file to parse", nargs='?')
   args = parser.parse_args()
   
   if args.help:
      os.system("more converter.txt")
      sys.exit(0)
   
   # if the file given is a xml file
   if args.file[-4:] == ".xml":
      xml_to_dot(args.file)
   elif args.file[-4:] == ".dot":
      dot_to_xml(args.file)
   else:
      print("The file given is not a xml nor a dot file")