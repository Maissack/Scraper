import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = []

# Extraction des infos de chaque livre
for book in soup.find_all('article', class_='product_pod'):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    availability = book.find('p', class_='instock availability').text.strip()
    link = book.h3.a['href']
    
    # Urljoin pour avoir un lien complet
    full_link = urljoin(url, link)
    
    books.append({
        'title': title,
        'price': price,
        'availability': availability,
        'url': full_link
    })

# Aesthetics
print(f"{'Title':<40} {'Price':<10} {'Availability':<15} {'URL'}")
print("="*100)

for book in books:
    print(f"{book['title']:<40} {book['price']:<10} {book['availability']:<15} {book['url']}")
