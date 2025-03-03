# Babellica

Command-line tool for text translation using LLMs or ArgosTranslate. Optional Gradio Web-UI.

## Summary

- [Usage](#usage)
- [Requirements](#requirements)
    - [Packages](#packages)
    - [Argos Translate](#argos-translate)
- [Docker/Podman](#dockerpodman)


## Usage

`./babellica.sh <input_file> <output_file> <from_lang> <to_lang> [llm|argos]`


`from_lang` and `to_lang` arguments may follow [ISO 639](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes). There are 50 language names and codes specified in `babellica.sh`. If there is no correspondence, the program will use what was given as an argument, being that a valid language or not.
 

The last argument can be either `llm` or `argos`. If it is not provided, it will use the default value: `llm`.


Example:

`./babellica.sh input.srt output.srt en pt llm`


### Set a specific model

`./babellica.sh setmodel [model_name] [temperature] [system_message]`


Example:


`./babellica.sh setmodel aya-expanse:32b 0.2`
 

## Requirements

### Packages

#### System Packages

- [`ollama`](https://github.com/ollama/ollama)
- [`pandoc`](https://github.com/jgm/pandoc)
- `poppler-utils`
- `perl`

#### Pip Packages

- [`ollama`](https://github.com/ollama/ollama)
- [`ebooklib`]
- [`argostranslate`](https://github.com/argosopentech/argos-translate)
- [`torch`](https://pytorch.org/get-started/locally/)

## Docker/Podman

### CLI:

```
podman build -f Dockerfile.cli -t babellica:cli
```

Then, run mounting your `pwd` to `/workspace`:

```
podman run -it --rm --volume $(pwd):/workspace babellica:cli --gpus=all babellica:cli <args>
```

Alias:

```
echo "alias babellica:cli='podman run -it --rm --volume \$(pwd):/workspace --gpus=all babellica:cli'" >> ~/.bashrc
```

### Gradio:

```
podman build -f Dockerfile.gradio -t babellica:gradio
```

```
podman run --it --rm -p 7860:7680 --gpus=all babellica:gradio
```

Alias:

```
echo "alias babellica:gradio='podman run -it --rm --gpus=all babellica:gradio'" >> ~/.bashrc
```