#!/bin/bash

sed -i "/\[ *[Ii][Ll][Ll][Uu][Ss][Tt][Rr][Aa][Tt][Ii][Oo][Nn]/Id" $1


# remove (# .htm ) ebook pattern
perl -0777 -pi -e 's{
    (?<bal>
         \{ (?:(?> [^{}]+ ) | (?&bal) )* \}      # balanced curly braces
       | \[ (?:(?> [^\[\]]+ ) | (?&bal) )* \]      # balanced square brackets
       | \( (?:(?> [^()]+ ) | (?&bal) )* \)        # balanced parentheses
    )
}{
   $+{bal} =~ /(?:\.(?:htm|html)(?:\.html|\.xhtml)|x-ebookmaker-pageno)/s ? "" : $+{bal}
}xeg' $1



# remove html attributes {.something}
perl -0777 -pi -e 's/\{\s*(?:\.[\w-]+\s*)+\}//gs' $1


# Remove markdown images
perl -pi -e 's/!\[[^]]*\]\([^)]*\)//g' $1


# Remove lines that are ::: and optinal characters
perl -ni -e 'print unless /^\s*:{3,}/' $1


# removes svgs references
perl -0777 -pi -e 's/<svg\b.*?<\/svg>//gsi' $1

# Delete lines with "..." or more or "---" or more or === or more
perl -i -ne 'next if /^\s*(?:\.{3,}|-{3,}|={3,})\s*$/; print' "$1"



perl -pi -e 's/^(#{1,}\s*)\[[^]]*\]\{[^}]+\}\s*/$1/; s/\s*\{[^}]+\}//g' $1
perl -Mutf8 -Mopen=:std,:utf8 -pi -e 's/\N{NO-BREAK SPACE}//g' $1

perl -0777 -i -pe '
  # Remove lines that consist solely of <div> or </div>
  s/^\s*<\/?div>\s*(\n|$)//gm;
  # Remove images in the alternative format, e.g. [colophon]{#... title="..."},
  # even if the curly-brace part spans multiple lines.
  s/\[[^\]]*\]\{.*?\}//gs;
  # Remove all occurrences of braces, brackets, asterisks, forward slashes, and backslashes
  s/[{}\[\]*\/\\]//g;
' $1

perl -i -pe '
  # If a dot followed by dashes is immediately followed by a non-space,
  # replace with a dot plus a space and that character.
  s/(\.)(-+)(\S)/$1 . " " . $3/ge;
  # For remaining cases (dot followed by dashes at end‐of-line or before whitespace),
  # replace with just a dot.
  s/(\.)(-+)//g;
  # Replace two or more consecutive dashes not preceded by a dot with " - "
  s/(?<!\.)-{2,}/ - /g;
' $1


perl -i -0777 -pe 's/```<nav.*?<nav>\s*```//gs' $1

perl -i -0777 -pe '
  # (1) Remove everything from a <nav …> tag to the next literal <nav> tag.
  s/<nav\b[^>]*>.*?<nav>//gs;
  # (2) Remove empty code-fence blocks:
  #     This matches an opening line with triple backticks (and optional whitespace),
  #     followed only by blank lines, and then a closing line with triple backticks.
  s/^\s*`{3}\s*\n(?:\s*\n)*\s*`{3}\s*\n?//gm;
' $1

# replace ": -" by ":"
perl -i -pe 's/:[ \t]*-[ \t]*/:/g' $1

# Replace .... by ...
perl -i -pe 's/\.{4,}/.../g' $1


# Delete lines with "..." or more or "---" or more or === or more
perl -i -ne 'next if /^\s*(?:\.{3,}|-{3,}|={3,})\s*$/; print' "$1"
perl -ni -e 'print unless /^\s*([^\s])(?:\s*\1\s*)*$/' $1


# Turn 4 or more \n into 3
perl -i -0777 -pe 's/(?:\r?\n){4,}/\n\n\n/g' $1

# Delete any whitespace before first character in a line
perl -pi -e 's/^[ \t]+//' $1

# Delte underlines
perl -pi -e 's/_//g' $1


# replaces two or more spaces by a single one:
perl -pi -e 's/ {2,}/ /g' $1


perl -ni -e 'print unless /^\s*(.)\1*\s*$/' $1


# places two newline characters after a header if there is only one
perl -0777 -pi -e 's/^(#.*\n)(?!\n)/$1\n/m' "$1"


