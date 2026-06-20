import pytest
from books_collector import BooksCollector


class TestBooksCollector:
    
    # ==================== ТЕСТЫ ДЛЯ add_new_book ====================
    
    @pytest.mark.parametrize("book_name", [
        "Война и мир",
        "А",
        "А" * 40  # максимальная длина
    ])
    def test_add_new_book_valid_name_success(self, book_name):
        """Проверка: книга с валидным названием (1-40 символов) добавляется"""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ''
    
    @pytest.mark.parametrize("invalid_name", [
        "",  # пустая строка
        "А" * 41  # 41 символ
    ])
    def test_add_new_book_invalid_name_not_added(self, invalid_name):
        """Проверка: книга с невалидным названием не добавляется"""
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        
        assert invalid_name not in collector.books_genre
    
    def test_add_new_book_duplicate_not_added(self):
        """Проверка: повторное добавление той же книги невозможно"""
        collector = BooksCollector()
        collector.add_new_book("Мастер и Маргарита")
        collector.add_new_book("Мастер и Маргарита")
        
        # Книга должна быть только одна
        books = [name for name in collector.books_genre.keys() if name == "Мастер и Маргарита"]
        assert len(books) == 1
    
    def test_add_new_book_with_empty_genre(self):
        """Проверка: у добавленной книги нет жанра (пустая строка)"""
        collector = BooksCollector()
        collector.add_new_book("Преступление и наказание")
        
        assert collector.books_genre["Преступление и наказание"] == ''
        assert collector.get_book_genre("Преступление и наказание") == ''
    
    # ==================== ТЕСТЫ ДЛЯ set_book_genre ====================
    
    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии"
    ])
    def test_set_book_genre_valid_genre_success(self, genre):
        """Проверка: жанр устанавливается, если он есть в списке допустимых"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        
        assert collector.get_book_genre("Книга") == genre
    
    def test_set_book_genre_invalid_genre_not_set(self):
        """Проверка: недопустимый жанр не устанавливается"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Роман")
        
        assert collector.get_book_genre("Книга") == ''
    
    def test_set_book_genre_for_nonexistent_book_not_set(self):
        """Проверка: жанр не устанавливается для несуществующей книги"""
        collector = BooksCollector()
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        
        assert "Несуществующая книга" not in collector.books_genre
    
    # ==================== ТЕСТЫ ДЛЯ get_book_genre ====================
    
    def test_get_book_genre_existing_book_returns_genre(self):
        """Проверка: метод возвращает жанр существующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Детективы")
        
        assert collector.get_book_genre("Книга") == "Детективы"
    
    def test_get_book_genre_nonexistent_book_returns_none(self):
        """Проверка: для несуществующей книги возвращается None"""
        collector = BooksCollector()
        
        assert collector.get_book_genre("Несуществующая книга") is None
    
    # ==================== ТЕСТЫ ДЛЯ get_books_with_specific_genre ====================
    
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Книга1", "Книга3"]),
        ("Детективы", ["Книга2"]),
        ("Ужасы", []),
        ("Комедии", [])
    ])
    def test_get_books_with_specific_genre_returns_correct_books(self, genre, expected_books):
        """Проверка: возвращаются только книги с указанным жанром"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Детективы")
        collector.set_book_genre("Книга3", "Фантастика")
        
        result = collector.get_books_with_specific_genre(genre)
        
        assert result == expected_books
    
    def test_get_books_with_specific_genre_empty_dictionary(self):
        """Проверка: при пустом словаре возвращается пустой список"""
        collector = BooksCollector()
        result = collector.get_books_with_specific_genre("Фантастика")
        
        assert result == []
    
    def test_get_books_with_specific_genre_invalid_genre_returns_empty(self):
        """Проверка: при запросе недопустимого жанра возвращается пустой список"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        
        result = collector.get_books_with_specific_genre("Поэзия")
        
        assert result == []
    
    # ==================== ТЕСТЫ ДЛЯ get_books_genre ====================
    
    def test_get_books_genre_returns_copy_not_reference(self):
        """Проверка: метод возвращает копию словаря, а не ссылку на внутренний"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        
        books_genre = collector.get_books_genre()
        # Изменяем полученный словарь
        books_genre["Новая книга"] = "Комедии"
        
        # Внутренний словарь не должен измениться
        assert "Новая книга" not in collector.books_genre
    
    def test_get_books_genre_returns_correct_dict(self):
        """Проверка: метод возвращает корректный словарь книг"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        
        expected = {"Книга1": "Фантастика", "Книга2": ""}
        
        assert collector.get_books_genre() == expected
    
    # ==================== ТЕСТЫ ДЛЯ get_books_for_children ====================
    
    def test_get_books_for_children_excludes_age_rating_genres(self):
        """Проверка: книги с возрастным рейтингом (Ужасы, Детективы) отсутствуют"""
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.add_new_book("Страшная книга")
        collector.add_new_book("Детектив")
        collector.set_book_genre("Детская книга", "Комедии")
        collector.set_book_genre("Страшная книга", "Ужасы")
        collector.set_book_genre("Детектив", "Детективы")
        
        result = collector.get_books_for_children()
        
        assert "Детская книга" in result
        assert "Страшная книга" not in result
        assert "Детектив" not in result
    
    def test_get_books_for_children_includes_only_books_with_genre(self):
        """Проверка: возвращаются только книги, у которых установлен жанр"""
        collector = BooksCollector()
        collector.add_new_book("Книга с жанром")
        collector.add_new_book("Книга без жанра")
        collector.set_book_genre("Книга с жанром", "Фантастика")
        
        result = collector.get_books_for_children()
        
        assert "Книга с жанром" in result
        assert "Книга без жанра" not in result
    
    def test_get_books_for_children_empty_dictionary(self):
        """Проверка: при пустом словаре возвращается пустой список"""
        collector = BooksCollector()
        
        assert collector.get_books_for_children() == []
    
    # ==================== ТЕСТЫ ДЛЯ add_book_in_favorites ====================
    
    def test_add_book_in_favorites_success(self):
        """Проверка: книга добавляется в избранное"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        
        assert "Книга" in collector.favorites
    
    def test_add_book_in_favorites_duplicate_not_added(self):
        """Проверка: повторное добавление книги в избранное невозможно"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        
        # В списке избранных должна быть только одна запись
        favorites_count = collector.favorites.count("Книга")
        assert favorites_count == 1
    
    def test_add_book_in_favorites_nonexistent_book_not_added(self):
        """Проверка: несуществующая книга не добавляется в избранное"""
        collector = BooksCollector()
        collector.add_book_in_favorites("Несуществующая книга")
        
        assert "Несуществующая книга" not in collector.favorites
    
    def test_add_book_in_favorites_book_without_genre_can_be_added(self):
        """Проверка: книгу без жанра можно добавить в избранное"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        collector.add_book_in_favorites("Книга без жанра")
        
        assert "Книга без жанра" in collector.favorites
    
    # ==================== ТЕСТЫ ДЛЯ delete_book_from_favorites ====================
    
    def test_delete_book_from_favorites_success(self):
        """Проверка: книга успешно удаляется из избранного"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        
        assert "Книга" not in collector.favorites
    
    def test_delete_book_from_favorites_nonexistent_book_no_error(self):
        """Проверка: удаление несуществующей книги не вызывает ошибку"""
        collector = BooksCollector()
        
        # Метод должен отработать без ошибок
        collector.delete_book_from_favorites("Несуществующая книга")
        
        assert collector.favorites == []
    
    def test_delete_book_from_favorites_book_not_in_favorites_no_error(self):
        """Проверка: удаление книги, которой нет в избранном, не вызывает ошибку"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        
        # Книга есть в словаре, но не в избранном
        collector.delete_book_from_favorites("Книга")
        
        assert collector.favorites == []
    
    # ==================== ТЕСТЫ ДЛЯ get_list_of_favorites_books ====================
    
    def test_get_list_of_favorites_books_returns_copy_not_reference(self):
        """Проверка: метод возвращает копию списка, а не ссылку на внутренний"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        
        favorites = collector.get_list_of_favorites_books()
        # Изменяем полученный список
        favorites.append("Новая книга")
        
        # Внутренний список не должен измениться
        assert "Новая книга" not in collector.favorites
    
    def test_get_list_of_favorites_books_returns_correct_list(self):
        """Проверка: метод возвращает корректный список избранных книг"""
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга3")
        
        expected = ["Книга1", "Книга3"]
        
        assert collector.get_list_of_favorites_books() == expected
    
    def test_get_list_of_favorites_books_empty(self):
        """Проверка: при пустом списке избранных возвращается пустой список"""
        collector = BooksCollector()
        
        assert collector.get_list_of_favorites_books() == []
    
    # ==================== КОМПЛЕКСНЫЕ ТЕСТЫ ====================
    
    def test_full_workflow(self):
        """Проверка: полный рабочий процесс с несколькими методами"""
        collector = BooksCollector()
        
        # Добавляем книги
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        
        # Устанавливаем жанры
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Ужасы")
        collector.set_book_genre("Книга3", "Комедии")
        
        # Проверяем жанры
        assert collector.get_book_genre("Книга1") == "Фантастика"
        assert collector.get_book_genre("Книга2") == "Ужасы"
        
        # Проверяем книги для детей (должны быть Книга1 и Книга3, но не Книга2)
        children_books = collector.get_books_for_children()
        assert "Книга1" in children_books
        assert "Книга2" not in children_books
        assert "Книга3" in children_books
        
        # Добавляем в избранное
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        
        # Проверяем избранное
        favorites = collector.get_list_of_favorites_books()
        assert "Книга1" in favorites
        assert "Книга2" in favorites
        assert "Книга3" not in favorites
        
        # Удаляем из избранного
        collector.delete_book_from_favorites("Книга1")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга1" not in favorites
        assert "Книга2" in favorites
    
    def test_book_without_genre_not_in_children_books(self):
        """Проверка: книга без жанра не попадает в список детских книг"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        collector.add_new_book("Книга с жанром")
        collector.set_book_genre("Книга с жанром", "Фантастика")
        
        children_books = collector.get_books_for_children()
        
        assert "Книга с жанром" in children_books
        assert "Книга без жанра" not in children_books

        


        

    







