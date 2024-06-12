from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import numpy as np  # Import numpy for NaN

# Set up ChromeDriver path
chrome_driver_path = "./chromedriver.exe"  # Update this with your ChromeDriver path

# Configure Chrome options to avoid detection
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Function to close popups
def close_popups():
    try:
        time.sleep(5)
        cancel_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss sign in information."]')
        cancel_button.click()
        print("Pop-up closed.")
        time.sleep(5)
    except Exception as e:
        print(f"No pop-up found or error closing pop-up: ")

# Function to click "Load more results" until all results are loaded
def load_all_results():
    while True:
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)
            load_more_button=driver.find_element(By.XPATH, '//button[span[text()="Load more results"]]')
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Loading")
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
    # load_all_results()

    properties = []

    # Collect all property cards on the page after loading all results
    property_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
    print(f"Found {len(property_cards)} property cards after loading all results.")

    # Extract basic details and visit each property link to extract more details
    for card in property_cards:
        try:
            try:
                property_price = card.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
            except:
                property_price = np.nan

            try:
                property_name = card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
            except:
                property_name = np.nan

            try:
                property_score = card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text
            except:
                property_score = np.nan

            try:
                property_url = card.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_attribute('href')
            except:
                property_url = np.nan

            try:
                property_distance = card.find_element(By.CSS_SELECTOR, 'span[data-testid="distance"]').text
            except:
                property_distance = np.nan
            # Navigate to the property detail page
            driver.execute_script("window.open(arguments[0]);", property_url)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)  # Random sleep to mimic human behavior
            try:
                property_detail=driver.find_element(By.CSS_SELECTOR, 'a[class="hprt-roomtype-link"]')
                property_detail.click()
                time.sleep(1)
                driver.back()
                time.sleep(1)
                try:
                    type_room=driver.find_element(By.CSS_SELECTOR,'div[data-name-en="privacy"]').text
                except:
                    type_room=np.nan
                try:
                    room_size=driver.find_element(By.CSS_SELECTOR,'div[data-name-en="room size"]').text
                except:
                    room_size=np.nan
                try: 
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="108"]')
                    sea_vew=1
                except:
                    sea_view=0
                try: 
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="112"]')
                    mountain_view=1
                except:
                    mountain_view=0
                    
                try: 
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="121"]')
                    city_view=1
                except:
                    city_view=0
                    
                try: 
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="93"]') # private pool
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="157"]')  #rooftop pool
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="159"]')  #pool with a view
                    driver.find_element(By.CSS_SELECTOR,'div[data-facility-id="111"]') #pool view
                    pool=1
                except:
                    pool=0
                    
                driver.find_element(By.CSS_SELECTOR,'button[aria-label="Close dialog"]').click()
            except:
                print("cannot get details")
            try:
                reviews_link = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="Property-Header-Nav-Tab-Trigger-reviews"]')
                reviews_link.click()
                time.sleep(2)  
                try:
                    couple_option=driver.find_element(By.CSS_SELECTOR,'option[data-key="COUPLES"]')
                    couple_option.click()
                    review_cards=driver.find_elements(By.CSS_SELECTOR,'div[data-testid="review-card"]')
                    review_count=0
                    for card in review_cards:
                        review_count+=1
                        review_room_name=card.find_element(By.CSS_SELECTOR,'span[data-testid="review-room-name"]').text
                        review_stay_date=card.find_element(By.CSS_SELECTOR,'span[data-testid="review-stay-date"]').text
                        
                        if(review_room_name!=property_name):
                            continue
                        couple_review_score=card.find_element(By.CSS_SELECTOR,'div[data-testid="review-score"]').text
                    driver.find_element(By.CSS_SELECTOR,'div[class="sliding-panel-widget-close-button"]')
                except:
                    print("No couples")
            except:
                reviews = np.nan

            


          

            # Append all details to properties list
            properties.append({
                'name': property_name,
                'price': property_price,
                'score': property_score,
                'url': property_url,
                'distance': property_distance,
           
            })
            print(properties)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        except Exception as e:
            print(f"Error extracting property details:")

    driver.quit()
    return properties

# URL to scrape
base_url = "https://www.booking.com/searchresults.en-gb.html?ss=Vung+Tau&ssne=Vung+Tau&ssne_untouched=Vung+Tau&label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEJuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKqt--yBsACAdICJGUxMDY1MmNiLTJhMjMtNDg1NC04MzQ3LTRmM2ExYTQ5YmQ5ONgCBuACAQ&sid=20394c3452926236aad651478adb440c&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-3733750&dest_type=city&checkin=2024-06-18&checkout=2024-06-19&group_adults=2&no_rooms=1&group_children=0"

# Scrape property cards
property_list = scrape_property_cards(base_url)


