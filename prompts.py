def create_give_answers_to_question_based_on_context_prompt(context: str):
    return (
            "Jesteś asystentem, który odpowiada na pytania na podstawie dostarczonego kontekstu. "
            "Jeśli odpowiedź znajduje się w kontekście, użyj jej. "
            "Oto kontekst: " + context + ""
                                         "Jeśli nie, odpowiedz zgodnie z własną wiedzą. "
                                         "Odpowiadaj możliwie najkrócej, jednym słowem."
    )

def create_give_answers_to_question():
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
