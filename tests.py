import pytest
from books_collector import BooksCollector


class TestBooksCollector:
    
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
        "1",
        "Книга с пробелами",
        "Special@#$%^&*()",
    ])
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
    
    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии",
    ])
    def test_set_book_genre_all_valid_genres(self, empty_collector, genre):
        """Все допустимые жанры успешно устанавливаются"""
        empty_collector.add_new_book("Тестовая книга")
        empty_collector.set_book_genre("Тестовая книга", genre)
        assert empty_collector.get_book_genre("Тестовая книга") == genre
    
    @pytest.mark.parametrize("invalid_genre", [
        "Роман",
        "Поэзия",
        "Триллер",
        "Вестерн",
        "",
        None,
        "Документалистика",
    ])
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