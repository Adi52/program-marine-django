# ones = ["", "jeden", "dwa", "trzy", "cztery", "pięć",
#         "sześć", "siedem", "osiem", "dziewięć"]
#
# tens = ["dziesięć", "jedenaście", "dwanaście", "trzynaście",
#         "czternaście", "piętnaście", "szesnaście", "siedemnaście",
#         "osiemnaście", "dziewiętnaście"]
#
# twenties = ["", "", "dwadzieścia", "trzydzieści", "czterdzieści",
#             "pięćdziesiąt", "sześćdziesiąt", "siedemdziesiąt",
#             "osiemdziesiąt", "dziewięćdziesiąt"]
#
# hundreds = ["", "sto", "dwieście", "trzysta", "czterysta",
#             "pięćset", "sześćset", "siedemset", "osiemset",
#             "dziewięćset"]
# thousands = ["", "", "milion", "miliard",
#              "bilion", "biliard", "trylion", "tryliard",
#              "kwadrylion", "kwadryliard", "kwintylion",
#              "kwintyliard", "sekstylion", "sekstyliard",
#              "septylion", "septyliard", "oktylion",
#              "oktyliard", "nonilion", "noniliard",
#              "decylion", "decyliard", "undecylion",
#              "undecyliard", "duodecylion", "duodecyliard",
#              "trycylion", "trycyliard", "kwadragilion",
#              "kwadragiliard", "oktogilion", "oktogiliard",
#              "centylion", "centyliard"]
#
#
# def get_suf(y):
#     if y == 1:
#         return ""
#     elif y in (2, 3, 4):
#         return "y"
#     return "ów"
#
#
# def get_thousand(y, d):
#     if d > 0:
#         return "tysiący"
#     else:
#         if y == 1:
#             return "tysiąc"
#         elif y in (2, 3, 4):
#             return "tysiące"
#         return "tysiący"
#
#
# def say_int(n):
#     tri = []
#     ns = str(n)
#     for k in range(3, 3 * len(thousands), 3):
#         r = ns[-k:]
#         q = len(ns) - k
#         if q < -2:
#             break
#         else:
#             tri.append(int(r[:3 + min(0, q)]))
#     suf = ""
#     out = []
#     for i, x in enumerate(tri):
#         if x == 0:
#             continue
#         b1 = x % 10
#         b2 = (x % 100) // 10
#         b3 = (x % 1000) // 100
#
#         suf = get_suf(b1)
#         if i == 1:
#             t = get_thousand(b1, b2)
#         else:
#             t = thousands[i]
#             if t and suf:
#                 t += suf
#
#         out.append(t)
#
#         if b2 == 0:
#             on = ones[b1]
#             if on:
#                 out.append(on)
#         elif b2 == 1:
#             te = tens[b1]
#             if te:
#                 out.append(te)
#         elif b2 > 1:
#             on = ones[b1]
#             tw = twenties[b2]
#             if on:
#                 out.append(on)
#             if tw:
#                 out.append(tw)
#         if b3 > 0:
#             hu = hundreds[b3]
#             if hu:
#                 out.append(hu)
#
#     out.reverse()
#     return " ".join(out)


# -*- coding: UTF-8

# Zamiana liczby na slowa z polska gramatyka
# www.algorytm.org

def words(liczba: int, skala: str = 'długa', jeden: bool = True):
    '''
    Zamienia liczbę na zapis słowny w języku polskim.
    Obsługuje liczby w zakresie do 10^66-1 dla długiej skali oraz 10^36-1 dla krótkiej skali.
    Możliwe pominięcie słowa "jeden" przy potęgach tysiąca.
    '''
    if (skala == 'długa' and abs(liczba) >= 10 ** 66) or (skala == 'krótka' and abs(liczba) >= 10 ** 36):
        raise ValueError('Zbyt duża liczba.')

    jedności = ('', 'jeden', 'dwa', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć')
    naście = ('', 'jedenaście', 'dwanaście', 'trzynaście', 'czternaście', 'piętnaście', 'szesnaście', 'siedemnaście',
              'osiemnaście', 'dziewiętnaście')
    dziesiątki = (
    '', 'dziesięć', 'dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt', 'sześćdziesiąt', 'siedemdziesiąt',
    'osiemdziesiąt', 'dziewięćdziesiąt')
    setki = (
    '', 'sto', 'dwieście', 'trzysta', 'czterysta', 'pięćset', 'sześćset', 'siedemset', 'osiemset', 'dziewięćset')

    grupy = [  # kolejne potęgi tysiąca, z formami gramatycznymi
        ('', '', ''),
        ('tysiąc', 'tysiące', 'tysięcy'),
    ]

    przedrostki = ('mi', 'bi', 'try', 'kwadry', 'kwinty', 'seksty', 'septy', 'okty', 'nony', 'decy')
    for p in przedrostki:
        grupy.append((f'{p}lion', f'{p}liony', f'{p}lionów'))
        if skala == 'długa':
            grupy.append((f'{p}liard', f'{p}liardy', f'{p}liardów'))

    if liczba == 0:
        return 'zero'

    słowa = []
    znak = ''
    if liczba < 0:
        znak = 'minus'
        liczba = -liczba

    g = 0
    while liczba != 0:
        # Liczba jest dzielona na kolejne potęgi tysiąca, od największej.
        s = liczba % 1_000 // 100
        d = liczba % 100 // 10
        j = liczba % 10
        liczba //= 1_000

        if s == d == j == 0:  # brak elementów do nazwania
            g += 1
            continue

        if d == 1 and j > 0:  # łączymy dziesiątki i jedności w -naście
            n = j
            d = j = 0
        else:
            n = 0

        # wybór formy gramatycznej
        if j == 1 and s + d + n == 0:
            forma = 0
        elif 2 <= j <= 4:
            forma = 1
        else:
            forma = 2

        słowa = [setki[s], dziesiątki[d], naście[n], jedności[j] if jeden or g == 0 else '', grupy[g][forma]] + słowa
        g += 1

    słowa.insert(0, znak)
    return ' '.join(s for s in słowa if s)


def change_to_words(n):
    return words(n)