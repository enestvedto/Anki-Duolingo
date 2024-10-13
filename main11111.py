import json
import time
import urllib.request

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### These are the functions to interact with Anki

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# Input the name of the deck as a string.
def createDeck(deckName: str):
    invoke('createDeck', deck=deckName)

# Input the name of the decks as a comma seperated string list.
def deleteDecks(deckNames: list):
    result= invoke('deleteDecks', decks = deckNames, cardsToo = True)

# Input the name of the deck as a string, the front of the card as a string,
# the back of the card as a string, and the tags as a comma seperated string 
# list where [''] is for no tags
def createNote(deckName: str, frontContent: str, backContent: str):
    # Construct the query string for finding notes
    query = f"front:{frontContent} back:{backContent}"

    # Fetch existing note IDs
    existing_note_ids = invoke('findNotes', query=query)

    # If any notes were found, check their fields
    if existing_note_ids:
        print(f"Note already exists with front: {frontContent} and back: {backContent}.")
        return None  # Note already exists

    # If no duplicates exist, create the note
    invoke('addNote', note={
        "deckName": deckName,
        "modelName": "Basic",
        "fields": {
            "Front": frontContent,
            "Back": backContent
        },
        "options": {
            "allowDuplicate": True,
        }
    })

    print(f"Note created successfully with front: {frontContent} and back: {backContent}.")
    return True  # Return a success indication


### These are the functions to interact with Duolingo

if __name__ == '__main__':
    # Instantiate Chrome options
    options = uc.ChromeOptions()
    options.headless = False  # Set to True for headless mode

    # Instantiate a Chrome browser with the options
    driver = uc.Chrome(
        use_subprocess=False,
        options=options,
    )

    try:
        # Visit the target URL
        driver.get("https://www.duolingo.com")
        time.sleep(1)

        # Click "I have an account"
        driver.find_element(By.CSS_SELECTOR, '[data-test="have-account"]').click()
        time.sleep(1)

        # Fill in the username field
        username = driver.find_element(By.CSS_SELECTOR, '[data-test="email-input"]')
        username.send_keys("")

        # Fill in the password field
        password = driver.find_element(By.CSS_SELECTOR, '[data-test="password-input"]')
        password.send_keys("")
        time.sleep(1)

        # Submit the login form
        driver.find_element(By.CSS_SELECTOR, '[data-test="register-button"]').click()
        time.sleep(3)

        # Navigate to the practice page
        driver.find_element(By.CSS_SELECTOR, '[data-test="practice-hub-nav"]').click()
        time.sleep(2)

        # Navigate to the words page
        driver.find_element(By.CSS_SELECTOR, '[src="https://d35aaqx5ub95lt.cloudfront.net/images/practiceHub/9d1604d8e8f843b492862b21a8a4e822.svg"]').click()
        time.sleep(2)

        # Load all of the words!
        image_selector = '[src="https://d35aaqx5ub95lt.cloudfront.net/images/practiceHub/5d6e001cb745302aecc569f09fb7d669.svg"]' 
        
        while True:
            try:
                # Wait for the image to be present
                image = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, image_selector))
                )
                # Click the image
                image.click()
                # time.sleep(1)  # Optional wait before the next click
            except Exception:
                # Break the loop only if the image is not found
                print("Image no longer exists; exiting the click loop.")
                break

        # Now let's get all of the words!
        words = driver.find_elements(By.CSS_SELECTOR, 'li._2g-qq')  # Fixed the CSS selector

        # Make the deck on ANKI
        createDeck("Automated Duolingo Vocab")

        for word in words:
            try:
                # Access the first <h3> child which is the Spanish content
                spanish_content = word.find_element(By.TAG_NAME, 'h3')

                # Access the first <p> child which is the English translation
                english_translation = word.find_element(By.TAG_NAME, 'p')

                createNote("Automated Duolingo Vocab", english_translation.text, spanish_content.text)

            except Exception as e:
                print("Error accessing Spanish or English word content:", e)

    finally:
        # Close the browser
        driver.quit()