from string import punctuation
from re import sub

class Pronounciation:
    def __init__(self, phoneme, needsDiacritic, predicate):
        self.phoneme = phoneme
        self.predicate = predicate
        self.needsDiacritic = needsDiacritic
class Grapheme:
    def __init__(self, char, isDiacritic, isEmphatic, isSolar, pronounciations):
        self.char = char
        self.isDiacritic = isDiacritic
        self.isEmpathic = isEmphatic
        self.isSolar = isSolar
        self.pronounciations = pronounciations
class Replacement:
    def __init__(self, regex, replacement):
        self.regex = regex
        self.replacement = replacement

postReplacements = [
    #الله، والله، بالله، تالله، إلخ
    Replacement(r'([aiu])(ː?\s*)llaːh([aiu]?\b)', lambda m: f"{m.group(1)}{m.group(2)}llˤɑːh{m.group(3)}" if m.group(1) in 'au' else f"{m.group(1)}{m.group(2)}llaːh{m.group(3)}"),
    #اللهم
    Replacement(r'([aiu])(ː?\s*)llaːhumm([aiu]?\b)', lambda m: f"{m.group(1)}{m.group(2)}llˤɑːhumm{m.group(3)}" if m.group(1) in 'au' else f"{m.group(1)}{m.group(2)}llaːhumm{m.group(3)}"),
    #مائة
    Replacement(r'miaːʔa', lambda m: "miʔa"),
    #هاء الكناية
    Replacement(r'([aiu])h([aiu]) (.[aiu])', lambda m: f"{m.group(1)}h{m.group(2)}ː {m.group(3)}")
]

preReplacements = [
    #عمرو
    Replacement(r'عَمْر([\u0617-\u061A\u064B-\u0652])و', lambda m : f"عَمْر{m.group(1)}"),
    #أولئك
    Replacement(r'أُولٰئِك', lambda m: "أُلٰئِك"),
    #أولو
    Replacement(r'أُولُو', lambda m: "أُلُو"),
    #أولات
    Replacement(r'أُولَات', lambda m: "أُلَات"),
    #أولي
    Replacement(r'أُولِي', lambda m: "أُلِي"),
    #داود
    Replacement(r'دَاوُد', lambda m: "دَاوُود")
]

graphemes = {
    " " : Grapheme(
        " ", False, False, False, [
            Pronounciation(" ", False, lambda str, i: True)
        ]
    ),
    "ٰ" : Grapheme(
        "ٰ", False, False, False, [
            Pronounciation("aː", False, lambda str, i: (len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic) and (i >= 2 and not graphemes[str[i-2]].isEmpathic)),
            Pronounciation("ɑː", False, lambda str, i: (len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic) and (i >= 2 and graphemes[str[i-2]].isEmpathic)),
            
        ]
    ),
    'ا' : Grapheme(
        'ا', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: i == 0),
            Pronounciation("", False, lambda str, i: ((i != 0) and ((str[i-1] == "ً") or (i >= 2 and str[i-1].isspace() and str[i-2] not in punctuation and str[i-2] not in "،.؛<>؟!~’,/") or (str[i-1] == 'و' and (i + 1 == len(str) or str[i + 1] == ' ')) or (len(str) > i + 1 and str[i + 1] == 'ْ')))),
            Pronounciation("a", False, lambda str, i: len(str) > i + 3 and i >= 2 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ' and not graphemes[str[i-2]].isEmpathic),
            Pronounciation("ɑ", False, lambda str, i: len(str) > i + 3 and i >= 2 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ' and graphemes[str[i-2]].isEmpathic),
            Pronounciation("aː", False, lambda str, i: (len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic) and (i >= 2 and not graphemes[str[i-2]].isEmpathic)),
            Pronounciation("ɑː", False, lambda str, i: (len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic) and (i >= 2 and graphemes[str[i-2]].isEmpathic))
            ]
    ),
    'أ' : Grapheme(
        'أ', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: True)
        ]
    ),
    'إ' : Grapheme(
        'إ', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: True)
        ]
    ),
    'آ' : Grapheme(
        'آ', False, False, False, [
            Pronounciation("ʔaː", True, lambda str, i: True)
        ]
    ),
    'ى' : Grapheme(
        'ى', False, False, None, [
            
            Pronounciation("a", False, lambda str, i: len(str) > i + 3 and i >= 2 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ' and not graphemes[str[i-2]].isEmpathic),
            Pronounciation("ɑ", False, lambda str, i: len(str) > i + 3 and i >= 2 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ' and graphemes[str[i-2]].isEmpathic),
            Pronounciation("aː", False, lambda str, i: i >= 2 and not graphemes[str[i-2]].isEmpathic),
            Pronounciation("ɑː", False, lambda str, i: i >= 2 and graphemes[str[i-2]].isEmpathic)
        ]
    ),
    'ب' : Grapheme(
        'ب', False, False, False, [
            Pronounciation("b", True, lambda str, i: True)
        ]
    ),
    'ت' : Grapheme(
        'ت', False, False, True, [
            Pronounciation("t", True, lambda str, i: True)
        ]
    ),
    'ث' : Grapheme(
        'ث', False, False, True, [
            Pronounciation("θ", True, lambda str, i: True)
        ]
    ),
    'ج' : Grapheme(
        'ج', False, False, False, [
            Pronounciation("d͡ʒ", True, lambda str, i: True)
        ]
    ),
    'ح' : Grapheme(
        'ح', False, False, False, [
            Pronounciation("ħ", True, lambda str, i: True)
        ]
    ),
    'خ' : Grapheme(
        'خ', False, True, False, [
            Pronounciation("x", True, lambda str, i: True)
        ]
    ),
    'د' : Grapheme(
        'د', False, False, True, [
            Pronounciation("d", True, lambda str, i: True)
        ]
    ),
    'ذ' : Grapheme(
        'ذ', False, False, True, [
            Pronounciation("ð", True, lambda str, i: True)
        ]
    ),
    'ر' : Grapheme(
        'ر', False, True, True, [
            Pronounciation("r", True, lambda str, i: True)
        ]
    ),
    'ز' : Grapheme(
        'ز', False, False, True, [
            Pronounciation("z", True, lambda str, i: True)
        ]
    ),
    'س' : Grapheme(
        'س', False, False, True, [
            Pronounciation("s", True, lambda str, i: True)
        ]
    ),
    'ش' : Grapheme(
        'ش', False, False, True, [
            Pronounciation("ʃ", True, lambda str, i: True)
        ]
    ),
    'ص' : Grapheme(
        'ص', False, True, True, [
            Pronounciation("sˤ", True, lambda str, i: True)
        ]
    ),
    'ض' : Grapheme(
        'ض', False, True, True, [
            Pronounciation("dˤ", True, lambda str, i: True)
        ]
    ),
    'ط' : Grapheme(
        'ط', False, True, True, [
            Pronounciation("tˤ", True, lambda str, i: True)
        ]
    ),
    'ظ' : Grapheme(
        'ظ', False, True, True, [
            Pronounciation("ðˤ", True, lambda str, i: True)
        ]
    ),
    'ع' : Grapheme(
        'ع', False, False, False, [
            Pronounciation("ʕ", True, lambda str, i: True)
        ]
    ),
    'غ' : Grapheme(
        'غ', False, True, False, [
            Pronounciation("ɣ", True, lambda str, i: True)
        ]
    ),
    'ف' : Grapheme(
        'ف', False, False, False, [
            Pronounciation("f", True, lambda str, i: True)
        ]
    ),
    'ق' : Grapheme(
        'ق', False, False, False, [
            Pronounciation("q", True, lambda str, i: True)
        ]
    ),
    'ك' : Grapheme(
        'ك', False, False, False, [
            Pronounciation("k", True, lambda str, i: True)
        ]
    ),
    'ل' : Grapheme(
        'ل', False, False, True, [
            Pronounciation("l", True, lambda str, i: len(str) == i + 1 or not graphemes[str[i+1]].isSolar),
            Pronounciation("", True, lambda str, i: graphemes[str[i+1]].isSolar)
        ]
    ),
    'م' : Grapheme(
        'م', False, False, False, [
            Pronounciation("m", True, lambda str, i: True),
        ]
    ),
    'ن' : Grapheme(
        'ن', False, False, True, [
            Pronounciation("n", True, lambda str, i: True),
        ]
    ),
    'ه' : Grapheme(
        'ه', False, False, False, [
            Pronounciation("h", True, lambda str, i: True),
        ]
    ),
    'ة' : Grapheme(
        'ة', False, False, False, [
            Pronounciation("h", True, lambda str, i: len(str) == i + 1 or str[i + 1] == 'ْ'),
            Pronounciation("t", True, lambda str, i: not str[i + 1] == 'ْ'),
        ]
    ),
    'و' : Grapheme(
        'و', False, False, False, [
            Pronounciation("u", False, lambda str, i: (len(str) > i + 3 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ') or (len(str) > i + 4 and str[i+1]=='ا' and str[i+2].isspace() and str[i+3] == "ا" and str[i+4] == 'ْ')),
            Pronounciation("uː", True, lambda str, i: len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic),
            Pronounciation("w", True, lambda str, i: graphemes[str[i+1]].isDiacritic),
            
        
        ]
    ),
    'ي' : Grapheme(
        'ي', False, False, False, [
            Pronounciation("i", True, lambda str, i: len(str) > i + 3 and str[i+1].isspace() and str[i+2] == "ا" and str[i+3] == 'ْ'),
            Pronounciation("iː", True, lambda str, i: len(str) == i + 1 or not graphemes[str[i+1]].isDiacritic),
            Pronounciation("j", True, lambda str, i: graphemes[str[i+1]].isDiacritic)
            
        ]
    ),
    'ئ' : Grapheme(
        'ئ', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: True)
        ]
    ),
    'ء' : Grapheme(
        'ء', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: True)
        ]
    ),
    'ؤ' : Grapheme(
        'ؤ', False, False, False, [
            Pronounciation("ʔ", True, lambda str, i: True)
        ]
    ),
    'َ' : Grapheme(
        'َ', True, False, None, [
            Pronounciation("a", False, lambda str, i: (len(str) == i + 1 or (str[i+1] != 'ا' and str[i+1] != 'ى' and str[i+1] != 'ٰ') or (len(str) > i + 2 and (str[i+1] == 'ا' or str[i+1] == 'ى' or str[i+1] != 'ٰ') and str[i + 2] == "ْ")) and not graphemes[str[i-1]].isEmpathic),
            Pronounciation("ɑ", False, lambda str, i: (len(str) == i + 1 or (str[i+1] != 'ا' and str[i+1] != 'ى' and str[i+1] != 'ٰ') or (len(str) > i + 2 and (str[i+1] == 'ا' or str[i+1] == 'ى' or str[i+1] != 'ٰ') and str[i + 2] == "ْ")) and graphemes[str[i-1]].isEmpathic),
            Pronounciation("", False, lambda str, i: len(str) > i + 2 and (str[i+1] == 'ا' or str[i+1] == 'ى' or str[i+1] != 'ٰ') and str[i + 2] == "ْ"),
        ]
    ),
    'ً' : Grapheme(
        'ً', True, False, None, [
            Pronounciation("an", False, lambda str, i: not graphemes[str[i-1]].isEmpathic),
            Pronounciation("ɑn", False, lambda str, i: graphemes[str[i-1]].isEmpathic)
        ]
    ),
    'ِ' : Grapheme(
        'ِ', True, False, None, [
            Pronounciation("i", False, lambda str, i: (len(str) == i + 1 or str[i+1] != 'ي') or (len(str) > i + 2 and str[i+1] == 'ي' and graphemes[str[i+2]].isDiacritic)),
            Pronounciation("", False, lambda str, i: str[i+1] == 'ي')
        ]
    ),
    'ٍ' : Grapheme(
        'ٍ', True, False, None, [
            Pronounciation("in", False, lambda str, i: True)
        ]
    ),
    'ُ' : Grapheme(
        'ُ', True, False, None, [
            Pronounciation("u", False, lambda str, i: (len(str) == i + 1 or str[i+1] != 'و') or (len(str) > i + 2 and str[i+1] == 'و' and graphemes[str[i+2]].isDiacritic)),
            Pronounciation("", False, lambda str, i: str[i+1] == 'و' and (len(str) == i + 2 or not graphemes[str[i+2]].isDiacritic)),
        ]
    ),
    'ٌ' : Grapheme(
        'ٌ', True, False, None, [
            Pronounciation("un", False, lambda str, i: True)
        ]
    ),
    'ْ' : Grapheme(
        'ْ', True, False, None, [
            Pronounciation("", False, lambda str, i: i != 0 and str[i - 1] != "ا")
        ]
    ),
    'ّ' : Grapheme(
        'ّ', True, False, None, [
            Pronounciation("_", False, lambda str, i: True)
        ]
    )
}

for c in punctuation + "،.؛<>؟!~’,/":
    graphemes[c] = Grapheme(
        c, False, False, False, [
            Pronounciation("||" if c=='.' else "|", False, lambda str, i: True)
        ]
    )

def stripDiacritics(word):
    for diactiric in "ًٌٍَُِ":
        word = word.replace(diactiric, "")
    return word

def preprocess(str):
    out = ""
    for replacement in preReplacements:
        str = sub(replacement.regex, replacement.replacement, str)
    for i, c in enumerate(str):
        if (graphemes[c].isDiacritic and (len(str) == i + 1 or str[i+1] in punctuation + "،.؛<>؟!~’,/" or (len(str) > i + 2 and str[i+2] in punctuation + "،.؛<>؟!~’,/"))):
            out += "ْ"
        else: 
            out += c
    return out

def postprocess(str):
    for replacement in postReplacements:
        str = sub(replacement.regex, replacement.replacement, str)
    return str

def translate(str):
    str = preprocess(str)
    out = ""
    wordi = 0
    for i, c in enumerate(str):
        if out != '' and (c in punctuation or c in "،.؛<>؟!~’,/") and out[-1] != " ": out += " "
        if out != '' and c != " " and out[-1] == "|": out += " "
        if c == ' ': wordi += 1

        if c not in graphemes:
            out += c
            continue
        if c == 'ّ':
            out += out[-1]
            continue
        for pronounciation in graphemes[c].pronounciations:
            if pronounciation.predicate(str, i):
                out += pronounciation.phoneme
                break
    return postprocess(out)

# Example, Ayat Al-Kursi, Quran 2:255
# Tajweed rules are not considered.
#print(translate("اَللّٰهُ لَا إِلٰهَ إِلَّا هُوَ اْلحَيُّ اْلقَيُّومْ، لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ، لَهُ مَا فِي اْلسَّمَاوَاتِ وَمَا فِي اْلأَرْضِ، مَنْ ذَا اْلَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ، يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ، وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ، وَسِعَ كُرْسِيُّهُ اْلسَّمَاوَاتِ وَاْلأَرْضَ، وَلَا يَؤُودُهُ حِفْظُهُمَا، وَهُوَ اْلعَلِيُّ اْلعَظِيمْ"))
