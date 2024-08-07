from selenium import webdriver
import csv
import time

# Setup the Chrome driver
driver = webdriver.Chrome()

# Function to fetch scores from a given SBD
def fetch_scores(sbd):
    url = f"https://diemthi.vnexpress.net/index/detail/sbd/{sbd}/year/2024"
    driver.get(url)
    time.sleep(2)  # Wait for page to load

    # Find and store the scores
    scores = {}
    scores['Số báo danh'] = sbd
    table_rows = driver.find_elements_by_css_selector('.o-detail-thisinh__diemthi table tbody tr')
    for row in table_rows:
        columns = row.find_elements_by_tag_name('td')
        subject = columns[0].text.strip()
        score = columns[1].text.strip()
        scores[subject] = score
    return scores

# Open CSV file to write
with open('candidate_scores.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Số báo danh", "Toán", "Ngữ văn", "Ngoại ngữ", "Vật lý", "Hóa học", "Sinh học"])

    # Loop through each candidate number
    for sbd in range(2021756, 2021857):
        sbd = f"0{sbd}"  # Format the SBD correctly
        try:
            score_data = fetch_scores(sbd)
            writer.writerow(score_data)
        except Exception as e:
            print(f"Failed to fetch data for SBD {sbd}: {str(e)}")

# Close the driver
driver.quit()
