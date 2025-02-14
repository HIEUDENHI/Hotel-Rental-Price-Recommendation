from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import numpy as np
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set up ChromeDriver path
# chrome_driver_path = "./chromedriver.exe"  # Update this with your ChromeDriver path
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--headless=chrome')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# Function to close popups
def close_popups():
    try:
        time.sleep(5)
        cancel_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss sign in information."]')
        cancel_button.click()
        print("Pop-up closed.")
        time.sleep(5)
    except:
        print(f"No pop-up found or error closing pop-up.")

# Function to click "Load more results" until all results are loaded
def load_all_results():
    while True:
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)
            load_more_button = driver.find_element(By.XPATH, '//button[span[text()="Load more results"]]')
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Loading more results")
            time.sleep(10)
        except Exception as e:
            print("No more 'Load more results' button found or clicking it failed, all results should be loaded.")
            break

# Function to scrape property cards
def scrape_property_cards(base_url):
    driver.get(base_url)
    time.sleep(2)  # Wait for the page to load


    close_popups()

    # Click "Load more results" until all property cards are loaded
    load_all_results() 

    properties = []
    reviewer_list = []
    # Collect all property cards on the page after loading all results
    property_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
    property_id = 1
    print(f"Found {len(property_cards)} property cards after loading all results.")

    # Extract basic details and visit each property link to extract more details
    for card in property_cards:
        try:
            property_price = card.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
        except:
            property_price = np.nan

        try:
            property_name = card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
        except:
            property_name = np.nan


        try:
            property_url = card.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_attribute('href')
        except:
            property_url = np.nan

        try:
            property_distance = card.find_element(By.CSS_SELECTOR, 'span[data-testid="distance"]').text
        except:
            property_distance = np.nan

        try:
            property_rating = card.find_element(By.CSS_SELECTOR, 'div[data-testid="rating-stars"]')
            span_elements = property_rating.find_elements(By.TAG_NAME, "span")
            hotel_star = len(span_elements)
        except:
            hotel_star = 0
    

        driver.execute_script("window.open(arguments[0]);", property_url)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Random sleep to mimic human behavior

        try:
            table=driver.find_element(By.ID,"hprt-table")
            table_body=table.find_element(By.TAG_NAME,"tbody")
            first_row = table_body.find_element(By.TAG_NAME, "tr")
            time.sleep(5)
            try:
                number_of_guests = first_row.find_element(By.CSS_SELECTOR, '.c-occupancy-icons__multiplier-number').text
            except: 
                try:
                    div_element = first_row.find_element(By.CSS_SELECTOR, ".hprt-block .c-occupancy-icons")
                    icon_elements = div_element.find_elements(By.CSS_SELECTOR, "i.bicon.bicon-occupancy")
                    number_of_guests=len(icon_elements)
                except:
                    try:
                        div_element = first_row.find_element(By.CSS_SELECTOR, ".hprt-block .wholesalers_table__occupancy__icons")
                        icon_elements = div_element.find_elements(By.CSS_SELECTOR, "i.bicon.bicon-occupancy")
                        number_of_guests=len(icon_elements)
                    except:
                        number_of_guests=np.nan
                        print("Cannot get number of guests")
            try:
                price_in_table=first_row.find_element(By.CSS_SELECTOR,'div.bui-price-display__value.prco-text-nowrap-helper.prco-inline-block-maker-helper.prco-f-font-heading').text
            except:
                price_in_table=np.nan
            try:
                property_detail = first_row.find_element(By.CSS_SELECTOR, 'a[class="hprt-roomtype-link"]')
                property_detail.click()
            except:
                try:
                    property_detail = first_row.find_element(By.CSS_SELECTOR, 'a[class="hprt-roomtype-link hprt-ws-roomtype-link wholesalers_table__roomname__text"]')
                    property_detail.click()  
                except:
                    print("Cannot click detail popup")
            time.sleep(5)
            try:
                right_container=driver.find_element(By.CSS_SELECTOR,'div[class="hprt-lightbox-right-container"]')
                try:
                    room_name=right_container.find_element(By.CSS_SELECTOR,'h1[id="hp_rt_room_gallery_modal_room_name"]').text
                except:
                    room_name=np.nan
                try:
                    type_room = right_container.find_element(By.CSS_SELECTOR, 'div[data-name-en="privacy"]').text
                except:
                    type_room = np.nan
                try:
                    room_size = right_container.find_element(By.CSS_SELECTOR, 'div[data-name-en="room size"]').text
                
                except:
                    try:
                        room_size = right_container.find_element(By.CSS_SELECTOR, 'div[data-name-en="roomsize"]').text
                    except:
                        room_size = np.nan
                
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="38"]')
                    private_bathroom = 1
                except:
                    private_bathroom = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="93"]')
                    private_pool = 1
                except:
                    private_pool = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="157"]')
                    rooftop_pool = 1
                except:
                    rooftop_pool = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="108"]')
                    sea_view = 1
                except:
                    sea_view = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="3"]')
                    minibar = 1
                except:
                    minibar = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="99"]')
                    barbecue = 1
                except:
                    barbecue = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="79"]')
                    soundproofing = 1
                except:
                    soundproofing = 0 
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="92"]')
                    sauna = 1
                except:
                    sauna = 0 
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="20"]')
                    spa_bath = 1
                except:
                    spa_bath = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="110"]')
                    garden_view = 1
                except:
                    garden_view = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="112"]')
                    mountain_view = 1
                except:
                    mountain_view = 0
                try:
                    right_container.find_element(By.CSS_SELECTOR, 'div[data-facility-id="121"]')
                    city_view = 1
                except:
                    city_view = 0
                try:
                    roomtype_div = right_container.find_element(By.CSS_SELECTOR, ".roomtype-no-margins")
                    # Count bedrooms and living rooms within the room-config element
                    bedroom_elements = roomtype_div.find_elements(By.CSS_SELECTOR, ".bedroom_bed_type")

                    bedroom_count = 0
                    # Loop through each room and count bedrooms and living rooms
                    for room in bedroom_elements:
                        room_type = room.find_element(By.TAG_NAME, 'strong').text
                        print(room_type)
                        if 'Bedroom' in room_type:
                            bedroom_count += 1
                    
                    number_of_bedroom=bedroom_count if bedroom_count!=0 else 1
                except:
                
                    number_of_bedroom=1
            except:
                    room_name = np.nan
                    type_room = np.nan
                    room_size = np.nan
                    private_bathroom = np.nan
                    private_pool = np.nan
                    rooftop_pool = np.nan
                    sea_view = np.nan
                    minibar = np.nan
                    barbecue = np.nan
                    soundproofing = np.nan
                    sauna = np.nan
                    spa_bath = np.nan
                    garden_view = np.nan
                    mountain_view = np.nan
                    city_view = np.nan
                    number_of_bedroom = np.nan

            # Close the modal popup (replace selectors with the appropriate ones)
            try:
                body_element = driver.find_element(By.TAG_NAME, "body")
                body_element.send_keys(Keys.ESCAPE)
                time.sleep(2)
            except:
                print("cannot close dialog")

            time.sleep(1)
        except Exception as e:
            print(e)

    

        # Append all details to properties list
        property = {
            'hotel_id': property_id,
            'name': property_name,
            'price': property_price,
            'price_in_table':price_in_table,
            'distance': property_distance,
            'type_room': type_room,
            'room_size': room_size,
            'hotel_star': hotel_star,
            'sea_view': sea_view,
            'mountain_view': mountain_view,
            'city_view': city_view,
            'room_name': room_name,  # extracted in the try-except block
            'number_of_guests':number_of_guests,
            'private_bathroom': private_bathroom,
            'private_pool': private_pool,
            'rooftop_pool': rooftop_pool,
            'minibar': minibar,
            'barbecue': barbecue,
            'soundproofing': soundproofing,
            'sauna': sauna,
            'spa_bath': spa_bath,
            'garden_view': garden_view,
            'number_of_bedrooms': number_of_bedroom,
            'url': property_url
        }
        properties.append(property)
        property_id += 1
        driver.close()  # Close the current tab
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab

    driver.quit()  # Close the browser
    return properties, reviewer_list

def save_to_csv(properties):
    properties_df = pd.DataFrame(properties)
    properties_df.to_csv("couple_booking_data.csv", index=False)

# URL to scrape
base_url="https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaPQBiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuALfh_mzBsACAdICJGVhYTdkNjZiLTQ5NjEtNDRlMy05YTkwLTRlZDA2NDgxYjQ2Y9gCBeACAQ&sid=20394c3452926236aad651478adb440c&aid=304142&ss=Vung+Tau&ssne=Vung+Tau&ssne_untouched=Vung+Tau&lang=en-gb&src=searchresults&dest_id=-3733750&dest_type=city&checkin=2024-08-14&checkout=2024-08-15&group_adults=5&no_rooms=2&group_children=0&soz=1&lang_changed=1&selected_currency=hotel_currency&nflt=ht_id%3D213"
# Scrape property cards
property_list, reviewer_list = scrape_property_cards(base_url)
save_to_csv(property_list)
