import requests
from bs4 import BeautifulSoup

def get_html(url):
    """Fetches and parses HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')  # Use 'content' for raw bytes
        return soup  # Return the BeautifulSoup object directly
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_text_from_elements(soup, element_name, element_class):
    """Extracts text from elements with specified name and class."""
    elements = soup.find_all(element_name, class_=element_class)
    text_content = '\n'.join(element.get_text(separator='\n', strip=True) for element in elements)
    return text_content

def main():
    url = 'https://www.gadgets360.com/mobile-recharge-plans/airtel-prepaid'
    soup = get_html(url)

    if soup:
        div_class = '_rpln _flx'
        extracted_text = extract_text_from_elements(soup, 'div', div_class)

        if extracted_text:
            print("\nExtracted Text:")
            print(extracted_text)
        else:
            print(f"No elements found with class '{div_class}'.")
    
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()
