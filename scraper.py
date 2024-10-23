import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(book_url)
soup = BeautifulSoup(response.text, 'html.parser')


# Extraire les infos du livre
book_data = {
    'product_page_url': book_url,
    'universal_product_code (upc)': soup.find('th', text='UPC').find_next_sibling('td').text,
    'title': soup.find('h1').text,
    'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
    'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
    'number_available': soup.find('th', text='Availability').find_next_sibling('td').text,
    'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
    'category': soup.find('ul', class_='breadcrumb').find_all('a')[-1].text,
    'review_rating': soup.find('p', class_='star-rating')['class'][1],
    'image_url': urljoin(book_url, soup.find('img')['src'])
}

csv_file = "book_data.csv"
headers = list(book_data.keys())

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerow(book_data)

print(f"Les informations du livre ont été stockées dans le fichier '{csv_file}'.")
