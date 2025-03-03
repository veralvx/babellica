import os
from pathlib import Path
import subprocess
import sys
import time

app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
babellica_bash_path =  app_dir + "/" + "babellica.sh"
babellica_mainpy_path = app_dir + "/" + "main.py"
log_file = f"{app_dir}/.babellica-log.txt"

try:
    import gradio as gr
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
    os.environ["GRADIO_RUNNING"] = "1"
    
except:
    print("Could not load Gradio module")
    sys.exit(0)


lang_dict = {
    "sq": "Albanian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "ca": "Catalan",
    "zt": "Chinese (traditional)",
    "da": "Danish",
    "et": "Estonian",
    "fi": "Finnish",
    "gl": "Galician",
    "ga": "Irish",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "ms": "Malay",
    "nb": "Norwegian",
    "sk": "Slovak",
    "zh": "Chinese (mandarin)",
    "es": "Spanish",
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "pa": "Punjabi",
    "mr": "Marathi",
    "te": "Telugu",
    "tr": "Turkish",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "vi": "Vietnamese",
    "ta": "Tamil",
    "ur": "Urdu",
    "jv": "Javanese",
    "it": "Italian",
    "ar": "Arabic",
    "gu": "Gujarati",
    "fa": "Persian",
    "pl": "Polish",
    "ps": "Pashto",
    "kn": "Kannada",
    "ml": "Malayalam",
    "id": "Indonesian",
    "su": "Sundanese",
    "ha": "Hausa",
    "or": "Oriya",
    "my": "Burmese",
    "uk": "Ukrainian",
    "tl": "Tagalog",
    "yo": "Yoruba",
    "am": "Amharic",
    "ig": "Igbo",
    "uz": "Uzbek",
    "sd": "Sindhi",
    "ne": "Nepali",
    "si": "Sinhala",
    "km": "Khmer",
    "ro": "Romanian",
    "nl": "Dutch",
    "el": "Greek",
    "hu": "Hungarian",
    "sv": "Swedish",
    "cs": "Czech",
    "bg": "Bulgarian",
    "he": "Hebrew",
    "sl": "Slovenian",
    "th": "Thai",
    # ISO 639-1/2/3 codes:
    "la": "Latin",
    "eo": "Esperanto",
    "sa": "Sanskrit",
    "arc": "Aramaic",
    "egy": "Ancient Egyptian",
    "sux": "Sumerian",
    "non": "Old Norse",
    "tlh": "Klingon",
    "ang": "Old English",
    "enm": "Middle English",
    # Made up codes:
    "hv": "High Valyrian",
    "elf": "Elvish",
    "vul": "Vulcan",
    "sim": "Simlish",
    "dth": "Dothraki",
    "nvi": "Na'vi",
    "min": "Minionese"
}


sorted_lang_dict = {k: v for k, v in sorted(lang_dict.items(), key=lambda item: item[1])}
sorted_lang_names = []
sorted_lang_codes = []

for key, value in sorted_lang_dict.items():
    sorted_lang_codes.append(key)
    sorted_lang_names.append(value)



def babellize(input):

    concat_input = []
    srtpubf_found=0

    for x in input["files"]:
        extension = os.path.splitext(x)[1][1:]

        if extension == "epub" or extension == "pdf" or extension == "srt":
            srtpubf_found = 1
            argv_input = x
            continue


        with open(x, "r") as file:
            read_x = file.readlines()
            read_x = " ".join(read_x)
            concat_input.append(read_x)

    if input["text"] is not None and not srtpubf_found:
        concat_input.append(input["text"])

    

    if not srtpubf_found:
        concat_input = " ".join(concat_input)

        with open(".babellica-file.txt", "w") as file:
            argv_input = ".babellica-file.txt"
            file.write(concat_input)
    
        print(concat_input)

    
    if os.getenv("INPUT_LANG") == None or os.getenv("OUTPUT_LANG") == None:
        set_env("English", "French")

    
    # this is a lang code
    input_lang = os.getenv("INPUT_LANG")
    output_lang = os.getenv("OUTPUT_LANG")
    ttype = os.getenv("TRANSLATION_TYPE")
    

    out_file_name = "babellica-translated.txt"
    if os.path.exists(out_file_name) == False:
        open(out_file_name, 'a').close()

    command = ["python3", babellica_mainpy_path, argv_input, out_file_name, input_lang, output_lang, ttype]


    # Open the process, capture stdout, and merge stderr if needed.


    #subprocess.run(
    #    command,
    #    text=True,  # equivalent to universal_newlines=True
    #)


    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,  # equivalent to universal_newlines=True
        bufsize=1
    )



    for line in process.stdout:
        if os.path.exists(out_file_name):
            with open(out_file_name, "r") as tr_file:
                translated_lines = tr_file.readlines()
        else:
            translated_lines = ["Loading..."]

        if os.path.exists(log_file):
            with open(log_file, "r") as lf:
                lf_lines = lf.readlines()
        else:
            lf_lines = ["Loading..."]

        lf_joined = " ".join(lf_lines)
        translated_joined =  " ".join(translated_lines)

        yield lf_joined, translated_joined


    process.stdout.close()
    process.wait()


def set_env(INPUT_LANG, OUTPUT_LANG, TRANSLATION_TYPE="llm", PRESERVE_LINE_BREAKS=0):

    for key, value in locals().items():
        
        hold_value = value

        if hold_value == True:
            hold_value = 1
        elif hold_value == False:
            hold_value = 0
        
        os.environ[key] = str(hold_value)


    for key, value in sorted_lang_dict.items():
        if str(INPUT_LANG) == value:
            input_lang_code = key
        
        if str(OUTPUT_LANG) == value:
            output_lang_code = key


    os.environ["INPUT_LANG"] = input_lang_code
    os.environ["OUTPUT_LANG"] = output_lang_code
    print("env has been set")
    env_result = subprocess.run(["env"], text=True, capture_output=True)
    print(env_result)


with gr.Blocks() as babelblock:


    def show_download():
        return gr.DownloadButton(label="Download", value=f"babellica-translated.txt", visible=True, scale=1,  variant="primary")

    def download_file():
        out_file_name = "babellica-translated.txt"
        return out_file_name

    
    with gr.Row(equal_height=True):
        text_input = gr.MultimodalTextbox(
            interactive=True,
            placeholder="Enter text or upload file...",
            show_label=True,
            sources=["upload"],
            lines=5,
            max_lines=40,
            file_count="single",
            file_types=["text", ".pdf", ".epub"],
            label="Input Text",
            max_plain_text_length=100000000000000000
        )


        with gr.Column():
                text_output = gr.Textbox(
                    interactive=True,
                    label="Translated text",
                    lines=5,
                    max_lines=40,
                    scale=15
                )

                d = gr.DownloadButton("Download the File", visible=False, scale=1,  variant="primary")

        d.click(download_file, None, d)


    with gr.Row(equal_height=True): 

        gr.Interface(
            fn=set_env,
            inputs=[
                gr.Dropdown(
                    sorted_lang_names, value="English",  multiselect=False, label="Input language"
                ),

                gr.Dropdown(
                    sorted_lang_names, value="French", multiselect=False, label="Output Language"
                ),

                gr.Radio(["llm", "argos"], value="llm", label="Translation Type"),

                gr.Checkbox(label="PRESERVE_LINE_BREAKS", value=0, info="Preserve all line breaks for conversion (use for poetry)"),

            ],
            outputs=None,
            live=True

        )

        log = gr.Textbox(
            interactive=False,
            label="Log",
            lines=8,
            max_lines=15,
            min_width=300
        )


    def clear_babellica():
        command = ["ollama", "stop", "babellica"]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,  # equivalent to universal_newlines=True
            )

        time.sleep(1)

        if os.path.exists("babellica-translated.txt"):
            os.remove("babellica-translated.txt")
        if os.path.exists(log_file):
            os.remove(log_file)




        return None, None, gr.DownloadButton("Download the File", visible=False)


    gr.on(
        triggers=[text_input.submit],
        fn=clear_babellica,
        inputs=None,
        outputs=[log, text_output, d]
            ).then(
                fn=babellize,
                inputs=text_input,
                outputs=[log, text_output,]
            ).then(
                fn=show_download,
                inputs=None,
                outputs=d
            )

    
    #chat_msg = text_input.submit(
    #    fn=babellize, inputs=text_input, outputs=[log, text_output]
    #)




def get_models():
    command = ["ollama", "ls"]
    result = subprocess.run(command, text=True, capture_output=True)
    result = str(result).split("\\n")[1:-1]

    models_list = []

    for model in result:
        models_list.append(f"{model.split(":")[0]}:{model.split(":")[1].split(" ")[0]}")
    
    return models_list




def setmodel_pyfunc(input_dr=True, input_tx=None, input_temp=None, input_sys_msg=None):

    if input_tx is None or input_tx == "":
        if input_dr != None:
            model_name = input_dr
    else:
        model_name = input_tx

    print(model_name)
    
    command = ["python3", babellica_mainpy_path, "setmodel", model_name, input_temp, input_sys_msg]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,  # equivalent to universal_newlines=True
        )

    return result.stdout

    


with gr.Blocks() as setmodel_pyfuncblock:
    models_list = get_models()

    input_dr = gr.Dropdown(models_list, value="aya-expanse:8b",  multiselect=False, label="Models installed")
    input_tx = gr.Textbox(placeholder="Enter Model for Ollama...", label="Install Model (optional)")
    input_temp = gr.Textbox(placeholder="Enter Temperature...", label="Temperature (optional)")
    input_sys_msg = gr.Textbox(placeholder="Enter System Message", label="System Message (optional)", lines=4)
    result = gr.Textbox(label="Result")


    def update_dropdown():
        models_list = get_models()
        models_upd = []

        for i in models_list:
            if "babellica" not in i:
                models_upd.append(i)

        return gr.Dropdown(models_upd, value="aya-expanse:8b",  multiselect=False, label="Models installed")

    set_btn = gr.Button("Set Model", variant="primary")


    gr.on(
        triggers=[set_btn.click],
        fn=setmodel_pyfunc,
        inputs=[input_dr, input_tx, input_temp, input_sys_msg],
        outputs=result
    ).then(
        fn=update_dropdown,
        inputs=None,
        outputs=input_dr
    )



demo = gr.TabbedInterface(
    interface_list=[babelblock, setmodel_pyfuncblock],
    tab_names=["Babellica", "setmodel"],
    title="BABELLICA",
    theme=gr.themes.Default(text_size="sm", spacing_size="sm", font=["ui-system", "Arial", "sans-serif", "monospace"])
)



gradio_server = os.getenv("GRADIO_SERVER_NAME")
if gradio_server != "0.0.0.0":
    gradio_server="127.0.0.1"


demo.queue(default_concurrency_limit=2)

try:
    demo.launch(share=False, server_name=gradio_server, pwa=True)
except KeyboardInterrupt:
    print("Shutting down...")
    sys.exit(0)