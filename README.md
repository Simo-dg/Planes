# Planes
✈️ 
## About
This project is intended for educational purposes. It serves as a practical application of various Python libraries including Selenium for web scraping, BeautifulSoup for parsing HTML, and Folium for data visualization. The project demonstrates how to extract data from websites, manipulate and process the data, and visualize the results in a meaningful way.

Please note that this project should be used responsibly and in accordance with the terms of service of the websites being scraped. Always respect the rules and regulations of web scraping to ensure ethical use of this project.
This Python script is designed to scrape flight data from a website and create an interactive map to visualize flight routes. The script uses Selenium for web scraping and BeautifulSoup for parsing HTML. It also uses Folium to create interactive maps.
## Getting Started

Follow these steps to set up and run the project:

1. Clone this repository to your local machine.

2. Install the required Python packages using `pip`:
  ```bash
   pip install -r requirements.txt
   ```
3. Run the script

## File Structure

- `script.py`: The main Python script.
- `requirements.txt`: A file listing the project's dependencies and their versions.
- `Airports.db`: A database containing airports' coordinates

## How the Script Works

1. Scraping Aircraft Data
The script starts by scraping aircraft data from a specific URL using Selenium and BeautifulSoup. It extracts information about aircraft models and their corresponding tail numbers from the website. The data is stored in a dictionary.

2. Scraping Flight Data
The script then uses the tail numbers obtained in the previous step to scrape flight data for each aircraft. It uses Selenium to visit flight tracking pages on FlightAware and collects information such as aircraft type, origin, destination, and airport codes. This data is stored in a dictionary.

3. Getting Airport Coordinates
The script retrieves airport coordinates (latitude and longitude) from an SQLite database (Airports.db) for the unique destination airports in the flight data. The coordinates are used later to plot the flight routes on the map.

4. Saving Flight Data
The flight data, including tail numbers, aircraft types, origins, and destinations, is saved to a text file (out.txt) for further analysis if needed.

5. Creating an Interactive Map
Using Folium, the script creates an interactive map (mappa_voli.html). It plots flight routes on the map, with different aircraft types represented by marker clusters. Each marker on the map represents an aircraft's destination airport, and clicking on a marker displays information about the aircraft.

## Data Sources
The airport data used in this project is sourced from the Sì, è una buona pratica citare la fonte dei dati che stai utilizzando nel tuo progetto. Puoi aggiungere queste informazioni nella sezione "Credits" o "Data Sources" del tuo README. Ecco un esempio di come potresti farlo:

## Data Sources

The airport data used in this project is sourced from the [Airports Code Database](https://public.opendatasoft.com/explore/dataset/airports-code/information/) provided by OpenDataSoft. 
Please ensure that any use of the data adheres to the terms of the license and credit the original source appropriately. 

## License
The database used in this project is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit [License](https://creativecommons.org/licenses/by-sa/3.0/).
Please ensure that any use of the data adheres to the terms of the license.

Note: The script currently scrapes data for the first 5 aircraft because it is in a test phase.

