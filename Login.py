import requests
from bs4 import BeautifulSoup
import re

def determine_link_type(link):

    if re.match(r"mailto:", link):
        return "Email"
    elif re.search(r"(facebook|twitter|linkedin|instagram)\.com", link):
        return "Social Media Profile"
    else:
        return "Unknown Link"

def search_in_engine(query, engine):

    if engine == "Bing":
        url = f"https://www.bing.com/search?q={query}"
    elif engine == "DuckDuckGo":
        url = f"https://duckduckgo.com/html/?q={query}"
    elif engine == "Brave":
        url = f"https://search.brave.com/search?q={query}"
    elif engine == "Google":
        url = f"https://www.google.com/search?q={query}"
    else:
        print("Invalid search engine.")
        return
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Data Extraction.
        results = soup.find_all("li", class_="b_algo") if engine == "Bing" else soup.find_all("div", class_="result")
        
        # Group results
        results_by_type = {
            "Email": [],
            "Social Media Profile": [],
            "Unknown Link": [],
        }
        
        # Track unique links.
        unique_links = set()
        
        for result in results:
            title = result.find("h2") if engine == "Bing" else result.find("h2", class_="result__title")
            title_text = title.get_text() if title else "Untitled"
            link = result.find("a")["href"]
            
           
            link_type = determine_link_type(link)
            
            
            if link not in unique_links:
                results_by_type[link_type].append((title_text, link))
                unique_links.add(link)
        
        print(f"Search results in {engine} for '{query}':\n")
        
        
        for link_type, results in results_by_type.items():
            if results:
                print(f"Link Type: {link_type}\n")
                for title_text, link in results:
                    print(f"Title: {title_text}")
                    print(f"Link: {link}\n")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    engines = ["Bing", "DuckDuckGo", "Google", "Brave"]
    
    for engine in engines:
        search_in_engine(query, engine)
