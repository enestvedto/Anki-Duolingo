# Anki-Duolingo

Anki-Duolingo enables users to combine the benefits of [Duolingo](https://www.duolingo.com/) and [Anki](https://apps.ankiweb.net/) to accelerate language learning. This tool makes use of [Anki-Connect](https://git.foosoft.net/alex/anki-connect) to communicate with your Anki application.

## Installation

The installation process is similar to other Anki plugins and can be accomplished in three steps:

1.  Open the `Install Add-on` dialog by selecting `Tools` | `Add-ons` | `Get Add-ons...` in Anki.
2.  Input [2055492159](https://ankiweb.net/shared/info/2055492159) into the text box labeled `Code` and press the `OK` button to proceed.
3.  Restart Anki when prompted to do so in order to complete the installation of Anki-Connect.

Anki must be kept running in the background in order for other applications to be able to use Anki-Connect. You can verify that Anki-Connect is running at any time by accessing `localhost:8765` in your browser. If the server is running, you will see the message `Anki-Connect` displayed in your browser window.

## Configuration

1.  Install necessary python packages by running `pip install -r requirements.txt`
2.  Replace `email` and `password` fields in [credentials.cfg](./credentials.cfg) with your Duolingo credentials.
