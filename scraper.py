import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

category_url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"
base_url = "https://books.toscrape.com/catalogue/category/books/science_22/"
page_num = 1
books = []

while True:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les infos sur chaque livre
    for book in soup.find_all('article', class_='product_pod'):
        book_url = urljoin(base_url, book.h3.a['href'])
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        book_data = {
            'product_page_url': book_url,
            'universal_product_code (upc)': book_soup.find('th', text='UPC').find_next_sibling('td').text,
            'title': book_soup.find('h1').text,
            'price_including_tax': book_soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
            'price_excluding_tax': book_soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
            'number_available': book_soup.find('th', text='Availability').find_next_sibling('td').text,
            'product_description': book_soup.find('meta', attrs={'name': 'description'})['content'].strip(),
            'category': book_soup.find('ul', class_='breadcrumb').find_all('a')[-1].text,
            'review_rating': book_soup.find('p', class_='star-rating')['class'][1],
            'image_url': urljoin(book_url, book_soup.find('img')['src'])
        }

        books.append(book_data)

    # Vérifier s'il y a une page suivante
    next_page = soup.find('li', class_='next')
    if next_page:
        next_url = next_page.a['href']
        category_url = urljoin(base_url, next_url)
        page_num += 1
    else:
        break

csv_file = "category_books.csv"
headers = list(books[0].keys())

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for book in books:
        writer.writerow(book)

print(f"Les informations de {len(books)} livres ont été stockées dans le fichier '{csv_file}'.")
