import itertools
import argostranslate.package


def install_all_language_pairs(languages):

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()

    print("Starting permutations...")
    pairs = itertools.permutations(languages, 2)

    for from_code, to_code in pairs:
        # Look for the package matching the language pair
        package = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code,
                available_packages
            ),
            None
        )
        if package:
            print(f"Installing package for {from_code} -> {to_code}...")
            # Download and install the package
            argostranslate.package.install_from_path(package.download())
        else:
            print(f"No package available for {from_code} -> {to_code}")

if __name__ == '__main__':
    languages = [
        "sq", "en", "ar", "az", "eu", "bn", "bg", "ca", "zt", "zh",
        "cs", "da", "nl", "eo", "et", "fi", "fr", "gl", "de", "el",
        "he", "hi", "hu", "id", "ga", "it", "ja", "ko", "lv", "lt",
        "ms", "nb", "fa", "pl", "pt", "ro", "ru", "sk", "sl", "es",
        "sv", "tl", "th", "tr", "uk", "ur"
    ]

    print("Starting Languages Installation...")
    
    install_all_language_pairs(languages)
