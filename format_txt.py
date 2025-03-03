import sys
import os
from pathlib import Path


txt_file = sys.argv[1]
extension = Path(txt_file)
extension = extension.suffix
output_file = sys.argv[1]
output_file = Path("{0}".format(output_file)).stem
dirname = os.path.dirname(output_file) 

if os.getenv("BABELLICA_CHAR_LIMIT") != None:
	char_limit = int(os.getenv("BABELLICA_CHAR_LIMIT"))
else:
	char_limit = 1000


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
output_file="{0}/formatted/{1}-formatted{2}".format(script_dir ,output_file, extension)


def check_remove_file(file_to_remove):
	check_file = os.path.isfile(file_to_remove)
	if check_file:
		os.remove(file_to_remove)


check_remove_file(output_file)


def txt_filter(txtread):
	txtread = txtread.replace(u'\ufeff', '').replace("*", "")
	txtread = txtread.replace("‘", "'").replace("’", "'").replace('“', '"').replace('”', '"').replace("'", "'")
	txtread = txtread.replace("_", "").replace('----"', "").replace(":--", ":").replace("--", "-").replace("GENERICCHAPTERDIVISION", "-*-").replace("\n\n", "-*-")
	
	if int(os.getenv("PRESERVE_LINE_BREAKS")) == 0:
		txtread = txtread.replace('\n', ' ')

	return txtread



def line_filter(line):
	line = line.strip()
	continue_condition = 0
	if line == "\n" or line == '\"' or line == '"' or line == "'\"" or len(line) < 2 or not line:
		continue_condition = 1

	return [line, continue_condition]



list_of_splitters = [".,",'."',".","--", "—", " - ", "-", "?", "!", "...",";", ":", ","]

def check_char_limit(line, char_limit, list_of_lines, list_of_splitters):

	if len(line) <= char_limit:
		list_of_lines.append(line)
		return
	
	elif list_of_splitters != None: 
		
		for pos, splitter in enumerate(list_of_splitters):
			
			if splitter in line:
				
				frag_line = line.replace(splitter, "{0} -*-".format(splitter))
				frag_line = frag_line.split(" -*-")
				
				if frag_line[-1] == '':
					frag_line.pop()

				list_of_splitters_cp = list_of_splitters.copy()
				list_of_splitters_cp.remove(splitter)
				
				for fl in frag_line:
			
					check_char_limit(fl, char_limit, list_of_lines, list_of_splitters_cp)
					
				return
				
			elif splitter == list_of_splitters[-1]:	
				list_of_lines.append(line)
			
				return
	else:
		list_of_lines.append(line)	
		return


with open(txt_file, 'r') as file:
	text_var = file.read()
	text_var = txt_filter(text_var)
	text_var = text_var.split("-*-")    
    

for line in text_var:

	line = line_filter(line)
	
	if line[1]:
		continue
	else:
		line = line[0]

		list_of_lines = []
  	    
		check_char_limit(line, char_limit, list_of_lines, list_of_splitters)	

		#print(list_of_lines)
		for i in list_of_lines:
	
			i = line_filter(i)

			if i[1]:
				continue
			else:
				i = i[0]

				with open(output_file, "a") as file:
					file.write(f"{i.strip()}")
			
			with open(output_file, "a") as file:
				file.write(f"\n")

	with open(output_file, "a") as file:
		file.write(f"\n")
