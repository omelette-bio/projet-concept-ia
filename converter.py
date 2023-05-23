#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse, os

def xml_to_dot(xml_file):
   tree = ET.parse(xml_file)
   root = tree.getroot()
   
   file_name = xml_file[:-4]
   
   if __name__ == "__main__":
      if args.save == "default":
         dot_file = file_name + ".dot"
      
      else:
         dot_file = args.save + ".dot"
   
   else:
      dot_file = file_name + ".dot"
   
   # ouverture du fichier dot, créé s'il n'existe pas, vidé s'il existe
   try:
      dot = os.open(dot_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
   except:
      print("error while creating the dot file")
      return 1
   
   # creation du style du graphe
   try:
      os.write(dot,bytes("digraph {\n", 'utf-8'))
      os.write(dot, bytes("\tnode[shape=circle, style=filled, fillcolor=white, color=black, fontcolor=black, fontsize=12];\n", 'utf-8'))
   except:
      print("error while writing the dot file")
      return 1
   
   # parcours de l'arbre xml pour récupérer les transitions
   for i in root:
      for j in i:
         if j.tag == "valmatrix":
            for k in j:
               l = len(k.text)
               debut = k.text[0:l//2].replace(" ", "")
               fin = k.text[l//2:l].replace(" ", "")
               try:
                  os.write(dot, bytes("\t"+debut + " -> " + fin + "\n", 'utf-8'))
               except:
                  print("error while writing the dot file")
                  return 1
   try:            
      os.write(dot,bytes("}", 'utf-8'))
   except:
      print("error while writing the dot file")
      return 1
   
   os.close(dot)
   return 0



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
      print("Error while opening the dot file")
      return


   file_name = dot_file[:-4]
   
   if __name__ == "__main__":
      if args.save == "default":
         xml_file = file_name + ".xml"
      else:
         xml_file = args.save + ".xml"
   else:
      xml_file = file_name + ".xml"

   
   # splitting the file into a list of words with the help of the spaces and the new lines
   try:
      dot_transitions = os.read(dot, 8192).decode('utf-8').split()
   except:
      print("Error while reading the dot file")
      return
   
   # ouvre un nouveau fichier xml, le crée s'il n'existe pas, le vide s'il existe
   try:
      xml = os.open(xml_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
   except:
      print("Error while opening/creating the xml file")
      return
   
   # écriture de l'en-tête du fichier xml
   try:
      os.write(xml, bytes("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n", 'utf-8'))
      os.write(xml, bytes("<instance format=\"Talos\">\n", 'utf-8'))
      os.write(xml, bytes("\t<values>\n", 'utf-8'))
      os.write(xml, bytes("\t\t<valmatrix>\n", 'utf-8'))
   except:
      print("Error while writing the xml file")
      return
   
   # écriture des transitions dans le fichier xml
   for i in range(len(dot_transitions)):
      if dot_transitions[i] == "->":
         try:
            os.write(xml, bytes("\t\t\t<data>" + seperate_number(dot_transitions[i-1]) + " " + seperate_number(dot_transitions[i+1]) + "</data>\n", 'utf-8'))
         except:
            print("Error while writing the xml file")
            return
   
   # écriture de la fin du fichier xml
   try:
      os.write(xml, bytes("\t\t</valmatrix>\n", 'utf-8'))
      os.write(xml, bytes("\t</values>\n", 'utf-8'))
      os.write(xml, bytes("</instance>\n", 'utf-8'))
   except:
      print("Error while writing the xml file")
      return
   
   os.close(xml)


   

if __name__ == "__main__":
   parser = argparse.ArgumentParser(add_help=False)
   parser.add_argument("--save", help="select the file to save to",default="default", type=str)
   parser.add_argument("-h","--help", action="store_true")
   parser.add_argument("file", help="the file to parse", nargs='?')
   args = parser.parse_args()
   
   if args.help:
      os.system("more converter.txt")
   else: 
      # if the file given is a xml file
      if args.file[-4:] == ".xml":
         xml_to_dot(args.file)
      elif args.file[-4:] == ".dot":
         dot_to_xml(args.file)
      else:
         print("The file given is not a xml nor a dot file")