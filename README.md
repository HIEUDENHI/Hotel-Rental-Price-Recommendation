# Hotel Rental Price Recommendation App

## Introduction
This project was created during my freshman year when I first delved into data science, analysis, and web scraping. The idea struck me while booking a room on Booking.com, inspiring me to build an application that recommends rental prices for hotel owners.

## Overview
This project is designed to help hotel owners determine an optimal rental price for their properties. It consists of three main components:
- **Web Scraper**: Scrapes hotel data from Booking.com using Selenium (see [scraper.py]).
- **Data Processing and Model Training**: Cleans the scraped data and trains a machine learning model to predict rental prices (refer to `data_processing.ipynb`).
- **Streamlit Web App**: Provides an interactive interface where users input property details and receive a price recommendation based on the trained model (see [app.py]). Due to the relatively small dataset, the trained model has a mean absolute error (MAE) of approximately 1 million VND, so the app outputs a recommended price range with a margin of around 1 million VND.

## Project Components

- **scraper.py**  
  Utilizes Selenium to:
  - Navigate Booking.com, handle pop-ups, and load additional results.
  - Scrape key property details such as name, price, distance, room size, and amenities (e.g., sea view, rooftop pool, minibar).
  - Save the collected data into a CSV file (e.g., `couple_booking_data.csv`).

- **data_processing.ipynb**  
  A Jupyter Notebook for:
  - Cleaning and preprocessing the scraped data.
  - Training a machine learning model to predict rental prices.
  - Saving the trained model as a pickle file (e.g., `train_model.sav`).

- **app.py**  
  A Streamlit application that:
  - Loads the pre-trained model.
  - Collects user inputs (e.g., distance from the city center, room size, number of guests, and amenities).
  - Outputs a recommended rental price based on the input features, with a recommendation range that accounts for a model error margin of about 1 million VND.


