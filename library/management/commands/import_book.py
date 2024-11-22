import os
from unicodedata import category

import pandas as pd
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

# Substitua pelo nome correto do app
from library.models import Author, Book, Category, Publisher


class Command(BaseCommand):
    help = 'Importa livros de um arquivo CSV para o banco de dados'

    def add_arguments(self, parser):
        # Argumento opcional para limitar o número de registros
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limita o número de registros a serem processados',
        )

    def handle(self, *args, **kwargs):
        # Caminho do CSV
        # Substitua pelo caminho correto
        csv_path = 'library/management/commands/book_data.csv'

        # Lê o CSV
        try:
            df = pd.read_csv(csv_path, engine='python', sep=',',
                             encoding='utf-8', on_bad_lines='skip')
        except FileNotFoundError:
            self.stderr.write(f"Erro: Arquivo '{csv_path}' não encontrado.")
            return
        except Exception as e:
            self.stderr.write(f"Erro ao ler o arquivo CSV: {e}")
            return

            # Aplica o limite, se especificado
        limit = kwargs['limit']
        if limit is not None:
            df = df.head(limit)  # Seleciona apenas as primeiras `limit` linhas

        for _, row in df.iterrows():
            # Obter ou criar o autor
            author_names = row['authors'].strip().split(',')
            authors = []
            for author_name in author_names:
                author_name = author_name.strip()
                author, _ = Author.objects.get_or_create(name=author_name)
                authors.append(author)
            print(authors)
            # Obter ou criar a categoria
            category_names = row['categories'].strip().split(',')
            categories = []
            for category_name in category_names:
                category_name = category_name.strip()
                category, _ = Category.objects.get_or_create(
                    name=category_name)
                categories.append(category)

            # Obter ou criar a editora
            publisher_name = row['publisher'].strip()
            publisher, _ = Publisher.objects.get_or_create(name=publisher_name)

            # Criar ou atualizar o livro
            book_title = row['title'].strip()
            book_subtitle = row['subtitle']
            total_quantity = 10

            book_year = row['publishedDate']

            book_description = row['description']

            book, created = Book.objects.get_or_create(
                title=book_title,
                subtitle=book_subtitle,
                publication_year=book_year,
                description=book_description,
                total_quantity=total_quantity,
                defaults={
                    'publisher': publisher,
                },
            )

            book.authors.set(authors)  # type: ignore
            book.categories.set(categories)  # type: ignore

            # Se o livro foi criado ou não tem uma imagem de capa, baixar a imagem
            if created or not book.cover:
                cover_url = row['image'].strip()
                if cover_url:
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                        }
                        response = requests.get(
                            cover_url, headers=headers, timeout=10)
                        response.raise_for_status()

                        # Salvar a imagem no campo `cover`
                        # Extrai o nome do arquivo sem parâmetros
                        image_name = os.path.basename(cover_url.split('?')[0])
                        book.cover.save(image_name, ContentFile(
                            response.content), save=True)
                        self.stdout.write(
                            f"Capa salva para o livro: {book.title}")
                    except requests.RequestException as e:
                        self.stderr.write(
                            f"Erro ao baixar a capa do livro '{book.title}': {e}")

            # Salvar o livro
            book.save()
            self.stdout.write(
                f"Livro {'criado' if created else 'atualizado'}: {book.title}")
