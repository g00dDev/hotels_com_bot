# -*- coding: utf-8 -*-
from utils.http_api.html_fabric import html_chunk

# Dictionaries of text notations used in the main code

API_LEX: dict = {
    'de_DE': {
        'address': 'Adresse:',
        'cmd_date_time': 'Datum und Uhrzeit der Anfrage:',
        'curr_price': 'Aktueller Preis:',
        'dist_to_center': 'Entfernung zum Stadtzentrum:',
        'no_city': 'keine Stadt angegeben',
        'no_label': 'keine Angabe',
        'no_street': 'keine Straße',
        'params': 'Abfrageparameter:',
        'request_result': 'Ergebnis der Anfrage:',
        'user_command': 'Befehl:',
    },
    'en_IE': {
        'address': 'Address:',
        'cmd_date_time': 'Date and time of the request:',
        'curr_price': 'Current price:',
        'dist_to_center': 'Distance to the city center:',
        'no_city': 'city is not specified',
        'no_label': 'not specified',
        'no_street': 'street is not specified',
        'params': 'Parameters:',
        'request_result': 'Result of request:',
        'user_command': 'Command:',
    },
    'es_ES': {
        'address': 'La dirección:',
        'cmd_date_time': 'Fecha y hora de solicitud:',
        'curr_price': 'Precio actual:',
        'dist_to_center': 'Distancia al centro de la ciudad:',
        'no_city': 'no se especificó ninguna ciudad',
        'no_label': 'no especificado',
        'no_street': 'sin calle',
        'params': 'Parámetros:',
        'request_result': 'Resultado de la solicitud:',
        'user_command': 'Comando:',
    },
    'fr_FR': {
        'address': 'Adresse:',
        'cmd_date_time': 'Date et heure de la requête:',
        'curr_price': 'Prix actuel:',
        'dist_to_center': 'Distance au centre-ville:',
        'no_city': 'aucune ville spécifiée',
        'no_label': 'non précisé',
        'no_street': 'pas de rue',
        'params': 'Paramètres:',
        'request_result': 'Résultat de la requête:',
        'user_command': 'Commande:',
    },
    'it_IT': {
        'address': 'Indirizzo:',
        'cmd_date_time': 'Data e ora della richiesta:',
        'curr_price': 'Prezzo corrente:',
        'dist_to_center': 'Distanza dal centro città:',
        'no_city': 'nessuna città specificata',
        'no_label': 'non specificato',
        'no_street': 'nessuna strada',
        'params': 'Parametri:',
        'request_result': 'Risultato della richiesta:',
        'user_command': 'Comando:',
    },
    'ru_RU': {
        'address': 'Адрес:',
        'cmd_date_time': 'Дата и время запроса:',
        'curr_price': 'Текущая цена:',
        'dist_to_center': 'Расстояние до центра города:',
        'no_city': 'город не указан',
        'no_label': 'не указано',
        'no_street': 'улица не указана',
        'params': 'Параметры:',
        'request_result': 'Результат запроса:',
        'user_command': 'Команда:',
    },
}
API_LEX['en_US'] = API_LEX['en_IE']

LOCALES: dict = {
    'RU': 'ru_RU',
    'EN': 'en_IE',
    'US': 'en_US',
    'DE': 'de_DE',
    'FR': 'fr_FR',
    'IT': 'it_IT',
    'ES': 'es_ES',
}
LOCALE_DEF, *_ = LOCALES.values()

LEX_ASSERTION: dict = {
    'de_DE': {
        'YES': 'JA',
        'NO': 'NEIN',
    },
    'en_IE': {
        'YES': 'YES',
        'NO': 'NO',
    },
    'es_ES': {
        'YES': 'SÍ',
        'NO': 'NO',
    },
    'fr_FR': {
        'YES': 'OUI',
        'NO': 'NON',
    },
    'it_IT': {
        'YES': 'SÌ',
        'NO': 'NO',
    },
    'ru_RU': {
        'YES': 'ДА',
        'NO': 'НЕТ',
    },
}
LEX_ASSERTION['en_US'] = LEX_ASSERTION['en_IE']

TB_LEX: dict = {
    'de_DE': {
        'hello': 'Hallo!',
        'another_city': 'Geben Sie einen anderen Stadtnamen ein:',
        'bad_assertion': f"Wähle {LEX_ASSERTION['de_DE']['YES']} oder {LEX_ASSERTION['de_DE']['NO']}",
        'bad_city': f"Es gibt keine solche Stadt oder die Stadt ist nicht "
                    f"in der Datenbank von {html_chunk('de.hotels.com', 'Hotels.com')} enthalten",
        'bad_command': "Unbekannter Befehl. Schreiben /help",
        'bad_currency': 'Währung aus der Liste der vorgeschlagenen Währungen auswählen',
        'bad_distances': 'Die maximale Entfernung muss größer als die minimale sein!',
        'bad_float_number': 'Es wurde eine reelle Zahl erwartet. '
                            'Das Dezimaltrennzeichen ist ein Punkt "."',
        'bad_history': 'Beim Übertragen des Befehlsverlaufs ist ein Fehler aufgetreten. '
                       'Versuchen Sie /delete_history',
        'bad_int_number': 'Positive Ganzzahl erwartet',
        'bad_photos': 'Beim Hochladen von Fotos ist ein Fehler aufgetreten. '
                      'Versuchen Sie, die Anfrage zu ändern',
        'bad_prices': 'Der Höchstpreis muss größer sein als der Mindestpreis!',
        'bad_quota': f"Die maximale Anzahl von Anfragen an den Server wurde erreicht. "
                     f"Versuchen {html_chunk('de.hotels.com', 'Hotels.com')}",
        'bot_stopped': 'Bot wurde gestoppt.',
        'check_in_date': 'Sie haben ein Anreisedatum ausgewählt:',
        'check_out_date': 'Sie haben ein Abreisedatum ausgewählt:',
        'choose_check_in_date': 'Wählen Sie Ihr Anreisedatum:',
        'choose_check_out_date': 'Wählen Sie Ihr Abreisedatum:',
        'choose_currency': 'Währung wählen:',
        'city_chosen': 'Stadt gewählt:',
        'city_req': 'Geben Sie die Stadt an, in der die Hotelsuche durchgeführt wird',
        'currency': 'Aktuelle Währung:',
        'default_locale': f"Standardsprache: {LOCALE_DEF}",
        'dist_min_req': 'Geben Sie die Mindestentfernung vom Hotel zum Stadtzentrum ein',
        'dist_max_req': 'Geben Sie die maximale Entfernung vom Hotel zum Stadtzentrum ein',
        'invalid_number': 'Ungültige Nummer! Zulässige Werte sind auf den Schaltflächen angegeben',
        'greeting_1': "Hallo! Ich bin ein Helfer-Bot",
        'greeting_2': f"Ich helfe Ihnen, mit {html_chunk('de.hotels.com', 'Hotels.com')} und "
                      f"{html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')} "
                      f"schnell Daten über die billigsten, teuersten und am besten geeigneten "
                      f"Hotels in fast jeder Stadt der Welt zu sammeln!",
        'greeting_3': 'Geben Sie einfach /help ein, um zu sehen, was ich tun kann',
        'help': '/help — Hilfe bei Bot-Befehlen\n'
                '/start — Sprache und Währung auswählen\n'
                '/lowprice — die günstigsten Hotels der Stadt anzeigen\n'
                '/highprice — die teuersten Hotels der Stadt anzeigen\n'
                '/bestdeal — zeigt die am besten geeigneten Hotels an, entsprechend '
                'der angegebenen Preisklasse und Entfernungsspanne zum Stadtzentrum\n'
                '/history — Hotelsuchverlauf anzeigen\n'
                '/delete_history — Hotelsuchverlauf löschen',
        'history': 'Befehlsverlauf:',
        'history_check_in': 'Anreisedatum:',
        'history_check_out': 'Abreisedatum:',
        'history_deleted': 'Verlauf gelöscht',
        'history_distances': 'Entfernungsbereich:',
        'history_prices': 'Preisspanne:',
        'hotels_1': 'Hotels',
        'hotels_2': 'Hotels',
        'hotels_list': 'Hotelliste:',
        'hotels_qty_req': 'Anzahl der Hotels eingeben',
        'illegal': 'Ihre Anfrage ist aus rechtlichen Gründen nicht verfügbar',
        'need_photos': 'Möchten Sie Hotelfotos anzeigen?',
        'no_history': 'Hotelsuchverlauf ist leer',
        'pending': 'Anfrage ausstehend...',
        'photos_chosen_1': "Wählen Sie",
        'photos_chosen_2': 'Foto(s) für jedes Hotel aus',
        'photos_qty': 'Wie viele Fotos sollen angezeigt werden?',
        'price_min_req': 'Mindestpreis eingeben (ganzzahlig)',
        'price_max_req': 'Höchstpreis eingeben (ganzzahlig)',
        'req_failure': 'Keine Hotels gefunden...',
        'request_failure': 'Entschuldigung, kein Hotel entspricht Ihrer Anfrage...',
        'request_success': "Anfrage bearbeitet. Freue mich zu helfen ))",
        'seek': 'Suche nach',
        'violation': 'Sie haben keine ausreichenden Berechtigungen für diesen Vorgang!'
    },
    'en_IE': {
        'hello': 'Hello!',
        'another_city': 'Enter another city name:',
        'bad_assertion': f"Choose {LEX_ASSERTION['en_IE']['YES']} or {LEX_ASSERTION['en_IE']['NO']}",
        'bad_city': f"There is no such city or the city is not included "
                    f"in the {html_chunk('hotels.com', 'Hotels.com')} database",
        'bad_command': "Unknown command. Write /help",
        'bad_currency': 'Choose a currency from the currency list',
        'bad_distances': 'Maximum distance must be bigger than the minimum distance!',
        'bad_float_number': 'Expected a real number. Fractional separator - dot "."',
        'bad_history': 'There was an error while transferring commands history. Try /delete_history',
        'bad_int_number': 'Expected a positive integer number',
        'bad_photos': 'There was an error while transferring photos. Try to change your request',
        'bad_prices': 'Maximum price must be bigger than the minimum price!',
        'bad_quota': f"The maximum number of requests to the server has been reached. "
                     f"Try {html_chunk('hotels.com', 'Hotels.com')}",
        'bot_stopped': 'Bot stopped.',
        'check_in_date': 'You have chosen check-in date:',
        'check_out_date': 'You have chosen check-out date:',
        'choose_check_in_date': 'Choose check-in date:',
        'choose_check_out_date': 'Choose check-out date:',
        'choose_currency': 'Choose currency:',
        'city_chosen': 'City chosen:',
        'city_req': 'Specify the city where hotels will be searched',
        'currency': 'Currency:',
        'default_locale': f"Language by default: {LOCALE_DEF}",
        'dist_min_req': 'Specify minimum distance from a hotel to the city center',
        'dist_max_req': 'Specify maximum distance from a hotel to the city center',
        'invalid_number': "Invalid number! Allowed values are indicated on the buttons",
        'greeting_1': "Hello! I'm a helper-bot",
        'greeting_2': f"I can help to quickly gather data about the cheapest, "
                      f"the most expensive and the most suitable hotels "
                      f"in almost any city of the Earth using {html_chunk('hotels.com', 'Hotels.com')} "
                      f"and {html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')}!",
        'greeting_3': 'Just write /help to know about my abilities',
        'help': '/help — help with bot commands\n'
                '/start — choose language and currency\n'
                '/lowprice — search the cheapest hotels in the city\n'
                '/highprice — search the most expensive hotels in the city\n'
                '/bestdeal — search the most suitable hotels in accordance with specified '
                'range of prices and range of distances to the city center\n'
                '/history — display hotels search history\n'
                '/delete_history — delete hotels search history',
        'history': 'Commands history:',
        'history_check_in': 'Check-in date:',
        'history_check_out': 'Check-out date:',
        'history_deleted': 'History of commands was deleted',
        'history_distances': 'Distances range:',
        'history_prices': 'Prices range:',
        'hotels_1': 'hotels',
        'hotels_2': 'hotels',
        'hotels_list': 'List of hotels:',
        'hotels_qty_req': 'Specify hotels quantity',
        'illegal': 'Your request is unavailable for legal reasons',
        'need_photos': 'Need to display photos of hotels?',
        'no_history': 'Hotels search history is empty',
        'pending': 'Request is pending...',
        'photos_chosen_1': "I'll try to display",
        'photos_chosen_2': 'photo(s) for each hotel',
        'photos_qty': 'How many photos to display?',
        'price_min_req': 'Specify the minimum price (integer)',
        'price_max_req': 'Specify the maximum price (integer)',
        'req_failure': 'No hotels were found...',
        'request_failure': 'Unfortunately, no hotels were found matching your request...',
        'request_success': "The request has been processed. I'm glad to help you ))",
        'seek': 'I will seek for',
        'violation': 'You do not have sufficient rights for this operation!'
    },
    'es_ES': {
        'hello': '¡Hola!',
        'another_city': 'Ingrese otro nombre de ciudad:',
        'bad_assertion': f"Elija {LEX_ASSERTION['en_IE']['YES']} o {LEX_ASSERTION['en_IE']['NO']}",
        'bad_city': f"No existe tal ciudad o la ciudad no está incluida "
                    f"en la base de datos de {html_chunk('es.hotels.com', 'Hotels.com')}",
        'bad_command': "Comando desconocido. Escribir /help",
        'bad_currency': 'Seleccione una moneda de la lista de monedas',
        'bad_distances': '¡La distancia máxima debe ser mayor que la mínima!',
        'bad_float_number': 'Se esperaba un número real. El separador decimal es un punto "."',
        'bad_history': 'Ocurrió un error al transmitir el historial de comandos. Pruebe /delete_history',
        'bad_int_number': 'Entero positivo esperado',
        'bad_photos': 'Se produjo un error al cargar las fotos. Intenta cambiar la solicitud',
        'bad_prices': '¡El precio máximo debe ser mayor que el precio mínimo!',
        'bad_quota': f"Se ha alcanzado el número máximo de solicitudes al servidor. "
                     f"Prueba {html_chunk('es.hotels.com', 'Hotels.com')}",
        'bot_stopped': 'El bot se ha detenido.',
        'check_in_date': 'Has seleccionado una fecha de entrada:',
        'check_out_date': 'Has seleccionado una fecha de salida:',
        'choose_check_in_date': 'Seleccione la fecha de entrada:',
        'choose_check_out_date': 'Seleccione la fecha de salida:',
        'choose_currency': 'Elegir moneda:',
        'city_chosen': 'Ciudad elegida:',
        'city_req': 'Especifique la ciudad donde se realizará la búsqueda de hoteles',
        'currency': 'Moneda actual:',
        'default_locale': f"Idioma predeterminado: {LOCALE_DEF}",
        'dist_min_req': 'Ingrese la distancia mínima del hotel al centro de la ciudad',
        'dist_max_req': 'Ingrese la distancia máxima del hotel al centro de la ciudad',
        'invalid_number': "¡Número invalido! Los valores permitidos se indican en los botones",
        'greeting_1': "¡Hola! Soy un bot ayudante",
        'greeting_2': f"¡Te ayudo a recopilar datos rápidamente sobre los hoteles más baratos, "
                      f"más caros y más adecuados en casi cualquier ciudad del mundo usando "
                      f"{html_chunk('es.hotels.com', 'Hotels.com')} y "
                      f"{html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')}!",
        'greeting_3': 'Solo escribe /help para ver qué puedo hacer',
        'help': '/help — ayuda con los comandos del bot\n'
                '/start — seleccionar idioma y moneda\n'
                '/lowprice — muestra los hoteles más baratos de la ciudad\n'
                '/highprice — muestra los hoteles más caros de la ciudad\n'
                '/bestdeal — muestra los hoteles más adecuados, de acuerdo con el rango de '
                'precios especificado y el rango de distancia al centro de la ciudad\n'
                '/history — muestra el historial de búsqueda de hoteles\n'
                '/delete_history — eliminar el historial de búsqueda de hoteles',
        'history': 'Historial de comandos:',
        'history_check_in': 'Fecha de entrada:',
        'history_check_out': 'Fecha de salida:',
        'history_deleted': 'Historial eliminado',
        'history_distances': 'Rango de distancia:',
        'history_prices': 'Rango de precios:',
        'hotels_1': 'hoteles',
        'hotels_2': 'hoteles',
        'hotels_list': 'Lista de hoteles:',
        'hotels_qty_req': 'Ingrese el número de hoteles',
        'illegal': 'Su solicitud no está disponible por razones legales',
        'need_photos': '¿Quieres mostrar fotos del hotel?',
        'no_history': 'El historial de búsqueda de hoteles está vacío',
        'pending': 'Solicitud pendiente...',
        'photos_chosen_1': "Elige",
        'photos_chosen_2': 'foto(s) para cada hotel',
        'photos_qty': '¿Cuántas fotos mostrar?',
        'price_min_req': 'Ingrese el precio mínimo (entero)',
        'price_max_req': 'Ingrese el precio máximo (entero)',
        'req_failure': 'No se encontraron hoteles...',
        'request_failure': 'Lo sentimos, ningún hotel coincidió con su solicitud...',
        'request_success': "Solicitud procesada. Feliz de ayudar ))",
        'seek': 'Buscaré',
        'violation': '¡No tienes suficientes permisos para esta operación!'
    },
    'fr_FR': {
        'hello': 'Bonjour!',
        'another_city': 'Entrez un autre nom de ville:',
        'bad_assertion': f"Choisissez {LEX_ASSERTION['fr_FR']['YES']} ou {LEX_ASSERTION['fr_FR']['NO']}",
        'bad_city': f"Il n'y a pas de telle ville ou la ville n'est pas incluse "
                    f"dans la base de données {html_chunk('fr.hotels.com', 'Hotels.com')}",
        'bad_command': 'Commande inconnue. Écrire /help',
        'bad_currency': 'Sélectionnez une devise dans la liste des devises suggérées',
        'bad_distances': 'La distance maximale doit être supérieure au minimum!',
        'bad_float_number': 'Un nombre réel était attendu. Le séparateur décimal est un point "."',
        'bad_history': "Une erreur s'est produite lors de la transmission de "
                       "l'historique des commandes. Essayez /delete_history",
        'bad_int_number': 'Entier positif attendu',
        'bad_photos': "Une erreur s'est produite lors du téléchargement des photos. "
                      "Essayez de modifier la demande",
        'bad_prices': 'Le prix maximum doit être supérieur au prix minimum!',
        'bad_quota': f"Le nombre maximum de requêtes au serveur a été atteint. "
                     f"Essayez {html_chunk('fr.hotels.com', 'Hotels.com')}",
        'bot_stopped': "Le bot s'est arrêté.",
        'check_in_date': "Vous avez sélectionné une date d'arrivée:",
        'check_out_date': "Vous avez sélectionné une date de départ:",
        'choose_check_in_date': "Sélectionnez la date d'arrivée:",
        'choose_check_out_date': "Sélectionnez la date de départ:",
        'choose_currency': 'Choisir la devise:',
        'city_chosen': 'Ville choisie:',
        'city_req': "Précisez la ville où la recherche d'hôtel sera effectuée",
        'currency': 'Devise actuelle:',
        'default_locale': f"Langue par défaut: {LOCALE_DEF}",
        'dist_min_req': "Entrez la distance minimale entre l'hôtel et le centre-ville",
        'dist_max_req': "Entrez la distance maximale entre l'hôtel et le centre-ville",
        'invalid_number': 'Numéro invalide! Les valeurs autorisées sont indiquées sur les boutons',
        'greeting_1': 'Bonjour! Je suis un assistant bot',
        'greeting_2': f"Je vous aide à collecter rapidement des données sur les hôtels les moins chers, "
                      f"les plus chers et les plus adaptés dans presque toutes les villes du monde en "
                      f"utilisant {html_chunk('fr.hotels.com', 'Hotels.com')} et "
                      f"{html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')}!",
        'greeting_3': 'Tapez simplement /help, pour voir ce que je peux faire',
        'help': "/help — aide avec les commandes du bot\n"
                "/start — sélectionner la langue et la devise\n"
                "/lowprice — affiche les hôtels les moins chers de la ville\n"
                "/highprice — affiche les hôtels les plus chers de la ville\n"
                "/bestdeal — affiche les hôtels les plus adaptés, en fonction de la fourchette "
                "de prix et de la distance spécifiées par rapport au centre-ville\n"
                "/history — affiche l'historique des recherches d'hôtels\n"
                "/delete_history — supprimer l'historique de recherche d'hôtels",
        'history': 'Historique des commandes:',
        'history_check_in': "Date d'arrivée:",
        'history_check_out': "Date de départ:",
        'history_deleted': 'Historique supprimé',
        'history_distances': 'Plage de distances:',
        'history_prices': 'Gamme de prix:',
        'hotels_1': 'hôtels',
        'hotels_2': 'hôtels',
        'hotels_list': 'Liste des hôtels:',
        'hotels_qty_req': "Entrez le nombre d'hôtels",
        'illegal': "Votre demande n'est pas disponible pour des raisons légales",
        'need_photos': "Voulez-vous afficher les photos de l'hôtel?",
        'no_history': "L'historique de recherche d'hôtel est vide",
        'pending': 'Demande en attente...',
        'photos_chosen_1': 'Choisissez',
        'photos_chosen_2': 'photo(s) pour chaque hôtel',
        'photos_qty': 'Combien de photos afficher?',
        'price_min_req': 'Entrez le prix minimum (entier)',
        'price_max_req': 'Entrez le prix maximum (entier)',
        'req_failure': 'Aucun hôtel trouvé...',
        'request_failure': 'Désolé, aucun hôtel ne correspond à votre demande...',
        'request_success': "Requête traitée. Heureux d'aider ))",
        'seek': 'Recherche',
        'violation': "Vous n'avez pas les droits suffisants pour cette opération!"
    },
    'it_IT': {
        'hello': 'Ciao!',
        'another_city': "Inserisci il nome di un'altra città:",
        'bad_assertion': f"Scegli {LEX_ASSERTION['it_IT']['YES']} o {LEX_ASSERTION['it_IT']['NO']}",
        'bad_city': f"Non esiste una tale città o la città non è inclusa "
                    f"nel database di {html_chunk('it.hotels.com', 'Hotels.com')}",
        'bad_command': 'Comando sconosciuto. Scrivi /help',
        'bad_currency': "Seleziona una valuta dall'elenco di valute suggerito",
        'bad_distances': 'La distanza massima deve essere maggiore del minimo!',
        'bad_float_number': 'Ci si aspettava un numero reale. Il separatore decimale è un punto "."',
        'bad_history': 'Si è verificato un errore durante la trasmissione della '
                       'cronologia dei comandi. Prova /delete_history',
        'bad_int_number': 'Intero positivo atteso',
        'bad_photos': 'Si è verificato un errore durante il caricamento delle foto. '
                      'Prova a modificare la richiesta',
        'bad_prices': 'Il prezzo massimo deve essere maggiore del prezzo minimo!',
        'bad_quota': f"È stato raggiunto il numero massimo di richieste al server. "
                     f"Prova {html_chunk('it.hotels.com', 'Hotels.com')}",
        'bot_stopped': 'Il bot si è fermato.',
        'check_in_date': 'Hai selezionato una data di arrivo:',
        'check_out_date': 'Hai selezionato una data di partenza:',
        'choose_check_in_date': 'Seleziona la data di arrivo:',
        'choose_check_out_date': 'Seleziona la data di partenza:',
        'choose_currency': 'Scegli valuta:',
        'city_chosen': 'Città scelta:',
        'city_req': "Specificare la città in cui verrà condotta la ricerca dell'hotel",
        'currency': 'Valuta corrente:',
        'default_locale': f"Lingua predefinita: {LOCALE_DEF}",
        'dist_min_req': "Inserisci la distanza minima dall'hotel al centro città",
        'dist_max_req': "Inserisci la distanza massima dall'hotel al centro città",
        'invalid_number': 'Numero non valido! I valori consentiti sono indicati sui pulsanti',
        'greeting_1': 'Ciao! Sono un bot aiutante',
        'greeting_2': f"Ti aiuto a raccogliere rapidamente i dati sugli hotel più economici, "
                      f"più costosi e più adatti in quasi tutte le città del mondo utilizzando "
                      f"{html_chunk('it.hotels.com', 'Hotels.com')} e "
                      f"{html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')}!",
        'greeting_3': 'Digita /help per vedere cosa posso fare',
        'help': "/help — aiuto con i comandi del bot\n"
                "/start — seleziona lingua e valuta\n"
                "/lowprice — mostra gli hotel più economici della città\n"
                "/highprice — mostra gli hotel più costosi della città\n"
                "/bestdeal — mostra gli hotel più adatti, in base alla fascia di prezzo "
                "specificata e alla fascia di distanza dal centro città\n"
                "/history — mostra la cronologia delle ricerche dell'hotel\n"
                "/delete_history — elimina la cronologia delle ricerche dell'hotel",
        'history': 'Cronologia comandi:',
        'history_check_in': 'Data di arrivo:',
        'history_check_out': 'Data di partenza:',
        'history_deleted': 'Cronologia eliminata',
        'history_distances': 'Intervallo di distanza:',
        'history_prices': 'Fascia di prezzo:',
        'hotels_1': 'hotel',
        'hotels_2': 'hotel',
        'hotels_list': 'Elenco hotel:',
        'hotels_qty_req': 'Inserisci numero di hotel',
        'illegal': 'La tua richiesta non è disponibile per motivi legali',
        'need_photos': "Vuoi visualizzare le foto dell'hotel?",
        'no_history': "La cronologia delle ricerche dell'hotel è vuota",
        'pending': 'Richiesta in sospeso...',
        'photos_chosen_1': "Scegli",
        'photos_chosen_2': 'foto per ogni hotel',
        'photos_qty': 'Quante foto visualizzare?',
        'price_min_req': 'Inserisci il prezzo minimo (numero intero)',
        'price_max_req': 'Inserisci il prezzo massimo (numero intero)',
        'req_failure': 'Nessun hotel trovato...',
        'request_failure': 'Siamo spiacenti, nessun hotel ha soddisfatto la tua richiesta...',
        'request_success': 'Richiesta elaborata. Felice di aiutare ))',
        'seek': 'Cercherò',
        'violation': 'Non hai permessi sufficienti per questa operazione!'
    },
    'ru_RU': {
        'hello': 'Привет!',
        'another_city': 'Введите другое название города:',
        'bad_assertion': f"Выберите {LEX_ASSERTION['ru_RU']['YES']} или {LEX_ASSERTION['ru_RU']['NO']}",
        'bad_city': f"Такого города нет или город не включен "
                    f"в базу данных {html_chunk('ru.hotels.com', 'Hotels.com')}",
        'bad_command': 'Неизвестная команда. Напишите /help',
        'bad_currency': 'Выберите валюту из предложенного списка валют',
        'bad_distances': 'Максимальное расстояние должно быть больше минимального!',
        'bad_float_number': 'Ожидалось действительное число. Разделитель дробной части - точка "."',
        'bad_history': 'Произошла ошибка передачи истории команд. Попробуйте /delete_history',
        'bad_int_number': 'Ожидалось положительное целое число',
        'bad_photos': 'Произошла ошибка передачи фотографий. Попробуйте изменить запрос',
        'bad_prices': 'Максимальная цена должна быть больше минимальной!',
        'bad_quota': f"Достигнуто максимальное количество запросов к серверу. "
                     f"Попробуйте {html_chunk('ru.hotels.com', 'Hotels.com')}",
        'bot_stopped': 'Бот остановлен.',
        'check_in_date': 'Вы выбрали дату заезда:',
        'check_out_date': 'Вы выбрали дату выезда:',
        'choose_check_in_date': 'Выберите дату заезда:',
        'choose_check_out_date': 'Выберите дату выезда:',
        'choose_currency': 'Выберите валюту:',
        'city_chosen': 'Выбран город:',
        'city_req': 'Укажите город, где будет проводиться поиск отелей',
        'currency': 'Текущая валюта:',
        'default_locale': f"Язык по умолчанию: {LOCALE_DEF}",
        'dist_min_req': 'Введите минимальное расстояние от отеля до центра города',
        'dist_max_req': 'Введите максимальное расстояние от отеля до центра города',
        'invalid_number': 'Недопустимое число! Допустимые значения указаны на кнопках',
        'greeting_1': 'Здравствуйте! Я - бот-помощник',
        'greeting_2': f"Я помогаю быстро собрать данные о самых дешевых, "
                      f"самых дорогих и самых подходящих отелях почти в любом городе Земли, "
                      f"используя {html_chunk('ru.hotels.com', 'Hotels.com')} и "
                      f"{html_chunk('rapidapi.com/apidojo/api/hotels4/', 'Rapid API')}!",
        'greeting_3': 'Просто наберите /help, чтобы узнать о моих возможностях',
        'help': '/help — помощь по командам бота\n'
                '/start — выбрать язык и валюту\n'
                '/lowprice — вывести самые дешёвые отели в городе\n'
                '/highprice — вывести самые дорогие отели в городе\n'
                '/bestdeal — вывести наиболее подходящие отели, в соответствии с указанным '
                'диапазоном цен и диапазоном расстояний до центра города\n'
                '/history — вывести историю поиска отелей\n'
                '/delete_history — удалить историю поиска отелей',
        'history': 'История команд:',
        'history_check_in': 'Дата заезда:',
        'history_check_out': 'Дата выезда:',
        'history_deleted': 'История команд удалена',
        'history_distances': 'Диапазон расстояний:',
        'history_prices': 'Диапазон цен:',
        'hotels_1': 'отеля',
        'hotels_2': 'отелей',
        'hotels_list': 'Список отелей:',
        'hotels_qty_req': 'Укажите количество отелей',
        'illegal': 'Ваш запрос недоступен по юридическим причинам',
        'need_photos': 'Фотографии отелей выводить?',
        'no_history': 'История поиска отелей пуста',
        'pending': 'Запрос обрабатывается...',
        'photos_chosen_1': 'Отбираю',
        'photos_chosen_2': 'фото для каждого отеля',
        'photos_qty': 'Сколько фотографий выводить?',
        'price_min_req': 'Введите минимальную цену (целое число)',
        'price_max_req': 'Введите максимальную цену (целое число)',
        'req_failure': 'Ни один отель не найден...',
        'request_failure': 'К сожалению, по Вашему запросу ни один отель не найден...',
        'request_success': 'Запрос обработан. Рад был помочь ))',
        'seek': 'Поищу',
        'violation': 'У Вас недостаточно прав для этой операции!'
    },
}
TB_LEX['en_US'] = TB_LEX['en_IE']
