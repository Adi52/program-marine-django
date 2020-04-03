ones = ["", "jeden", "dwa", "trzy", "cztery", "pięć",
        "sześć", "siedem", "osiem", "dziewięć"]

tens = ["dziesięć", "jedenaście", "dwanaście", "trzynaście",
        "czternaście", "piętnaście", "szesnaście", "siedemnaście",
        "osiemnaście", "dziewiętnaście"]

twenties = ["", "", "dwadzieścia", "trzydzieści", "czterdzieści",
            "pięćdziesiąt", "sześćdziesiąt", "siedemdziesiąt",
            "osiemdziesiąt", "dziewięćdziesiąt"]

hundreds = ["", "sto", "dwieście", "trzysta", "czterysta",
            "pięćset", "sześćset", "siedemset", "osiemset",
            "dziewięćset"]
thousands = ["", "", "milion", "miliard",
             "bilion", "biliard", "trylion", "tryliard",
             "kwadrylion", "kwadryliard", "kwintylion",
             "kwintyliard", "sekstylion", "sekstyliard",
             "septylion", "septyliard", "oktylion",
             "oktyliard", "nonilion", "noniliard",
             "decylion", "decyliard", "undecylion",
             "undecyliard", "duodecylion", "duodecyliard",
             "trycylion", "trycyliard", "kwadragilion",
             "kwadragiliard", "oktogilion", "oktogiliard",
             "centylion", "centyliard"]


def get_suf(y):
    if y == 1:
        return ""
    elif y in (2, 3, 4):
        return "y"
    return "ów"


def get_thousand(y, d):
    if d > 0:
        return "tysiący"
    else:
        if y == 1:
            return "tysiąc"
        elif y in (2, 3, 4):
            return "tysiące"
        return "tysiący"


def say_int(n):
    tri = []
    ns = str(n)
    for k in range(3, 3 * len(thousands), 3):
        r = ns[-k:]
        q = len(ns) - k
        if q < -2:
            break
        else:
            tri.append(int(r[:3 + min(0, q)]))
    suf = ""
    out = []
    for i, x in enumerate(tri):
        if x == 0:
            continue
        b1 = x % 10
        b2 = (x % 100) // 10
        b3 = (x % 1000) // 100

        suf = get_suf(b1)
        if i == 1:
            t = get_thousand(b1, b2)
        else:
            t = thousands[i]
            if t and suf:
                t += suf

        out.append(t)

        if b2 == 0:
            on = ones[b1]
            if on:
                out.append(on)
        elif b2 == 1:
            te = tens[b1]
            if te:
                out.append(te)
        elif b2 > 1:
            on = ones[b1]
            tw = twenties[b2]
            if on:
                out.append(on)
            if tw:
                out.append(tw)
        if b3 > 0:
            hu = hundreds[b3]
            if hu:
                out.append(hu)

    out.reverse()
    return " ".join(out)