import time
from typing import Any, Dict, List

import pandas as pd
import requests


def search_books(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Pesquisa livros na OpenLibrary API.

    Args:
        query: Termo de busca
        limit: Número máximo de resultados

    Returns:
        Lista de livros encontrados
    """
    base_url = "https://openlibrary.org/search.json"
    params = {
        "q": query,
        "limit": limit
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()["docs"]
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")


def get_book_description(work_key: str) -> str:
    """
    Obtém a descrição do livro usando a Works API.

    Args:
        work_key: Chave da obra na OpenLibrary

    Returns:
        Descrição do livro ou string vazia se não encontrada
    """
    if not work_key:
        return ""

    url = f"https://openlibrary.org{work_key}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Tenta diferentes campos onde a descrição pode estar
            description = data.get('description', '')
            if isinstance(description, dict):
                description = description.get('value', '')
            return description if isinstance(description, str) else ''
    except:
        pass
    return ""


def get_book_subtitle(work_key: str) -> str:
    """
    Obtém o subtítulo do livro usando a Works API.

    Args:
        work_key: Chave da obra na OpenLibrary

    Returns:
        Subtítulo do livro ou string vazia se não encontrado
    """
    if not work_key:
        return ""

    url = f"https://openlibrary.org{work_key}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('subtitle', '')
    except:
        pass
    return ""


def get_book_details(books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extrai detalhes relevantes dos livros.

    Args:
        books: Lista de livros da API

    Returns:
        Lista com detalhes formatados dos livros
    """
    books_details = []

    for book in books:
        # Obtém a descrição usando a Works API
        description = get_book_description(book.get('key', ''))
        subtitle = get_book_subtitle(book.get('key', ''))

        # Se não encontrou subtítulo na Works API, tenta pegar do resultado da busca
        if not subtitle and book.get('subtitle'):
            subtitle = book['subtitle']

        # Processa o ano de publicação
        publish_year = ""
        if book.get('first_publish_year'):
            publish_year = str(book['first_publish_year'])
        elif book.get('publish_year'):
            publish_year = str(min(book['publish_year'])) if isinstance(
                book['publish_year'], list) else str(book['publish_year'])

        details = {
            "title": book.get("title", ""),
            "subtitle": subtitle,
            "authors": ', '.join(book.get("author_name", []) if book.get("author_name") else ""),
            "categories": ', '.join(book.get("subject", [])[:5] if book.get("subject") else ""),
            "publisher": book.get("publisher", [""])[0] if book.get("publisher") else "",
            "image": f"https://covers.openlibrary.org/b/id/{book.get('cover_i', '')}-L.jpg" if book.get('cover_i') else "",
            "publishedDate": publish_year,
            # Limita o tamanho da descrição
            "description": description[:500] + "..." if len(description) > 500 else description
        }
        books_details.append(details)
        # Pequena pausa para não sobrecarregar a API
        # Aumentado para dar tempo entre as requisições de descrição
        time.sleep(0.2)

    return books_details


def save_to_csv(books: List[Dict[str, Any]], filename: str = "livros.csv"):
    """
    Salva os detalhes dos livros em um arquivo CSV.

    Args:
        books: Lista com detalhes dos livros
        filename: Nome do arquivo CSV
    """
    df = pd.DataFrame(books)
    df.to_csv(filename, index=False, encoding='utf-8')


def main():
    # Exemplo de uso
    query = "Steve Jobs"  # Pode ser alterado para qualquer termo de busca
    limit = 10  # Número de livros a serem buscados

    try:
        # Busca os livros
        print(f"Buscando livros sobre: {query}")
        books = search_books(query, limit)

        # Obtém os detalhes
        print("Processando detalhes dos livros...")
        books_details = get_book_details(books)

        # Salva em CSV
        filename = "_download/book_data.csv"
        save_to_csv(books_details, filename)
        print(f"Dados salvos com sucesso em: {filename}")

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    main()
