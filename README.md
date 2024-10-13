# Anki-Duolingo

Anki-Duolingo enables users to combine the benefits of [Duolingo](https://www.duolingo.com/) and [Anki](https://apps.ankiweb.net/) to accelerate language learning. This tool makes use of [Anki-Connect](https://git.foosoft.net/alex/anki-connect) to communicate with your Anki application.

Currently, the main feature of this tool is to create and update an Anki deck with all vocab someone has unlocked on Duolingo. Future plans can be found below in the TODO sections.

## Installation

The installation process is similar to other Anki plugins and can be accomplished in three steps:

1.  Open the `Install Add-on` dialog by selecting `Tools` | `Add-ons` | `Get Add-ons...` in Anki.
2.  Input [2055492159](https://ankiweb.net/shared/info/2055492159) into the text box labeled `Code` and press the `OK` button to proceed.
3.  Restart Anki when prompted to do so in order to complete the installation of Anki-Connect.

Anki must be kept running in the background in order for other applications to be able to use Anki-Connect. You can verify that Anki-Connect is running at any time by accessing `localhost:8765` in your browser. If the server is running, you will see the message `Anki-Connect` displayed in your browser window.

## Configuration

NOTE: Make sure you have git and python installed. At this point you should also have Anki desktop installed and the plugin configured also.

1.  Install necessary python packages by running `pip install -r requirements.txt`
2.  Replace `email` and `password` fields in [config.cfg](./config.cfg) with your Duolingo credentials.
3.  Replace `deckname` field in [config.cfg](./config.cfg) with your desired deck name.
4.  Run `python3 main.py` and watch as your deck is automatically created in a matter of seconds/minutes!
    Note: This can be run over and over and it will not create duplicated cards that exactly match both the front and back of another card so you can keep updating your deck as you learn new words on Duolingo.

### TODO:

1.  Make the script schedulable so your deck automatically stays up to date!

### Maybe TODO:

1.  Include the audio clips for the target language.
2.  Add tagging for Anki cards so you can study sub decks based on certain tags (ex. "foods", "animals", etc.)
