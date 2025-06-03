from typing import List


def create_give_answers_to_question_based_on_context_prompt(context: str):
    return (
            "Jesteś asystentem, który odpowiada na pytania na podstawie dostarczonego kontekstu. "
            "Jeśli odpowiedź znajduje się w kontekście, użyj jej. "
            "Oto kontekst: " + context + ""
                                         "Jeśli nie, odpowiedz zgodnie z własną wiedzą. "
                                         "Odpowiadaj możliwie najkrócej, jednym słowem."
    )

def create_give_answers_to_question_prompt():
    return (
        "Jesteś asystentem, który odpowiada na pytania. "
        "Odpowiadaj możliwie najkrócej, niepełnym zdaniem, bez kropki na końcu"
        "Na przykład: Stolica Polski? Warszawa. Prezydent Polski w 2022? Andrzej Duda."
        "Odpowiadaj w języku, w którym zadano ci pytanie."
    )

def create_fix_answers_prompt():
    return (
        "Jesteś asystentem, który poprawia błędy w pliku JSON. "
        "Twoim zadaniem jest poprawić błędy obliczeniowe oraz odpowiedź na pytania otwarte zawarte w JSON"
        "Plik JSON jest bardzo duży, więc będziesz dostawać go partiami."
        "Poprawisz błędy obliczeniowe oraz odpowiesz na pytania i zwrócić dokładnie taki sam fragment JSON, który dostałeś"
    )


def create_anonymize_personal_data_prompt():
    return (
        "Jesteś asystentem, którego zadaniem będzie anomizacja danych w tekście"
        "Twoim zadaniem jest zamieniń dane osobowe na słowo CENZURA w tekście"
        "Dane osobowe, które musisz anonimizować to: Imię Nazwisko, wiek, miasto, ulica, numer domu zamieszkania"
        "Przykłady: "
        "Jan Kowalski -> CENZURA"
        "Jan Kowalski ma 13 lat -> CENZURA ma CENZURA lat"
        "Jan Kowalski mieszka w Katowicach przy ul. Wolności 13 -> CENZURA mieszka w CENZURA przy ul. CENZURA"
        "Nie redagujesz tekstu, nie parafrazujesz, zwracasz słowo w słowo, zwróć tylko i wyłącznie oryginalny tekst jedynie z anonimizacją danych"
    )

def create_find_street_name_of_university(transcriptions: List[str]):
    return (
        "Jesteś asystentem, którego zadaniem będzie dowiedzenie się przy jakiej ulicy znajduje się konkretny instytut uniwersytetu, gdzie pracuje Andrzej Ma"
        "Dostaniesz transkrypcje rozmów, na których podstawie będziesz musiał podać ulicę"
        "Andrzej Maj jest to fikcyjan postać, więc informacje na jego temat pozyskasz z transkrypcji rozmów, ale musisz użyć własnej wiedzy na temat konkretnej uczelni"
        "Uważaj, bo niektóre nagrania są chaotyczne lub mogą wprowadzic w błąd"
        "Krok po kroku analizuj transkrypcje i wyciągaj wnioski. Na końcu podaj tylko i wyłącznie nazwę ulicy w odmianie przypadku dopełniacza'"
        "Oto rozmowy: \n ".join(
            f"Rozmowa {i+1}: {text}" for i, text in enumerate(transcriptions)
        )
    )

def create_recognize_city_prompt():
    return (
        "Jesteś asystentem, którego zadaniem będzie rozponać miasto na podstawie 4 schematycznych grafik."
        "Jedna grafika nie pasuje do pozostałych"
        "Analizuj fragmenty mapy i zidentyfikuj jakie to miasto."
        "Podaj jakie to miasto"
    )


def create_image_upon_description_prompt(desc: str):
    return (
        "Jesteś asystentem, którego zadaniem będzie wygenerować obraz na podstawie opisu dostarczonego w json: " + desc
    )


def create_extract_text_from_image_prompt():
    return (
        "Jesteś asystentem, którego zadaniem jest wyodrębnić tekst z podanego obrazka. Zwróć tylko i wyłącznie wyodrębniony tekst"
    )

def create_categorize_text_prompt():
    return (
        "Jesteś asystentem, którego zadaniem jest dopasować kategorię do podanego tekstu"
        "Dany tekst można skategoryzować jako jako tekst o ludziach lub tekst o hardwarze"
        "Jeżeli tekst nie pasuje do żadnej z tych kategorii to go pomijamy! Tekst musi pasować, nie tworzymy nowych kategorii"
        "Dostaniesz tekst w formie mapy, gdzie kluczem będzie nazwa pliku, a wartością będzie tekst do skategoryzowania"
        "Odpowiedź zwróć w formacie obiektu: {\"people\":[], \"hardware\":[]}. "
        "Gdzie do tablicy people dodasz klucze, których wartość dotycza ludzi"
        "a do tablicy hardware dodasz klucze, których wartości dotyczą hardwaru"
        "Posortuj alfabetycznie nazwy plików w tablicach"
    )

def create_answer_to_questions_accoring_to_context_test_audio_image(context: str):
    return (
        "Jesteś asystentem, którego zadaniem jest odpowiedzieć na pytania krótko w 1 zdaniu"
        "Odpowiedz udzielisz na podstawie kontekstu, którego Tobie dostarczę. Będzie on tekstem, transkrypcją audio oraz opisem grafik"
        "Odpowiedź zwróć w formacie: { \"idpytania\":\"krótka odpowiedź w 1 zdaniu\"}"
        "Oto kontekst: " + context
    )


def create_give_key_words_based_on_reports_and_facts(reports, facts):
    return (
        "Jesteś asystentem, którego zadaniem jest podać słowa kluczowe dla danych raportów"
        "Dla każdego faktu wyekstrahuj kluczowe informacje (np. osoby, ich zawody, specjalne umiejętności)"
        "Wygeneruj wstępne słowa kluczowe na podstawie jego treści i nazwy pliku. Zidentyfikuj osoby/miejsca wspomniane w raporcie."
        "Dobierz pasujące fakty (np. dotyczące tych samych osób)."
        "Połącz słowa kluczowe z raportu ze słowami kluczowymi wynikającymi z powiązanych faktów."
        "Słowa kluczowa mają być w języku polskim w mianowniku."
        "Zwróć tylko odpowiedź, odpowiedź ma być w formacie: {\"2024-11-12_report-00-sektor_C4.txt\": \"słowo,kluczowe,przykład1\",\"2024-11-12_report-01-sektor_A1.txt\": \"inne,słowa,przykład2\",}"
        "O to raporty: " + str(reports) + ". A o to fakty: " + str(facts)
    )

def create_give_sql_query_prompt(database_metadata: []):
    return (
        "Jesteś asystentem, którego zadaniem jest zwrócić zapytanie sql zgodnie z poniższym kontekstem oraz wymaganiami."
        "O to metadane bazy danych dla której wygenerujesz zapytania. Zawierają ona nazwę tabeli (Table) oraz strukturę tabeli (Create Table)."
        "" + str(database_metadata[0]['reply'][0]) + "."
        "" + str(database_metadata[1]['reply'][0]) + "."
        "" + str(database_metadata[2]['reply'][0]) + "."
        "" + str(database_metadata[3]['reply'][0]) + "."
        "Na podstawie tych metadanych bazy zwróć mi zapytanie, które zwróci nam numery ID czynnych datacenter, które zarządzane są przez menadżerów, którzy aktualnie przebywają na urlopie (są nieaktywni)."
        "Zwróć tylko zapytanie SQL."
    )

def create_extract_people_and_cities_prompt(notes: str):
    return (
        "Jesteś asystentem, którego zadaniem jest wyodrębnić wszystkie osoby oraz miasta jakie pojawiają się w tekście."
        "O to tekst: " + notes + "."
        "Odpowiedź zwróć w formacie json {\"people\": [], \"cities\": []} gdzie w polu poeple oraz cities będzie tablica stringów z osobami oraz miastami."
        "Nie używaj polskich znaków (na przykład Rafal, zamiast Rafał), do tablicy dodawaj tylko imię, bez nazwiska."
        "Miasta zwróć wielkimi literami, np WARSZAWA."
    )

def create_photo_enhance_prompt():
    return (
        "Jesteś asystentem, którego zadaniem jest ocenić jakość fotografii i zadecydować o potrzebnej operacji."
        "Zwracasz tylko poniższe słowa kluczowe: "
        "REPAIR (dla szumów/glitchy)"
        "DARKEN (dla zbyt jasnych)"
        "BRIGHTEN (dla zbyt ciemnych)"
        "NONE (dla zdjęć, które nie potrzebują obróki"
    )

def create_person_description():
    return(
        "Jesteś ekspertem w analizie zdjęć i tworzeniu rysopisów. Twoim zadaniem jest obiektywny opis wyglądu osoby, która znajduje się na zdjęciach."
        "Chodzi o jedną osobę, która pojawia się na wszystkich zdjęciach"
        "Rysopis musi być dokładny."
        "Opisz cechy fizyczne postaci."
        "Rysopis musi być w języku polskim w kodowaniu utf-8."
        "Zwróć tylko rysopis."
    )