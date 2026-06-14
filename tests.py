import pytest
from books_collector import BooksCollector


class TestBooksCollector:

    # ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ ГРАНИЧНЫХ ЗНАЧЕНИЙ ==========
    
    @pytest.mark.parametrize("name, expected", [
        ("A", True),                    # 1 символ - минимальная граница (валидно)
        ("B" * 40, True),              # 40 символов - максимальная граница (валидно)
        ("", False),                   # 0 символов - невалидно
        ("C" * 41, False),             # 41 символ - невалидно
        ("D" * 100, False),            # 100 символов - невалидно
    ])
    def test_add_new_book_boundary_values(self, name, expected):
        """Параметризованный тест граничных значений длины названия книги"""
        collector = BooksCollector()
        collector.add_new_book(name)
        
        if expected:
            assert name in collector.get_books_genre()
        else:
            assert name not in collector.get_books_genre()
    
    @pytest.mark.parametrize("valid_name", [
        "Книга",
        "Очень длинное название книги из тридцати символов",
        "A" * 40,
        "1",
        "Книга с пробелами",
        "Special@#$%^&*()",
    ])
    def test_add_new_book_valid_names(self, valid_name):
        """Параметризованный тест валидных названий книг разной длины"""
        collector = BooksCollector()
        collector.add_new_book(valid_name)
        assert valid_name in collector.get_books_genre()
    
    @pytest.mark.parametrize("invalid_name", [
        "",
        "A" * 41,
        "B" * 50,
        "C" * 100,
        "Очень длинное название книги которое превышает сорок символов и поэтому не должно добавиться",
    ])
    def test_add_new_book_invalid_names(self, invalid_name):
        """Параметризованный тест невалидных названий книг"""
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.get_books_genre()
    
    # ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ ЖАНРОВ ==========
    
    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии",
    ])
    def test_set_book_genre_all_valid_genres(self, genre):
        """Параметризованный тест установки всех допустимых жанров"""
        collector = BooksCollector()
        collector.add_new_book("Тестовая книга")
        collector.set_book_genre("Тестовая книга", genre)
        assert collector.get_book_genre("Тестовая книга") == genre
    
    @pytest.mark.parametrize("invalid_genre", [
        "Роман",
        "Поэзия",
        "Триллер",
        "Вестерн",
        "",
        None,
        "Документалистика",
    ])
    def test_set_book_genre_invalid_genres(self, invalid_genre):
        """Параметризованный тест попытки установить недопустимые жанры"""
        collector = BooksCollector()
        collector.add_new_book("Тестовая книга")
        collector.set_book_genre("Тестовая книга", invalid_genre)
        assert collector.get_book_genre("Тестовая книга") == ""
    
    # ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ ПОИСКА КНИГ ПО ЖАНРУ ==========
    
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Гарри Поттер", "Властелин колец"]),
        ("Детективы", ["Шерлок Холмс"]),
        ("Ужасы", []),
        ("Комедии", []),
        ("Мультфильмы", []),
    ])
    def test_get_books_with_specific_genre_parametrized(self, genre, expected_books):
        """Параметризованный тест поиска книг по разным жанрам"""
        collector = BooksCollector()
        
        # Добавляем тестовые книги
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Властелин колец")
        collector.add_new_book("Шерлок Холмс")
        
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.set_book_genre("Властелин колец", "Фантастика")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected_books
    
    # ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ ДЕТСКИХ КНИГ ==========
    
    @pytest.mark.parametrize("genre, should_be_in_children", [
        ("Фантастика", True),
        ("Мультфильмы", True),
        ("Комедии", True),
        ("Ужасы", False),
        ("Детективы", False),
    ])
    def test_get_books_for_children_by_genre(self, genre, should_be_in_children):
        """Параметризованный тест определения детских книг по жанру"""
        collector = BooksCollector()
        book_name = f"Книга жанра {genre}"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        
        if should_be_in_children:
            assert book_name in children_books
        else:
            assert book_name not in children_books
    
    # ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ ИЗБРАННОГО ==========
    
    @pytest.mark.parametrize("books_to_add, books_to_favorite, expected_favorites", [
        (["Книга1", "Книга2"], ["Книга1"], ["Книга1"]),
        (["Книга1", "Книга2", "Книга3"], ["Книга1", "Книга3"], ["Книга1", "Книга3"]),
        (["Книга1"], ["Книга2"], []),
        ([], ["Книга1"], []),
    ])
    def test_add_book_in_favorites_parametrized(self, books_to_add, books_to_favorite, expected_favorites):
        """Параметризованный тест добавления книг в избранное"""
        collector = BooksCollector()
        
        # Добавляем книги
        for book in books_to_add:
            collector.add_new_book(book)
        
        # Добавляем в избранное
        for book in books_to_favorite:
            collector.add_book_in_favorites(book)
        
        assert collector.get_list_of_favorites_books() == expected_favorites
    
    @pytest.mark.parametrize("favorites_before, book_to_delete, favorites_after", [
        (["Книга1"], "Книга1", []),
        (["Книга1", "Книга2"], "Книга1", ["Книга2"]),
        (["Книга1", "Книга2", "Книга3"], "Книга2", ["Книга1", "Книга3"]),
        ([], "Книга1", []),
        (["Книга1"], "Книга2", ["Книга1"]),
    ])
    def test_delete_book_from_favorites_parametrized(self, favorites_before, book_to_delete, favorites_after):
        """Параметризованный тест удаления книг из избранного"""
        collector = BooksCollector()
        
        # Добавляем книги в словарь
        for book in favorites_before:
            collector.add_new_book(book)
        
        # Добавляем в избранное
        for book in favorites_before:
            collector.add_book_in_favorites(book)
        
        # Удаляем книгу
        collector.delete_book_from_favorites(book_to_delete)
        
        assert collector.get_list_of_favorites_books() == favorites_after

    # ========== ОСТАЛЬНЫЕ ТЕСТЫ ==========
    
    def test_add_new_book_duplicate_not_added(self):
        """Одну и ту же книгу нельзя добавить дважды"""
        collector = BooksCollector()
        collector.add_new_book("Война и мир")
        collector.add_new_book("Война и мир")
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_book_not_exist(self):
        """Попытка установить жанр несуществующей книге"""
        collector = BooksCollector()
        collector.add_new_book("Существующая книга")
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_set_book_genre_change_genre(self):
        """Изменение жанра у существующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        collector.set_book_genre("Книга", "Комедии")
        assert collector.get_book_genre("Книга") == "Комедии"

    def test_get_book_genre_existing_book(self):
        """Получение жанра существующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Детективы")
        assert collector.get_book_genre("Книга") == "Детективы"

    def test_get_book_genre_not_existing_book(self):
        """Получение жанра несуществующей книги возвращает None"""
        collector = BooksCollector()
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_get_book_genre_book_without_genre(self):
        """Получение жанра книги без установленного жанра"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        assert collector.get_book_genre("Книга без жанра") == ""

    # ========== Тесты для get_books_genre ==========

    def test_get_books_genre_returns_correct_dict(self):
        """Метод возвращает правильный словарь books_genre"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        
        result = collector.get_books_genre()
        expected = {"Книга1": "Фантастика", "Книга2": ""}
        assert result == expected

    def test_get_books_genre_empty_dict(self):
        """Метод возвращает пустой словарь, если книги не добавлены"""
        collector = BooksCollector()
        result = collector.get_books_genre()
        assert result == {}
        assert len(result) == 0

    def test_get_books_genre_returns_dict_type(self):
        """Метод возвращает объект типа dict"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        result = collector.get_books_genre()
        assert isinstance(result, dict)

    def test_get_books_genre_does_not_return_reference(self):
        """Метод возвращает копию словаря, а не ссылку на оригинал"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        
        books_genre = collector.get_books_genre()
        books_genre["Новая_книга"] = "Фантастика"
        books_genre["Книга"] = "Измененный_жанр"
        
        original = collector.get_books_genre()
        assert "Новая_книга" not in original
        assert original["Книга"] == ""

    def test_get_books_genre_after_adding_multiple_books(self):
        """Проверка словаря после добавления нескольких книг"""
        collector = BooksCollector()
        books_data = {
            "Война и мир": "",
            "Преступление и наказание": "Детективы",
            "Мастер и Маргарита": "Фантастика"
        }
        
        for book, genre in books_data.items():
            collector.add_new_book(book)
            if genre:
                collector.set_book_genre(book, genre)
        
        result = collector.get_books_genre()
        assert result == books_data

    def test_get_books_genre_after_deleting_book(self):
        """Проверка, что удаление книги из избранного не влияет на books_genre"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        
        result = collector.get_books_genre()
        assert "Книга" in result
        assert len(result) == 1

    def test_get_books_genre_after_setting_genre(self):
        """Проверка обновления словаря после установки жанра"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Комедии")
        
        result = collector.get_books_genre()
        assert result["Книга"] == "Комедии"

    def test_get_books_for_children_book_without_genre_excluded(self):
        """Книга без жанра не попадает в детский список"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        children_books = collector.get_books_for_children()
        assert "Книга без жанра" not in children_books

    def test_get_books_for_children_empty_collection(self):
        """Пустая коллекция - пустой детский список"""
        collector = BooksCollector()
        assert collector.get_books_for_children() == []

    def test_add_book_in_favorites_book_not_exist(self):
        """Попытка добавить несуществующую книгу в избранное"""
        collector = BooksCollector()
        collector.add_book_in_favorites("Несуществующая книга")
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_duplicate_not_added(self):
        """Повторное добавление книги в избранное не создает дубликат"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        assert collector.get_list_of_favorites_books().count("Книга") == 1
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites_book_not_in_favorites(self):
        """Попытка удалить книгу, которой нет в избранном"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.delete_book_from_favorites("Книга")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_empty_favorites(self):
        """Удаление из пустого списка избранного"""
        collector = BooksCollector()
        collector.delete_book_from_favorites("Любая книга")
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_empty(self):
        """Получение пустого списка избранного"""
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_with_books(self):
        """Получение списка избранного с книгами"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга1", "Книга2"]

    def test_get_list_of_favorites_books_returns_copy(self):
        """Метод возвращает копию списка (изменение не влияет на оригинал)"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        
        favorites = collector.get_list_of_favorites_books()
        favorites.append("Новая книга")
        
        assert "Новая книга" not in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_get_list_of_favorites_books_returns_list_type(self):
        """Метод возвращает объект типа list"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        
        result = collector.get_list_of_favorites_books()
        assert isinstance(result, list)

    # ========== Комплексный тест ==========

    def test_full_workflow(self):
        """Полный сценарий работы с коллекцией"""
        collector = BooksCollector()
        
        collector.add_new_book("Мастер и Маргарита")
        collector.add_new_book("Властелин колец")
        collector.add_new_book("Сияние")
        
        collector.set_book_genre("Мастер и Маргарита", "Фантастика")
        collector.set_book_genre("Властелин колец", "Фантастика")
        collector.set_book_genre("Сияние", "Ужасы")
        
        all_books = collector.get_books_genre()
        assert len(all_books) == 3
        
        children_books = collector.get_books_for_children()
        assert "Мастер и Маргарита" in children_books
        assert "Властелин колец" in children_books
        assert "Сияние" not in children_books
        
        fantasy_books = collector.get_books_with_specific_genre("Фантастика")
        assert len(fantasy_books) == 2
        
        collector.add_book_in_favorites("Мастер и Маргарита")
        collector.add_book_in_favorites("Сияние")
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        
        collector.delete_book_from_favorites("Сияние")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1
        assert "Мастер и Маргарита" in favorites

        