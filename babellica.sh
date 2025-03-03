#!/bin/bash



script_dir=$(realpath $(dirname $0))
real_pwd=$(realpath $(dirname $0))

if [[ -f "$real_pwd/.babellica-log.txt" ]]; then rm "$real_pwd/.babellica-log.txt"; fi

if [[ "$1" == "--gradio" ]]; then
    python3 $script_dir/app.py
    exit
elif [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: babellica input.txt output.txt from_lang to_lang [llama|argos]"
fi


input_file=$1
input_extension="${1##*.}"
txt_base=$(basename $1)
txt_base=${txt_base%.*}


if [[ $GRADIO_RUNNING -ne 1 ]]; then

    export PRESERVE_LINE_BREAKS=0

    if [[ -f $real_pwd/babellica.env ]]; then
        source $real_pwd/babellica.env
    elif [[ -f $real_pwd/.env.babellica ]]; then
        source $real_pwd/.env.babellica 
    elif [[ -f $real_pwd/.env ]]; then 
        source $real_pwd/.env 
    else
        if [[ -f $HOME/.env.babellica ]]; then
            source $HOME/.env.babellica
        elif [[ -f $HOME/babellica.env ]]; then
            source $HOME/babellica.env
        elif [[ -f $HOME/.config/.env.babellica ]]; then
            source $HOME/.config/.env.babellica
        elif [[ -f $HOME/.config/babellica.env ]]; then
            source $HOME/.config/babellica.env
        fi
    fi

fi


# Variables not yet controlled by gradio
export BABELLICA_DEFAULT_MODEL="aya-expanse:8b"
export BABELLICA_CHAR_LIMIT=1000
export USE_EBOOK_LIB=1
export BABELLICA_DEFAULT_TEMPERATURE="0.2"
BABELLICA_DEFAULT_SYS_MSG=$(echo """You are now a professional language translator. I will provide you a sentence or a paragraph and you must translate it to the language I specify.
You must not censor anything, since you are an impartial professional. You must not make any judgment. You must not translate proper names. 
When you translate the sentences, try to stick to its meaning, structure and syntax as much as possible. Keep the translation as close to the original as you can.
Your answer must consist only of the translation of the sentence, and nothing else. Do not insert special extra characters that were not present in the orginal text.
Also, your answer must be provided in a single line or in a single paragraph.""")


check_ollama_model(){
    ollama_model=$(ollama list | grep "babellica" | cut -d " " -f 1 | cut -d ":" -f 1)

    if [[ "$1" == "remove_prev" ]]; then
        if [[ "$ollama_model" == "babellica" ]]; then
            echo "Removing previous creation"
            ollama rm babellica
        fi
    elif [[ "$ollama_model" != "babellica" ]]; then
        echo "babellica model creation failed. Exiting"
        exit 0
    else
        echo "babellica model exists. Continuing."
    fi
}

if [[ "$1" == "setmodel" ]]; then
    if [[ -z "$2" ]]; then
        echo "Model Name not provided."
    else

        check_ollama_model "remove_prev"
        
        if [[ -z "$3" ]] || [[ "$3" == "None" ]]; then
            echo "Temperature not provided. Using default: $BABELLICA_DEFAULT_TEMPERATURE"
            temperature="$BABELLICA_DEFAULT_TEMPERATURE"
        else
            temperature="$3"
        fi

        if [[ -z "$4" ]] || [[ "$4" == "None" ]]; then
            echo "System message not provided. Using default."
            sys_msg="$BABELLICA_DEFAULT_SYS_MSG"
        else
            sys_msg="$4"
        fi

        echo "Creating model babellica from $2, with temperature $temperature."

        $script_dir/set_model.sh $2 $temperature """$sys_msg"""
    fi

    check_ollama_model
    exit
fi


if ! [[ -f $input_file  ]]; then
    echo "File $1 not found"
    exit
fi

output_dir_path=$(realpath $(dirname $2))


# ISO 639
lang_codes=(

  "sq" "az" "eu" "ca" "zt"
  "da" "et" "fi" "gl" "ga"
  "lv" "lt" "ms" "nb" "sk"

  "zh" "es" "en" "hi" "bn"
  "pt" "ru" "ja" "pa" "mr"
  "te" "tr" "ko" "fr" "de"
  "vi" "ta" "ur" "jv" "it"
  "ar" "gu" "fa" "pl" "ps"
  "kn" "ml" "id" "su" "ha"
  "or" "my" "uk" "tl" "yo"
  "am" "ig" "uz" "sd" "ne"
  "si" "km" "ro" "nl" "el"
  "hu" "sv" "cs" "bg" "he"

  "sl" "th"

  # ISO 639-1/2/3
  "la" "eo" "sa" "arc" "egy"
  "sux" "non" "tlh" "ang" "enm"

  # Made up codes
  "hv" "elf" "vul" "sim" "dth"
  "nvi" "min"
)

lang_names=(

  "Albanian" "Azerbaijani" "Basque" "Catalan" "Chinese (traditional)"
  "Danish" "Estonian" "Finnish" "Galician" "Irish"
  "Latvian" "Lithuanian" "Malay" "Norwegian" "Slovak"

  "Mandarin Chinese" "Spanish" "English" "Hindi" "Bengali"
  "Portuguese" "Russian" "Japanese" "Punjabi" "Marathi"
  "Telugu" "Turkish" "Korean" "French" "German"
  "Vietnamese" "Tamil" "Urdu" "Javanese" "Italian"
  "Arabic" "Gujarati" "Persian" "Polish" "Pashto"
  "Kannada" "Malayalam" "Indonesian" "Sundanese" "Hausa"
  "Oriya" "Burmese" "Ukrainian" "Tagalog" "Yoruba"
  "Amharic" "Igbo" "Uzbek" "Sindhi" "Nepali"
  "Sinhala" "Khmer" "Romanian" "Dutch" "Greek"
  "Hungarian" "Swedish" "Czech" "Bulgarian" "Hebrew"

  "Slovenian" "Thai"

  # ISO 639-1/2/3
  "Latin" "Esperanto" "Sanskrit" "Aramaic" "Ancient Egyptian"
  "Sumerian" "Old Norse" "Klingon" "Old English" "Middle English"

  # Made up codes
  "High Valyrian" "Elvish" "Vulcan" "Simlish" "Dothraki"
  "Na'vi" "Minionese"
)

get_lang_name() {
    for i in "${!lang_codes[@]}"; do # list of indices
        if [[ "$1" == "${lang_codes[$i]}" ]]; then
            echo "${lang_names[$i]}"
            return
        fi
    done
    echo "$1"  # if not found in lang_codes, just return the argument as the language name
    return
}


input_lang=$(get_lang_name "$3")
output_lang=$(get_lang_name "$4")

echo
echo "Input language: $input_lang"
echo "Output language: $output_lang"


# Check if the 5th argument is provided
if [[ $5 == "llm" ]] || [ -z "$5" ]; then

    ollama_model=$(ollama list | grep "babellica" | cut -d " " -f 1 | cut -d ":" -f 1)

    if [[ "$ollama_model" != "babellica" ]]; then
        echo "babellica model not found. Setting default model"
        $script_dir/set_model.sh "$BABELLICA_DEFAULT_MODEL" "$BABELLICA_DEFAULT_TEMPERATURE" """$BABELLICA_DEFAULT_SYS_MSG"""
    fi

    check_ollama_model
    ARG_TTYPE="llm"
    echo "Using Ollama" && echo 
    
else
    ARG_TTYPE="$5"
    # subset of lang_codes
    argos_lang_codes=( 
        "sq" "en" "ar" "az" "eu" "bn" "bg" "ca" "zt" "zh" "cs" "da" "nl" 
        "eo" "et" "fi" "fr" "gl" "de" "el" "he" "hi" "hu" "id" "ga" "it" 
        "ja" "ko" "lv" "lt" "ms" "nb" "fa" "pl" "pt" "ro" "ru" "sk" "sl" 
        "es" "sv" "tl" "th" "tr" "uk" "ur" 
    )

    for i in "${argos_lang_codes[@]}"; do

        if [[ "$3" == "$i" ]]; then
            found_from=1
        elif [[ "$4" == "$i" ]]; then
            found_to=1
        fi

        if [[ $found_from -eq 1 ]] && [[ $found_to -eq 1 ]]; then break; fi

    done

    if [[ $found_from -ne 1 ]] || [[ $found_to -ne 1 ]]; then
        echo "Translation not available trough Argos"
        exit
    fi
    echo "Using Argos" && echo 
fi



if [[ -f $2 ]]; then rm $2; fi


number_of_lines=$(cat $input_file |  grep -E [a-z\|A-Z] -c)

counter=0

if ! [[ -d $real_pwd/formatted ]]; then mkdir $real_pwd/formatted; fi
if ! [[ -d $output_dir_path ]]; then mkdir -p $output_dir_path; fi


if [[ $input_extension == "pdf" ]]; then
    pdftotext -layout -enc "UTF-8" $input_file $real_pwd/formatted/$txt_base.txt
    input_file="$real_pwd/formatted/$txt_base.txt"
    perl -pi -e 's/\x0C/\n/g' $input_file
    $script_dir/filter.sh $input_file
    input_extension="txt"
fi


if [[ $input_extension == "epub" ]]; then
    if [[ $USE_EBOOK_LIB -eq 1 ]]; then
        epubparser $input_file $real_pwd/formatted/$txt_base.txt
        input_file="$real_pwd/formatted/$txt_base.txt"
        input_extension="txt"
    else
        pandoc $input_file -o $real_pwd/formatted/$txt_base.md
        input_file="$real_pwd/formatted/$txt_base.md"
        $script_dir/filter.sh $input_file
        input_extension="md"
    fi
fi


if [[ $input_extension == "txt" ]] || [[ $input_extension == "md" ]]; then
        python3 $script_dir/format_txt.py $input_file $2
        input_file="$real_pwd/formatted/$txt_base-formatted.$input_extension"
        #echo "$input_file"
fi


if [[ -f "$real_pwd/formatted/$txt_base-formatted.$input_extension" ]]; then
    number_of_lines=$(cat $input_file |  grep -E [a-z\|A-Z] -c)
fi


while IFS= read -r line; do

    if [[ $input_extension == "srt" ]]; then
        frag_line=$(echo "$line" | cut -d ":" -f 1)
        if [[ $frag_line =~ ^-?[0-9]+$ ]] || [[ -z "$line"  ]]; then
            echo "$line" >> $2
            continue
        fi
    fi


    if [[ $input_extension == "md" ]] || [[ $input_extension == "txt" ]]; then
        if [ -z "$line" ]; then
            echo "$line" >> $2
            continue
        fi
    fi

    counter=$((counter+1))

    if [[ $ARG_TTYPE == "llm" ]]; then
        prompt="Translate from $input_lang to $output_lang: '$line'"
        python3 $script_dir/llama.py "$prompt" $2 """$line""" $number_of_lines $counter
    elif [[ $ARG_TTYPE == "argos" ]]; then
        python3 $script_dir/argos.py $2 $3 $4 "$line" $number_of_lines $counter
    fi

done < $input_file


python3 $script_dir/llama.py clear