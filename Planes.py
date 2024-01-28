from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import defaultdict
import sqlite3
import folium
from folium.plugins import MarkerCluster
from folium import LayerControl
from itertools import islice
import time

def get_aircraft_data(url):
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    aircraft_sections = soup.find_all('h2', class_='text-subtitle-2')
    aircraft_data = defaultdict(list)

    for section in aircraft_sections:
        model = section.get_text(strip=True)
        table = section.find_next('table')
        tail_numbers = [a['title'] for a in table.find_all('a', title=lambda x: x and x.startswith('EI-'))]
        aircraft_data[model].extend(tail_numbers)

    if 'Help us improve coverage in your area' in aircraft_data:
        del aircraft_data['Help us improve coverage in your area']

    tail_number_data = {}
    for model, tail_numbers in aircraft_data.items():
        for tail_number in tail_numbers:
            tail_number_data[tail_number] = model

    return tail_number_data

def get_flight_data(tail_number_data):
    driver = webdriver.Chrome()  
    final = {}  
    unique_cities = set()

    for tail_number, aircraft_type in islice(tail_number_data.items(), 5):
        url = "https://flightaware.com/live/flight/" + tail_number
        driver.get(url)
        time.sleep(30)  
        wait = WebDriverWait(driver, 10)

        origine_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.flightPageSummaryCity")))
        destinazione_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.destinationCity")))
        airport_code_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.flightPageSummaryAirportCode')))

        airport_codes = [element.text for element in airport_code_elements]
        origin_airport = airport_codes[0]
        destination_airport = airport_codes[1]

        origine = origine_element.text
        destinazione = destinazione_element.text

        final[tail_number] = [aircraft_type, origine, destinazione, origin_airport, destination_airport]
        unique_cities.add(destination_airport)

        driver.quit()
    return final, list(unique_cities)

def get_airport_coordinates(unique_cities):
    conn = sqlite3.connect('Airports.db')
    cur = conn.cursor()

    airport_coordinates = {}
    for airport_code in unique_cities:
        cur.execute("SELECT Latitude, Longitude FROM airports WHERE AirportCode = ?", (airport_code,))
        result = cur.fetchone()

        if result is not None:
            lat, lon = result
            airport_coordinates[airport_code] = (lat, lon)
    conn.close()

    return airport_coordinates

def save_flight_data(final):
    with open('out.txt', 'w') as file:
        file.write('Tail Number\tAircraft Type\tOrigine\tDestinazione\n')

        for tail_number, data in final.items():
            file.write(f'{tail_number}\t{data[0]}\t{data[1]}\t{data[2]}\n')

def create_map(final, airport_coordinates):
    mappa = folium.Map(location=[0, 0], zoom_start=2)

    clusters = {}
    for modello_aereo in set(val[0] for val in final.values()):
        clusters[modello_aereo] = MarkerCluster(name=modello_aereo).add_to(mappa)

    for tail_number, dati_volo in final.items():
        aereo = dati_volo[0]
        destinazione = dati_volo[4]
        coordinate_destinazione = airport_coordinates.get(destinazione)

        if coordinate_destinazione:
            colore_marcatore = 'red' if aereo == '332' else 'blue'
            popup_text = f"Aereo: {aereo}, Tail Number: {tail_number}"
            marcatore_aereo = folium.Marker(location=coordinate_destinazione, popup=folium.Popup(popup_text), icon=folium.Icon(color=colore_marcatore))

            # Aggiungi il marcatore al cluster corrispondente
            clusters[aereo].add_child(marcatore_aereo)

    LayerControl().add_to(mappa)
    mappa.save('mappa_voli.html')

def main():
    url = "https://planefinder.net/data/airline/ITY/fleet"
    tail_number_data = get_aircraft_data(url)
    final, unique_cities = get_flight_data(tail_number_data)
    airport_coordinates = get_airport_coordinates(unique_cities)
    save_flight_data(final)
    create_map(final, airport_coordinates)

if __name__ == "__main__":
    main()