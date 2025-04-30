import requests

def get_firecrawl_data(firecrawl_token):
    """
    Fetches data from the Firecrawl API.
    """
    # Define the Firecrawl scrape endpoint
    url = "https://api.firecrawl.dev/scrape"

    # Define the payload for the API request
    payload = {
        "url": "https://wazuh.com/partners/find-a-partner/",
        "formats": ["markdown"],
        "onlyMainContent": True,
        "includeTags": [],
        "excludeTags": [],
        "headers": {},
        "waitFor": 0,
        "mobile": False,
        "skipTlsVerification": False,
        "timeout": 30000,
        "jsonOptions": {
            "schema": {},
            "systemPrompt": "",
            "prompt": ""
        },
        "actions": [],
        "location": {
            "country": "US",
            "languages": ["en-US"]
        },
        "removeBase64Images": True,
        "blockAds": True,
        "proxy": "basic",
        "changeTrackingOptions": {
            "mode": "git-diff",
            "schema": {},
            "prompt": ""
        }
    }

    # Define the headers for the API request
    headers = {
        "Authorization": f"Bearer {firecrawl_token}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching data from Firecrawl API:", response.status_code, response.text)
        return None

def ask_ollama(content):
    """
    Sends the scraped content to the Ollama API and asks a question.
    """
    # Define the Ollama API endpoint
    ollama_url = "http://localhost:11434/api/generate"

    # Define the payload for the Ollama API request
    ollama_payload = {
        "model": "llama2",  # Replace with the appropriate model name if needed
        "prompt": f"The following is the content of a webpage:\n\n{content}\n\nWho are the partners identified on this page?"
    }

    # Make the API request to Ollama
    response = requests.post(ollama_url, json=ollama_payload)

    if response.status_code == 200:
        return response.json().get("response", "No response from Ollama.")
    else:
        print("Error communicating with Ollama API:", response.status_code, response.text)
        return None

def main():
    # Prompt the user for their Firecrawl token
    firecrawl_token = input("Enter your Firecrawl token: ")

    # Get data from Firecrawl
    firecrawl_data = get_firecrawl_data(firecrawl_token)

    if firecrawl_data:
        # Send the data to Ollama and ask the question
        ollama_response = ask_ollama(firecrawl_data)

        # Print the response from Ollama
        print("Ollama's response:", ollama_response)

if __name__ == "__main__":
    main()

