import datetime


def create_declaration_resident(document, parking_place, date, yacht, fee, fee_words, owner_details, parking_period,
                                commissioning_body, chip_card):
    parking_period['from'] = parking_period['from'].strftime("%d.%m.%Y")
    parking_period['to'] = parking_period['to'].strftime("%d.%m.%Y")
    media = False
    fee['quarter_fee'] = round(fee['parking_fee'] / 4, 2)
    if chip_card:
        chip_card = 'Tak'
    else:
        chip_card = 'Nie'
    # Sprawdza czy jacht stoi na kei nieopomiarowanej (dodatkowa opłata za media).
    if 'D' in parking_place:
        media = True

    for paragraph in document.paragraphs:
        if 'Miejsce postojowe' in paragraph.text:
            paragraph.text = 'Miejsce postojowe {}                                                               ' \
                             '                                        ' \
                             'Data {}'.format(parking_place, date)

    document.add_paragraph('\n')
    document.add_paragraph('Nazwa jachtu: ', style='List Number').add_run(yacht['name']).bold = True
    document.add_paragraph('Nr rejestracyjny: ', style='List Number').add_run(
        yacht['registration_number']).bold = True
    document.add_paragraph('Port macierzysty: ', style='List Number').add_run(
        yacht['home_port']).bold = True
    document.add_paragraph('Dane jachtu: ', style='List Number')
    p = document.add_paragraph('            Długość: ')
    p.add_run(str(yacht['length'])).bold = True
    p.add_run(' m')
    p.add_run('             Szerokość: ')
    p.add_run(str(yacht['width'])).bold = True
    p.add_run(' m')
    document.add_paragraph('Typ jachtu: ', style='List Number').add_run(yacht['ytype']).bold = True
    document.add_paragraph('Dane właściciela* lub użytkownika jachtu*: ', style='List Number')
    document.add_paragraph('            - imię i nazwisko: ').add_run(owner_details['name']).bold = True
    document.add_paragraph('            - adres : ').add_run(owner_details['address']).bold = True
    document.add_paragraph('Dane armatora: ', style='List Number')
    document.add_paragraph('            - imię i nazwisko: ').add_run(owner_details['name']).bold = True
    document.add_paragraph('            - adres : ').add_run(owner_details['address']).bold = True
    document.add_paragraph('Podmiot zlecający, podpisujący umowę na postój jachtu: ', style='List Number')
    document.add_paragraph('            - nazwisko imię */ pełna nazwa klubu lub firmy: ').add_run(
        commissioning_body['name']).bold = True
    document.add_paragraph('            - adres: ').add_run(commissioning_body['address']).bold = True
    document.add_paragraph('            - tel: ').add_run(commissioning_body['tel']).bold = True
    document.add_paragraph('            - E-mail: ').add_run(commissioning_body['e-mail']).bold = True

    document.add_paragraph('            - NIP klubu/stowarzyszenia: ').add_run(
        commissioning_body['nip']).bold = True
    document.add_paragraph('Deklarowany okres i czas postoju: ', style='List Number')
    document.add_paragraph('            - od dnia: ').add_run(parking_period['from']).bold = True
    document.add_paragraph('            - do dnia: ').add_run(parking_period['to']).bold = True
    document.add_paragraph('')
    x = document.add_paragraph('Opłata za postój wynosi: ', style='List Number').add_run(
        str(fee['parking_fee']) + " zł").bold = True
    document.add_paragraph('Słownie: ', style='List Number').add_run(fee_words).bold = True

    this_year = datetime.date.today().year

    if parking_period['from'] == '01.05.{}'.format(this_year) and parking_period['to'] == '30.04.{}'.format(
            this_year + 1):
        # Rezydent całoroczny
        document.add_paragraph(
            'Czynsz płatny, zgodnie z wystawioną fakturą z góry, jednorazowo lub w poniższych '
            'ratach za każdy kwartał do:')
        document.add_paragraph('      I. 15.05.2020, w kwocie: ').add_run(str(fee['quarter_fee']) + " zł.").bold = True
        document.add_paragraph('     II. 15.08.2020, w kwocie: ').add_run(str(fee['quarter_fee']) + " zł.").bold = True
        document.add_paragraph('    III. 15.11.2020, w kwocie: ').add_run(str(fee['quarter_fee']) + " zł.").bold = True
        document.add_paragraph('    IV. 15.21.2020, w kwocie: ').add_run(str(fee['quarter_fee']) + " zł.").bold = True
        document.add_paragraph('na rachunek Wynajmującego o nr  88 1030 1117 0000 0000 8899 5007.')

    elif parking_period['from'] == '01.05.{}'.format(this_year) and parking_period['to'] == '31.10.{}'.format(
            this_year):
        # Rezydent półroczny
        document.add_paragraph(
            'Czynsz płatny, zgodnie z wystawioną fakturą z góry, jednorazowo lub w poniższych '
            'ratach za każdy kwartał do:')
        document.add_paragraph('      I. 15.05.2020, w kwocie: ').add_run(
            str(round(fee['parking_fee'] / 2, 2)) + " zł.").bold = True
        document.add_paragraph('     II. 15.08.2020, w kwocie: ').add_run(
            str(round(fee['parking_fee'] / 2, 2)) + " zł.").bold = True
        document.add_paragraph('na rachunek Wynajmującego o nr  88 1030 1117 0000 0000 8899 5007.')

    document.add_paragraph('Adres do korespondencji: ', style='List Number').add_run(
        owner_details['address']).bold = True
    document.add_paragraph('Karta chipowa: ', style='List Number').add_run(chip_card).bold = True
    if media:
        p = document.add_paragraph('Dodatkowo zlecone usługi: ', style='List Number')
        p.add_run('184zł - miejsce postojowe na wodzie nieopomiarowane').bold = True
    document.add_paragraph('Miejsce postoju nr: ', style='List Number').add_run(parking_place).bold = True
    document.add_paragraph(
        '\nUprzejmie informujemy, że w trakcie postoju jachtu na przystani NCŻ AWFiS może zaistnieć '
        'konieczność zmiany miejsca lokalizacji postoju jachtu na inne zgodnie z ze wskazaniem '
        'upoważnionego pracownika przystani.\n\n'
        'Oświadczam, iż zapoznałem się z Regulaminem przystani Narodowego Centrum Żeglarstwa AWFiS '
        'Gdańsku, w tym zawarcia umowy na postój. W pełni go akceptuję co poświadczam własnoręcznym '
        'podpisem pod Deklaracją postoju. Oświadczam, iż w przypadku okresu postoju krótszego niż '
        'zadeklarowany (wynikający m.in. ze sprzedaży jachtu) mam świadomość, że stawka będzie '
        'rekalkulowana do krótszego okresu postoju, zgodnie z obowiązującym cennikiem.\n\n').paragraph_format.alignment = 3
    document.add_paragraph(".........................................................				 .........."
                           "...............................................").add_run(
        '   podpis pracownika NCŻ                                                                                 '
        '             podpis (imię, nazwisko)').italic = True
