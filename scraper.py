import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = []

# Extraction des infos de chaque livre
for book in soup.find_all('article', class_='product_pod'):
    title = book.h3.a['title'].strip()  
    price = book.find('p', class_='price_color').text.strip() 
    availability = book.find('p', class_='instock availability').text.strip() 
    link = book.h3.a['href']
    full_link = urljoin(url, link)
    
    books.append({
        'Title': title,             
        'Price': price,
        'Availability': availability,
        'URL': full_link
    })

csv_file = "books.csv"
headers = ['Title', 'Price', 'Availability', 'URL'] 

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    
    for book in books:
        writer.writerow(book)

print(f"Les informations des {len(books)} livres ont été stockées dans le fichier '{csv_file}'.")
