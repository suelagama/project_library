import csv

import pandas as pd

search_term = input('Informe o termo a ser pesquisado: ')

url = f'https://www.googleapis.com/books/v1/volumes/?q={
    search_term.replace(' ', '-')}'

df = pd.read_json(url)
# display(df['items'][1]['volumeInfo']['publishedDate'])

with open('_download/book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'subtitle', 'authors', 'publisher',
                  'publishedDate', 'description', 'categories', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for item in df['items']:
        if 'publishedDate' not in item['volumeInfo']:
            item['volumeInfo']['publishedDate'] = 0
        item['volumeInfo']['year'] = pd.to_datetime(
            item['volumeInfo']['publishedDate']).strftime('%Y')
        volume_info = item['volumeInfo']
        image = volume_info.get('imageLinks', {})
        # isbn = volume_info['industryIdentifiers'][0]
        try:
            writer.writerow({
                # 'isbn': isbn.get('identifier', ''),
                'title': volume_info.get('title', ''),
                'subtitle': volume_info.get('subtitle', ''),
                'authors': ', '.join(volume_info.get('authors', [])),
                'publisher': volume_info.get('publisher', ''),
                'publishedDate': volume_info.get('year', ''),
                'description': volume_info.get('description', ''),
                'categories': ', '.join(volume_info.get('categories', [])),
                'image': image.get('thumbnail', '')
            })

        except KeyError:
            print(f"Skipping item due to missing keys: {item}")

print("CSV file 'book_data.csv' created successfully.")
