import sys
import os

promptpy_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
log_file = f"{promptpy_dir}/.babellica-log.txt"

try:
    import ollama
except:
    print("ollama module not installed")
    sys.exit(0)

input_prompt = sys.argv[1]


if input_prompt == "clear":

    try:
        import torch
    except:
        sys.exit()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    sys.exit()

elif input_prompt == "clear_non_unicode":
    input_prompt = ''.join([i if ord(i) < 256 else ' ' for i in sys.argv[2]])
    sys.exit(input_prompt)


input_line = sys.argv[3]


response = ollama.generate(
    model='babellica',
    prompt='{0}'.format(input_prompt),
    options={
        'temperature': 0.2
    }
)


generated_text = response.response
response = generated_text


#response = response.replace("\\n", " ").replace("\\","").replace("/", " ").replace("#", "").replace("*", "").strip()
response = response.replace('\\"', '"').replace("\\'", "'").strip()


def check_start_blank(response):
    if response[0] != " ":
        return response
    
    if response[0] == " ":
        response = response[1:]
        check_start_blank(response)



def count_rm_quote(count, list):
    if count % 2 == 0:
        list = list[1:-1]
    return list



## TODO
def check_enclosed_quotes(response):
    
    count = 0

    if input_line[0] == input_line[-1]:
        if input_line[0] == "\"" and response[0] == "\'":
            response[0] = "\""
            if response[-1] == "\'":
                response[-1] == "\""
        elif input_line[0] == "\'" and response[0] == "\"":
            response[0] = "\'"
            if response[-1] == "\"":
                response[-1] == "\'"

    elif response[0] == "\"" and response[0] == response[-1]:
        count = response.count("\"")
    elif response[0] == "\'" and response[0] == response[-1]:
        count = response.count("\'")
        
    # not perfect. This would remove the first and last quotes, improperly:
    #  "In the beginning..." Unquoted text...  "The end."  
    if count != 0:
        response = count_rm_quote(count, response)
    
    return response



response = check_start_blank(response)
response = check_enclosed_quotes(response)
            
#if response[0] == " ":
#    response = response[1:]

#response = ''.join([i if ord(i) < 256 else ' ' for i in response])

if int(os.getenv("PRESERVE_LINE_BREAKS")) == 1:
    newlines = "\n"
else:
    response = response.replace("\\n", " ")
    newlines = "\n" # or use \n\n


with open(sys.argv[2], "a") as file:
    file.write(f"{response}{newlines}")


percentage = (float(sys.argv[5])/float(sys.argv[4])) * 100


with open(log_file, "a") as f:
    f.write("-"*60 + "\n\n")
    f.write(sys.argv[3] + "\n\n")
    f.write(response + "\n\n")
    f.write(f"{sys.argv[5]} / {sys.argv[4]} = {percentage:.2f}%\n")
    f.write("-"*60 + "\n\n")


print()
print("-"*60, end="\n\n")
print(sys.argv[3], end="\n\n")
print(response, end="\n\n")
print(f"{sys.argv[5]} / {sys.argv[4]} = {percentage:.2f}%\n")
print("-"*60)
print()


