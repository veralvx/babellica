import sys
import warnings
import os

argos_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
log_file = f"{argos_dir}/.babellica-log.txt"

warnings.filterwarnings(
    "ignore",
    message="You are using `torch.load` with `weights_only=False`",
    category=FutureWarning
)

try:
    import argostranslate.package
    import argostranslate.translate
except:
    print("argostranslate module not installed")
    sys.exit(0)



from_code = sys.argv[2]
to_code = sys.argv[3]

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
installed_packages = argostranslate.package.get_installed_packages()

already_installed = any(
    pkg.from_code == from_code and pkg.to_code == to_code
    for pkg in installed_packages
)


package = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code,
        available_packages
    ),
    None
)


if already_installed:
    print(f"Package for {from_code} -> {to_code} is already installed. Skipping...")

elif package:
    print(f"Installing package for {from_code} -> {to_code}...")
    # Download and install the package
    argostranslate.package.install_from_path(package.download())
else:
    print(f"No package available for {from_code} -> {to_code}")
    with open(log_file, "a") as f:
        f.write(f"No package available for {from_code} -> {to_code}\n")
    sys.exit(0)




translatedText = argostranslate.translate.translate(sys.argv[4], from_code, to_code)



if int(os.getenv("PRESERVE_LINE_BREAKS")) == 1:
    newlines = "\n"
else:
    newlines = "\n\n"



with open(sys.argv[1], "a") as file:
    file.write(f"{translatedText}\n")


percentage = (float(sys.argv[6])/float(sys.argv[5])) * 100



with open(log_file, "a") as f:
    f.write("-"*60 + "\n\n")
    f.write(sys.argv[4] + "\n\n")
    f.write(translatedText + "\n\n")
    f.write(f"{sys.argv[6]} / {sys.argv[5]} = {percentage:.2f}%\n")
    f.write("-"*60 + "\n\n")



print()
print("-"*60, end="\n\n")
print(sys.argv[4], end="\n\n")
print(translatedText, end="\n\n")
print(f"{sys.argv[6]} / {sys.argv[5]} = {percentage:.2f}%\n")
print("-"*60)
print()


