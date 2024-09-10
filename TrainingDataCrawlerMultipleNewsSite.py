#Importing Necessary Libraries
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Creating a options
options = Options()
#Updating preferences for for faster execution
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--headless")
driver = webdriver.Chrome(options = options)


#Function to craw the data from kathmandu post
def getDataFromKathmanduPost():
    # Opening the file to store our precious data
    file = open('TrainingDataNews.csv', 'w')
    # Adding a header to the CSV file
    file.write('news,label\n')

    # The URL of Kathmandu Post's national news page
    url = 'https://kathmandupost.com/national'
    driver.get(url)  # Let’s navigate to the page and see what’s cooking

    allnews = []

    # Using a counter to press the “load more” button repeatedly
    # This site uses lazy loading, so more headlines appear when we click “load more”
    for counter in range(1, 20):  # Adjust the range as needed based on how many headlines you want
        try:
            # Wait until the “load more” button is visible
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'load-more-btn'))
            )
            # Click the “load more” button to fetch additional headlines
            element.click()
            print(f'Clicked “load more” {counter} times')
        except Exception as e:
            # If something goes wrong, print the error message
            print(e)
        # Wait for the page to load more content
        time.sleep(2)

    try:
        # Locate the news section on the page
        newBlock = driver.find_element(By.ID, 'news-list')
        # Find all blocks containing more news
        morenewsBlocks = newBlock.find_elements(By.CLASS_NAME, "block--morenews")
        print(f'Found {len(morenewsBlocks)} blocks of more news')

        for morenewsBlock in morenewsBlocks:
            # Extract news headlines from each block
            newsheadings = morenewsBlock.find_elements(By.CLASS_NAME, "article-image")
            for newsHeading in newsheadings:
                # Get the headline text and clean it up for our CSV file
                heading = newsHeading.find_element(By.TAG_NAME, 'h3').text
                newsHeadingText = heading.split("\n")[0].replace(",", "|")
                allnews.append(newsHeadingText)
                # Write the headline to the CSV file
                file.write(f'{newsHeadingText}\n')
    except Exception as e:
        # Handle any errors that occur during extraction
        print(e)
        print('Error in finding news')

    print(f'Total {len(allnews)} headlines collected')
    file.close()


#Getting the data from online khabar another news site
# this site has pagination but it's different from kathmandu post
def getDataFromOnlineKhabar():
    allOnlineNews = []
    fileOnline = open('TrainingDataNews.csv', 'a')  # Append mode to add more data
    fileOnline.write('news,label\n')

    # Loop through the pages to collect headlines
    for counter in range(1, 10):  # Adjust the range based on the number of pages
        url = f'https://english.onlinekhabar.com/category/social/page/{counter}'
        driver.get(url)  # Navigate to the page
        try:
            # Wait until the news elements are present
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'listical-news-big'))
            )
        except Exception as e:
            # Handle any issues if the page doesn’t load correctly
            print(e)

        # Find and extract news headlines
        newsheadings = element.find_elements(By.CLASS_NAME, "ok-post-contents")
        for newsHeading in newsheadings:
            newsHeadingText = newsHeading.text.split("\n")[0].replace(",", "|")
            allOnlineNews.append(newsHeadingText)
            fileOnline.write(f'{newsHeadingText}\n')

    print(f'Total {len(allOnlineNews)} headlines collected')
    fileOnline.close()


getDataFromKathmanduPost()
getDataFromOnlineKhabar()