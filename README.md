# Arabic-Phonetiser
This is a python script which can translate diacriticized arabic text to IPA

### Usage
```py
from arabic_phonetiser import translate
print(translate("مَرْحَبًا أَيُّهَا اْلعَالَمُ"))
#>> marħaban ʔajjuha lʕaːlam
```
### Rules
- Input text must be in Modern Standard Arabic
- Input text must have full diacritics and germination
- Input text must have a superscript alef for applicable words where a hidden alef is present
- Hamzat Al-Wasl must have a diacritic, with either sukoon if it is not pronounced, or a diacritic if it is at the beginning of a sentence or after a stop
