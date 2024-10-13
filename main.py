from anki.anki import create_deck, create_note
from duolingo.duolingo import DuolingoBot
from selenium.webdriver.common.by import By

def main():
    duolingo_bot = DuolingoBot()
    
    try:
        duolingo_bot.login()
        duolingo_bot.navigate_to_words()
        duolingo_bot.load_full_vocab()

        # Extract words
        words = duolingo_bot.extract_words()
        create_deck("Automated Duolingo Vocab")

        for word in words:
            try:
                spanish_content = word.find_element(By.TAG_NAME, 'h3')
                english_translation = word.find_element(By.TAG_NAME, 'p')
                create_note("Automated Duolingo Vocab", english_translation.text, spanish_content.text)
            except Exception as e:
                print("Error accessing word content:", e)

    finally:
        duolingo_bot.close()

if __name__ == '__main__':
    main()
