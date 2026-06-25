import pytest
from books_collector import BooksCollector


class TestBooksCollector:

    # ==================== ФИКСТУРА ====================

    @pytest.fixture
    def collector(self):
        """Возвращает новый экземпляр BooksCollector для каждого теста."""
        return BooksCollector()

    # ==================== ТЕСТЫ ДЛЯ add_new_book ====================

    @pytest.mark.parametrize("book_name", [
        "Война и мир",
        "А",
        "А" * 40  # максимальная длина
    ])
    def test_add_new_book_valid_name_success(self, collector, book_name):
        """Проверка: книга с валидным названием (1-40 символов) добавляется."""
        collector.add_new_book(book_name)

        assert book_name in collector.books_genre

    def test_add_new_book_valid_name_has_empty_genre(self, collector):
        """Проверка: у добавленной книги жанр пустой."""
        collector.add_new_book("Преступление и наказание")

        assert collector.books_genre["Преступление и наказание"] == ''
        assert collector.get_book_genre("Преступление и наказание") == ''

    @pytest.mark.parametrize("invalid_name", [
        "",  # пустая строка
        "А" * 41  # 41 символ
    ])
    def test_add_new_book_invalid_name_not_added(self, collector, invalid_name):
        """Проверка: книга с невалидным названием не добавляется."""
        collector.add_new_book(invalid_name)

        assert invalid_name not in collector.books_genre

    def test_add_new_book_duplicate_not_added(self, collector):
        """Проверка: повторное добавление той же книги невозможно."""
        collector.add_new_book("Мастер и Маргарита")
        collector.add_new_book("Мастер и Маргарита")

        books = [name for name in collector.books_genre.keys() if name == "Мастер и Маргарита"]
        assert len(books) == 1

    # ==================== ТЕСТЫ ДЛЯ set_book_genre ====================

    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии"
    ])
    def test_set_book_genre_valid_genre_success(self, collector, genre):
        """Проверка: жанр устанавливается, если он есть в списке допустимых."""
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)

        assert collector.get_book_genre("Книга") == genre

    def test_set_book_genre_invalid_genre_not_set(self, collector):
        """Проверка: недопустимый жанр не устанавливается."""
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Роман")

        assert collector.get_book_genre("Книга") == ''

    def test_set_book_genre_for_nonexistent_book_not_set(self, collector):
        """Проверка: жанр не устанавливается для несуществующей книги."""
        collector.set_book_genre("Несуществующая книга", "Фантастика")

        assert "Несуществующая книга" not in collector.books_genre

    # ==================== ТЕСТЫ ДЛЯ get_book_genre ====================

    def test_get_book_genre_existing_book_returns_genre(self, collector):
        """Проверка: метод возвращает жанр существующей книги."""
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Детективы")

        assert collector.get_book_genre("Книга") == "Детективы"

    def test_get_book_genre_nonexistent_book_returns_none(self, collector):
        """Проверка: для несуществующей книги возвращается None."""
        assert collector.get_book_genre("Несуществующая книга") is None

    # ==================== ТЕСТЫ ДЛЯ get_books_with_specific_genre ====================

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Книга1", "Книга3"]),
        ("Детективы", ["Книга2"]),
        ("Ужасы", []),
        ("Комедии", [])
    ])
    def test_get_books_with_specific_genre_returns_correct_books(self, collector, genre, expected_books):
        """Проверка: возвращаются только книги с указанным жанром."""
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Детективы")
        collector.set_book_genre("Книга3", "Фантастика")

        result = collector.get_books_with_specific_genre(genre)

        assert result == expected_books

    def test_get_books_with_specific_genre_empty_dictionary(self, collector):
        """Проверка: при пустом словаре возвращается пустой список."""
        result = collector.get_books_with_specific_genre("Фантастика")

        assert result == []

    def test_get_books_with_specific_genre_invalid_genre_returns_empty(self, collector):
        """Проверка: при запросе недопустимого жанра возвращается пустой список."""
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")

        result = collector.get_books_with_specific_genre("Поэзия")

        assert result == []

    # ==================== ТЕСТЫ ДЛЯ get_books_genre ====================

    def test_get_books_genre_returns_copy_not_reference(self, collector):
        """Проверка: метод возвращает копию словаря, а не ссылку на внутренний."""
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")

        books_genre = collector.get_books_genre()
        books_genre["Новая книга"] = "Комедии"

        assert "Новая книга" not in collector.books_genre

    def test_get_books_genre_returns_correct_dict(self, collector):
        """Проверка: метод возвращает корректный словарь книг."""
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")

        expected = {"Книга1": "Фантастика", "Книга2": ""}

        assert collector.get_books_genre() == expected

    # ==================== ТЕСТЫ ДЛЯ get_books_for_children ====================

    def test_get_books_for_children_includes_safe_genres(self, collector):
        """Проверка: книги с безопасными жанрами попадают в детский список."""
        collector.add_new_book("Комедия")
        collector.add_new_book("Фантастика")
        collector.set_book_genre("Комедия", "Комедии")
        collector.set_book_genre("Фантастика", "Фантастика")

        result = collector.get_books_for_children()

        assert "Комедия" in result
        assert "Фантастика" in result

    def test_get_books_for_children_excludes_age_rating_genres(self, collector):
        """Проверка: книги с возрастным рейтингом (Ужасы, Детективы) отсутствуют."""
        collector.add_new_book("Страшная книга")
        collector.add_new_book("Детектив")
        collector.set_book_genre("Страшная книга", "Ужасы")
        collector.set_book_genre("Детектив", "Детективы")

        result = collector.get_books_for_children()

        assert "Страшная книга" not in result
        assert "Детектив" not in result

    def test_get_books_for_children_includes_only_books_with_genre(self, collector):
        """Проверка: возвращаются только книги, у которых установлен жанр."""
        collector.add_new_book("Книга с жанром")
        collector.add_new_book("Книга без жанра")
        collector.set_book_genre("Книга с жанром", "Фантастика")

        result = collector.get_books_for_children()

        assert "Книга с жанром" in result
        assert "Книга без жанра" not in result

    def test_get_books_for_children_empty_dictionary(self, collector):
        """Проверка: при пустом словаре возвращается пустой список."""
        assert collector.get_books_for_children() == []

    # ==================== ТЕСТЫ ДЛЯ add_book_in_favorites ====================

    def test_add_book_in_favorites_success(self, collector):
        """Проверка: книга добавляется в избранное."""
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")

        assert "Книга" in collector.favorites

    def test_add_book_in_favorites_duplicate_not_added(self, collector):
        """Проверка: повторное добавление книги в избранное невозможно."""
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")

        favorites_count = collector.favorites.count("Книга")
        assert favorites_count == 1

    def test_add_book_in_favorites_nonexistent_book_not_added(self, collector):
        """Проверка: несуществующая книга не добавляется в избранное."""
        collector.add_book_in_favorites("Несуществующая книга")

        assert "Несуществующая книга" not in collector.favorites

    def test_add_book_in_favorites_book_without_genre_can_be_added(self, collector):
        """Проверка: книгу без жанра можно добавить в избранное."""
        collector.add_new_book("Книга без жанра")
        collector.add_book_in_favorites("Книга без жанра")

        assert "Книга без жанра" in collector.favorites

    # ==================== ТЕСТЫ ДЛЯ delete_book_from_favorites ====================

    def test_delete_book_from_favorites_success(self, collector):
        """Проверка: книга успешно удаляется из избранного."""
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")

        assert "Книга" not in collector.favorites

    def test_delete_book_from_favorites_nonexistent_book_no_error(self, collector):
        """Проверка: удаление несуществующей книги не вызывает ошибку."""
        collector.delete_book_from_favorites("Несуществующая книга")

        assert collector.favorites == []

    def test_delete_book_from_favorites_book_not_in_favorites_no_error(self, collector):
        """Проверка: удаление книги, которой нет в избранном, не вызывает ошибку."""
        collector.add_new_book("Книга")
        collector.delete_book_from_favorites("Книга")

        assert collector.favorites == []

    # ==================== ТЕСТЫ ДЛЯ get_list_of_favorites_books ====================

    def test_get_list_of_favorites_books_returns_copy_not_reference(self, collector):
        """Проверка: метод возвращает копию списка, а не ссылку на внутренний."""
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")

        favorites = collector.get_list_of_favorites_books()
        favorites.append("Новая книга")

        assert "Новая книга" not in collector.favorites

    def test_get_list_of_favorites_books_returns_correct_list(self, collector):
        """Проверка: метод возвращает корректный список избранных книг."""
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга3")

        expected = ["Книга1", "Книга3"]

        assert collector.get_list_of_favorites_books() == expected

    def test_get_list_of_favorites_books_empty(self, collector):
        """Проверка: при пустом списке избранных возвращается пустой список."""
        assert collector.get_list_of_favorites_books() == []