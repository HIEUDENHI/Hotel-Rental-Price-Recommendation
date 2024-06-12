from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import numpy as np
import pandas as pd
import os
# Set up ChromeDriver path
# chrome_driver_path = "./chromedriver.exe"  # Update this with your ChromeDriver path

# Configure Chrome options to avoid detection
options = Options()
options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")  # Added for extra security

service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
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
        print(f"No pop-up found or error closing pop-up: {e}")

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
            property_score = card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"] div').text.strip().split('\n')[0]
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
        time.sleep(2)  # Random sleep to mimic human behavior

        # Initialize additional property details
        
        type_room = np.nan
        room_size = np.nan
        sea_view = 0
        mountain_view = 0
        city_view = 0
        pool = 0

        total_review_score = 0

        try:
            # Try to open the room details popup
            try:
                property_detail = driver.find_element(By.CSS_SELECTOR, 'a[class="hprt-roomtype-link"]')
                property_detail.click()
            except:
                print("Cannot click detail popup")
            time.sleep(1)
            
            
            # Extract details from the property page (after clicking the popup)
            try:
                room_name_element = driver.find_element(By.ID, "hp_rt_room_gallery_modal_room_name")
                room_name = room_name_element.text
            except:
                room_name = ""
            try:
                type_room = driver.find_element(By.CSS_SELECTOR, 'div[data-name-en="privacy"]').text
            except:
                type_room = np.nan
            try:
                room_size = driver.find_element(By.CSS_SELECTOR, 'div[data-name-en="room size"]').text
            except:
                room_size = np.nan
            try:
                driver.find_element(By.CSS_SELECTOR, 'div[data-facility-id="108"]')
                sea_view = 1
            except:
                sea_view = 0
            try:
                driver.find_element(By.CSS_SELECTOR, 'div[data-facility-id="112"]')
                mountain_view = 1
            except:
                mountain_view = 0
            try:
                driver.find_element(By.CSS_SELECTOR, 'div[data-facility-id="121"]')
                city_view = 1
            except:
                city_view = 0

            pool_elements = [
                'div[data-facility-id="93"]',   # private pool
                'div[data-facility-id="157"]',  # rooftop pool
                'div[data-facility-id="159"]',  # pool with a view
                'div[data-facility-id="111"]'   # pool view
            ]

            for selector in pool_elements:
                try:
                    driver.find_element(By.CSS_SELECTOR, selector)
                    pool = 1
                    break
                except:
                    continue

            # Close the modal popup (replace selectors with the appropriate ones)
            try:
                body_element = driver.find_element(By.TAG_NAME, "body")
                body_element.send_keys(Keys.ESCAPE)
                time.sleep(2)
            except:
                print("cannot close dialog")
                    
        
            time.sleep(1)
        except:
            print("Cannot get details")
        count=0
        try:
            # Navigate to the reviews section
            reviews_link = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="Property-Header-Nav-Tab-Trigger-reviews"]')
            reviews_link.click()
            time.sleep(2)

            # Filter reviews by "Couples"
            try:
                couple_option = driver.find_element(By.CSS_SELECTOR, 'option[data-key="COUPLES"]')
                couple_option.click()
                time.sleep(5)
                
                # Scroll to load more reviews

                while True:
                    review_cards_section = driver.find_element(By.ID, "reviewCardsSection")
                    
                    # Extract review data
                    review_cards = review_cards_section.find_elements(By.CSS_SELECTOR, "div[data-testid='review-cards'] > div")
                    for card in review_cards:
                        count+=1
                        try:
                            reviewer_tmp = card.find_element(By.CSS_SELECTOR,'div[data-testid="review-avatar"]').text.split("\n")
                            if len(reviewer_tmp) == 3:
                                reviewer_name = reviewer_tmp[1]
                                reviewer_country = reviewer_tmp[2]
                            else:
                                reviewer_name = reviewer_tmp[0]
                                reviewer_country = reviewer_tmp[1]
                           
                        except:
                            print("cannot get name")
                        
                        try:
                            review_room_name = card.find_element(By.CSS_SELECTOR, 'span[data-testid="review-room-name"]').text
                            # if review_room_name != room_name:
                            #     continue
                        except:
                            continue
                        
                        try:
                            review_stay_date = card.find_element(By.CSS_SELECTOR, 'span[data-testid="review-stay-date"]').text
                            
                        except:
                            review_stay_date=np.nan
                            print("No review date")
                        
                        try:
                            review_num_night = card.find_element(By.CSS_SELECTOR, 'span[data-testid="review-num-nights"]').text
                        except:
                            review_num_night=np.nan
                            print("No review date")
                        
                        try:
                            review_score = card.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text.split("\n")[0]
                            total_review_score += float(review_score)
                        except:
                            print("No review score")
                        reviewer={
                            'reviewer_name':reviewer_name,
                            'reviewer_country': reviewer_country,
                            'review_stay_date':review_stay_date,
                            'review_num_night':review_num_night,
                            'review_score':review_score
                        }
                        reviewer_list.append(reviewer)
                            
                    # Click the "Next page" button (if available)
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next page"]'))
                        )
                        next_button.click()
                        
                        # Add a random sleep interval to mimic human behavior
                        time.sleep(random.uniform(2, 5))
                    except Exception as e:
                        print(f"Cannot find the 'Next page' button: {e}")
                        break
                
                # Close the reviews section
                driver.find_element(By.CSS_SELECTOR, 'div[class="sliding-panel-widget-close-button"]').click()
            except:
                print("No couples reviews found")
        except:
            print("Cannot get review")

        # Append all details to properties list
        property = {
            'name': property_name,
            'price': property_price,
            'score': property_score,
            'url': property_url,
            'distance': property_distance,
            'type_room': type_room,
            'room_size': room_size,
            'sea_view': sea_view,
            'mountain_view': mountain_view,
            'city_view': city_view,
            'pool': pool,
            'total_review_score': total_review_score/count
        }
        properties.append(property)
        driver.close()  # Close the current tab
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab
        

    driver.quit()  # Close the browser
    return properties, reviewer_list

def save_to_csv(properties, reviewers):
    properties_df = pd.DataFrame(properties)
    reviewers_df = pd.DataFrame(reviewers)
    properties_df.to_csv("couple_booking_data", index=False)
    reviewers_df.to_csv(f"review_couple_booking", index=False)

# URL to scrape
base_url = "https://www.booking.com/searchresults.en-gb.html?ss=Vung+Tau&ssne=Vung+Tau&ssne_untouched=Vung+Tau&label=gen173nr-1FCAEoggI46AdIM1gEaPQBiAEBmAEJuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKqt--yBsACAdICJGUxMDY1MmNiLTJhMjMtNDg1NC04MzQ3LTRmM2ExYTQ5YmQ5ONgCBuACAQ&sid=20394c3452926236aad651478adb440c&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-3733750&dest_type=city&checkin=2024-06-18&checkout=2024-06-19&group_adults=2&no_rooms=1&group_children=0"

# Scrape property cards
property_list,reviewer_list = scrape_property_cards(base_url)
save_to_csv(property_list,reviewer_list)
