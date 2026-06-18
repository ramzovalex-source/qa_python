import pytest
from books_collector import BooksCollector


class TestBooksCollector:
<<<<<<< HEAD
    
    @pytest.fixture
    def empty_collector(self):
        return BooksCollector()
    
    @pytest.fixture
    def collector_with_books(self):
        """Фикстура с подготовленными тестовыми данными"""
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Властелин колец")
        collector.add_new_book("Шерлок Холмс")
        
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.set_book_genre("Властелин колец", "Фантастика")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        return collector
    
    # ========== ТЕСТЫ ДЛЯ add_new_book ==========
    
    @pytest.mark.parametrize("valid_name", [
        "A",
        "B" * 40,
        "Книга",
        "Очень длинное название книги из тридцати символов",
=======

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
>>>>>>> b2ab2311adddd02f8fea2159d99578c87f0fed9e
        "1",
        "Книга с пробелами",
        "Special@#$%^&*()",
    ])
<<<<<<< HEAD
    def test_add_new_book_valid_names(self, empty_collector, valid_name):
        """Все валидные названия добавляются в коллекцию"""
        empty_collector.add_new_book(valid_name)
        assert valid_name in empty_collector.get_books_genre()
    
    @pytest.mark.parametrize("invalid_name", [
        "",
        "C" * 41,
        "D" * 50,
        "E" * 100,
        "Очень длинное название книги которое превышает сорок символов",
    ])
    def test_add_new_book_invalid_names(self, empty_collector, invalid_name):
        """Все невалидные названия не добавляются в коллекцию"""
        empty_collector.add_new_book(invalid_name)
        assert invalid_name not in empty_collector.get_books_genre()
    
    def test_add_new_book_duplicate_not_added(self, empty_collector):
        """Одну и ту же книгу нельзя добавить дважды"""
        empty_collector.add_new_book("Война и мир")
        empty_collector.add_new_book("Война и мир")
        assert len(empty_collector.get_books_genre()) == 1
    
    # ========== ТЕСТЫ ДЛЯ set_book_genre ==========
=======
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
>>>>>>> b2ab2311adddd02f8fea2159d99578c87f0fed9e
    
    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии",
    ])
<<<<<<< HEAD
    def test_set_book_genre_all_valid_genres(self, empty_collector, genre):
        """Все допустимые жанры успешно устанавливаются"""
        empty_collector.add_new_book("Тестовая книга")
        empty_collector.set_book_genre("Тестовая книга", genre)
        assert empty_collector.get_book_genre("Тестовая книга") == genre
=======
    def test_set_book_genre_all_valid_genres(self, genre):
        """Параметризованный тест установки всех допустимых жанров"""
        collector = BooksCollector()
        collector.add_new_book("Тестовая книга")
        collector.set_book_genre("Тестовая книга", genre)
        assert collector.get_book_genre("Тестовая книга") == genre
>>>>>>> b2ab2311adddd02f8fea2159d99578c87f0fed9e
    
    @pytest.mark.parametrize("invalid_genre", [
        "Роман",
        "Поэзия",
        "Триллер",
        "Вестерн",
        "",
        None,
        "Документалистика",
    ])
<<<<<<< HEAD
    def test_set_book_genre_invalid_genres(self, empty_collector, invalid_genre):
        """Все недопустимые жанры не устанавливаются"""
        empty_collector.add_new_book("Тестовая книга")
        empty_collector.set_book_genre("Тестовая книга", invalid_genre)
        assert empty_collector.get_book_genre("Тестовая книга") == ""
    
    def test_set_book_genre_book_not_exist(self, empty_collector):
        """Попытка установить жанр несуществующей книге"""
        empty_collector.add_new_book("Существующая книга")
        empty_collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert empty_collector.get_book_genre("Несуществующая книга") is None
    
    def test_set_book_genre_change_genre(self, empty_collector):
        """Изменение жанра у существующей книги"""
        empty_collector.add_new_book("Книга")
        empty_collector.set_book_genre("Книга", "Фантастика")
        empty_collector.set_book_genre("Книга", "Комедии")
        assert empty_collector.get_book_genre("Книга") == "Комедии"
    
    # ========== ТЕСТЫ ДЛЯ get_book_genre ==========
    
    def test_get_book_genre_existing_book(self, empty_collector):
        """Получение жанра существующей книги"""
        empty_collector.add_new_book("Книга")
        empty_collector.set_book_genre("Книга", "Детективы")
        assert empty_collector.get_book_genre("Книга") == "Детективы"
    
    def test_get_book_genre_not_existing_book(self, empty_collector):
        """Получение жанра несуществующей книги возвращает None"""
        assert empty_collector.get_book_genre("Неизвестная книга") is None
    
    def test_get_book_genre_book_without_genre(self, empty_collector):
        """Получение жанра книги без установленного жанра"""
        empty_collector.add_new_book("Книга без жанра")
        assert empty_collector.get_book_genre("Книга без жанра") == ""
    
    # ========== ТЕСТЫ ДЛЯ get_books_with_specific_genre ==========
    
    @pytest.mark.parametrize("genre", [
        "Ужасы",
        "Комедии",
        "Мультфильмы",
        "Роман",
    ])
    def test_get_books_with_specific_genre_returns_empty_for_absent_genres(self, collector_with_books, genre):
        """Для жанров, которых нет в коллекции, возвращается пустой список"""
        result = collector_with_books.get_books_with_specific_genre(genre)
        assert result == []
    
    def test_get_books_with_specific_genre_fantasy(self, collector_with_books):
        """Поиск книг жанра 'Фантастика'"""
        result = collector_with_books.get_books_with_specific_genre("Фантастика")
        assert result == ["Гарри Поттер", "Властелин колец"]
    
    def test_get_books_with_specific_genre_detectives(self, collector_with_books):
        """Поиск книг жанра 'Детективы'"""
        result = collector_with_books.get_books_with_specific_genre("Детективы")
        assert result == ["Шерлок Холмс"]
    
    def test_get_books_with_specific_genre_invalid(self, collector_with_books):
        """Поиск по несуществующему жанру"""
        result = collector_with_books.get_books_with_specific_genre("Роман")
        assert result == []
    
    # ========== ТЕСТЫ ДЛЯ get_books_genre ==========
    
    def test_get_books_genre_returns_correct_dict(self, empty_collector):
        """Метод возвращает правильный словарь books_genre"""
        empty_collector.add_new_book("Книга1")
        empty_collector.add_new_book("Книга2")
        empty_collector.set_book_genre("Книга1", "Фантастика")
        
        result = empty_collector.get_books_genre()
        expected = {"Книга1": "Фантастика", "Книга2": ""}
        assert result == expected
    
    def test_get_books_genre_empty_dict(self, empty_collector):
        """Метод возвращает пустой словарь, если книги не добавлены"""
        result = empty_collector.get_books_genre()
        assert result == {}
        assert len(result) == 0
    
    def test_get_books_genre_returns_dict_type(self, empty_collector):
        """Метод возвращает объект типа dict"""
        empty_collector.add_new_book("Книга")
        result = empty_collector.get_books_genre()
        assert isinstance(result, dict)
    
    def test_get_books_genre_does_not_return_reference(self, empty_collector):
        """Метод возвращает копию словаря, а не ссылку на оригинал"""
        empty_collector.add_new_book("Книга")
        
        books_genre = empty_collector.get_books_genre()
        books_genre["Новая_книга"] = "Фантастика"
        books_genre["Книга"] = "Измененный_жанр"
        
        original = empty_collector.get_books_genre()
        assert "Новая_книга" not in original
        assert original["Книга"] == ""
    
    def test_get_books_genre_without_genres(self, empty_collector):
        """Проверка словаря после добавления книг без жанров"""
        books = ["Война и мир", "Анна Каренина", "Евгений Онегин"]
        for book in books:
            empty_collector.add_new_book(book)
        
        result = empty_collector.get_books_genre()
        expected = {book: "" for book in books}
        assert result == expected
    
    def test_get_books_genre_with_genres(self, empty_collector):
        """Проверка словаря после добавления книг с жанрами"""
        books_data = {
            "Преступление и наказание": "Детективы",
            "Мастер и Маргарита": "Фантастика",
            "Гарри Поттер": "Фантастика"
        }
        
        for book, genre in books_data.items():
            empty_collector.add_new_book(book)
            empty_collector.set_book_genre(book, genre)
        
        result = empty_collector.get_books_genre()
        assert result == books_data
    
    def test_get_books_genre_after_deleting_book_from_favorites(self, empty_collector):
        """Удаление книги из избранного не влияет на books_genre"""
        empty_collector.add_new_book("Книга")
        empty_collector.add_book_in_favorites("Книга")
        empty_collector.delete_book_from_favorites("Книга")
        
        result = empty_collector.get_books_genre()
        assert "Книга" in result
        assert len(result) == 1
    
    def test_get_books_genre_after_setting_genre(self, empty_collector):
        """Проверка обновления словаря после установки жанра"""
        empty_collector.add_new_book("Книга")
        empty_collector.set_book_genre("Книга", "Комедии")
        
        result = empty_collector.get_books_genre()
        assert result["Книга"] == "Комедии"
    
    # ========== ТЕСТЫ ДЛЯ get_books_for_children ==========
    
    @pytest.mark.parametrize("safe_genre", [
        "Фантастика",
        "Мультфильмы",
        "Комедии",
    ])
    def test_get_books_for_children_includes_safe_genres(self, empty_collector, safe_genre):
        """Все безопасные жанры попадают в детский список"""
        book_name = f"Книга жанра {safe_genre}"
        empty_collector.add_new_book(book_name)
        empty_collector.set_book_genre(book_name, safe_genre)
        
        children_books = empty_collector.get_books_for_children()
        assert book_name in children_books
    
    @pytest.mark.parametrize("unsafe_genre", [
        "Ужасы",
        "Детективы",
    ])
    def test_get_books_for_children_excludes_unsafe_genres(self, empty_collector, unsafe_genre):
        """Все опасные жанры не попадают в детский список"""
        book_name = f"Книга жанра {unsafe_genre}"
        empty_collector.add_new_book(book_name)
        empty_collector.set_book_genre(book_name, unsafe_genre)
        
        children_books = empty_collector.get_books_for_children()
        assert book_name not in children_books
    
    def test_get_books_for_children_book_without_genre_excluded(self, empty_collector):
        """Книга без жанра не попадает в детский список"""
        empty_collector.add_new_book("Книга без жанра")
        children_books = empty_collector.get_books_for_children()
        assert "Книга без жанра" not in children_books
    
    def test_get_books_for_children_empty_collection(self, empty_collector):
        """Пустая коллекция - пустой детский список"""
        assert empty_collector.get_books_for_children() == []
    
    # ========== ТЕСТЫ ДЛЯ add_book_in_favorites ==========
    
    @pytest.mark.parametrize("book_name", [
        "Книга1",
        "Книга2",
        "Любая книга",
        "Книга с пробелами",
    ])
    def test_add_book_in_favorites_existing_books(self, empty_collector, book_name):
        """Любые существующие книги успешно добавляются в избранное"""
        empty_collector.add_new_book(book_name)
        empty_collector.add_book_in_favorites(book_name)
        assert book_name in empty_collector.get_list_of_favorites_books()
    
    def test_add_book_in_favorites_nonexistent_book_not_added(self, empty_collector):
        """Несуществующая книга не добавляется в избранное"""
        empty_collector.add_book_in_favorites("Несуществующая книга")
        assert empty_collector.get_list_of_favorites_books() == []
    
    def test_add_book_in_favorites_duplicate_not_added(self, empty_collector):
        """Повторное добавление книги в избранное не создает дубликат"""
        empty_collector.add_new_book("Книга")
        empty_collector.add_book_in_favorites("Книга")
        empty_collector.add_book_in_favorites("Книга")
        assert empty_collector.get_list_of_favorites_books() == ["Книга"]
        assert len(empty_collector.get_list_of_favorites_books()) == 1
    
    def test_add_book_in_favorites_multiple_books(self, empty_collector):
        """Добавление нескольких книг в избранное"""
        books = ["Книга1", "Книга2", "Книга3"]
        for book in books:
            empty_collector.add_new_book(book)
            empty_collector.add_book_in_favorites(book)
        
        assert empty_collector.get_list_of_favorites_books() == books
    
    # ========== ТЕСТЫ ДЛЯ delete_book_from_favorites ==========
    
    @pytest.mark.parametrize("book_name", [
        "Книга1",
        "Книга2",
        "Любая книга",
    ])
    def test_delete_book_from_favorites_existing_books(self, empty_collector, book_name):
        """Любые существующие книги успешно удаляются из избранного"""
        empty_collector.add_new_book(book_name)
        empty_collector.add_book_in_favorites(book_name)
        empty_collector.delete_book_from_favorites(book_name)
        assert book_name not in empty_collector.get_list_of_favorites_books()
    
    def test_delete_book_from_favorites_single_book(self, empty_collector):
        """Удаление единственной книги из избранного"""
        empty_collector.add_new_book("Книга")
        empty_collector.add_book_in_favorites("Книга")
        empty_collector.delete_book_from_favorites("Книга")
        assert empty_collector.get_list_of_favorites_books() == []
    
    def test_delete_book_from_favorites_multiple_books(self, empty_collector):
        """Удаление одной книги из нескольких в избранном"""
        books = ["Книга1", "Книга2", "Книга3"]
        for book in books:
            empty_collector.add_new_book(book)
            empty_collector.add_book_in_favorites(book)
        
        empty_collector.delete_book_from_favorites("Книга2")
        assert empty_collector.get_list_of_favorites_books() == ["Книга1", "Книга3"]
    
    def test_delete_book_from_favorites_nonexistent_book(self, empty_collector):
        """Удаление несуществующей книги не меняет список избранного"""
        books = ["Книга1", "Книга2"]
        for book in books:
            empty_collector.add_new_book(book)
            empty_collector.add_book_in_favorites(book)
        
        empty_collector.delete_book_from_favorites("Несуществующая книга")
        assert empty_collector.get_list_of_favorites_books() == books
    
    def test_delete_book_from_favorites_empty_favorites(self, empty_collector):
        """Удаление из пустого списка избранного не вызывает ошибок"""
        empty_collector.delete_book_from_favorites("Любая книга")
        assert empty_collector.get_list_of_favorites_books() == []
    
    # ========== ТЕСТЫ ДЛЯ get_list_of_favorites_books ==========
    
    def test_get_list_of_favorites_books_empty(self, empty_collector):
        """Получение пустого списка избранного"""
        assert empty_collector.get_list_of_favorites_books() == []
    
    def test_get_list_of_favorites_books_with_books(self, empty_collector):
        """Получение списка избранного с книгами"""
        empty_collector.add_new_book("Книга1")
        empty_collector.add_new_book("Книга2")
        empty_collector.add_book_in_favorites("Книга1")
        empty_collector.add_book_in_favorites("Книга2")
        
        favorites = empty_collector.get_list_of_favorites_books()
        assert favorites == ["Книга1", "Книга2"]
    
    def test_get_list_of_favorites_books_returns_copy(self, empty_collector):
        """Метод возвращает копию списка (изменение не влияет на оригинал)"""
        empty_collector.add_new_book("Книга")
        empty_collector.add_book_in_favorites("Книга")
        
        favorites = empty_collector.get_list_of_favorites_books()
        favorites.append("Новая книга")
        
        assert "Новая книга" not in empty_collector.get_list_of_favorites_books()
        assert len(empty_collector.get_list_of_favorites_books()) == 1
    
    def test_get_list_of_favorites_books_returns_list_type(self, empty_collector):
        """Метод возвращает объект типа list"""
        empty_collector.add_new_book("Книга")
        empty_collector.add_book_in_favorites("Книга")
        
        result = empty_collector.get_list_of_favorites_books()
        assert isinstance(result, list)
=======
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

        


        

    







