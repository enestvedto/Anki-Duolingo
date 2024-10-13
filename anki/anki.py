import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    try:
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', request_json)))
    except Exception as e:
        raise Exception(f"Failed to invoke Anki API: {e}")

    if len(response) != 2 or 'error' not in response or 'result' not in response:
        raise Exception('Invalid response structure from Anki')

    if response['error'] is not None:
        raise Exception(response['error'])
    
    return response['result']

def create_deck(deck_name: str):
    try:
        invoke('createDeck', deck=deck_name)
        print(f"Deck '{deck_name}' created successfully.")
    except Exception as e:
        print(f"Error creating deck '{deck_name}': {e}")

def delete_decks(deck_names: list):
    try:
        invoke('deleteDecks', decks=deck_names, cardsToo=True)
        print(f"Decks deleted: {deck_names}")
    except Exception as e:
        print(f"Error deleting decks {deck_names}: {e}")

def create_note(deck_name: str, front_content: str, back_content: str):
    # Normalize the content
    front_content = front_content.strip()
    back_content = back_content.strip()

    # Escape the contents for the query
    front_content_escaped = f'"{front_content}"'  # Wrap in quotes
    back_content_escaped = f'"{back_content}"'    # Wrap in quotes

    # Construct the query string for finding notes
    query = f"front:{front_content_escaped} back:{back_content_escaped}"
    existing_note_ids = invoke('findNotes', query=query)

    if existing_note_ids:
        print(f"Note already exists: Front: '{front_content}' | Back: '{back_content}'.")
        return None  # Note already exists

    try:
        invoke('addNote', note={
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": front_content,
                "Back": back_content
            },
            "options": {
                "allowDuplicate": True,  # Prevent duplicates
            }
        })
        print(f"Note created: '{front_content}' | '{back_content}'.")
        return True
    except Exception as e:
        print(f"Error creating note: {e}")
        return False
