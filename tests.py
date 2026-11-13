import pytest
from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
 # проверяем добавление книг с разными названиями:
    # обычное название, короткое название и название ровно в 40 символов добавляются,
    # пустое и длиннее 40 символов — нет
    @pytest.mark.parametrize(
        'name, expected_result',
        [
            ('Гордость и предубеждение и зомби', True),
            ('Оно', True),
            ('А' * 40, True),
            ('', False),
            ('А' * 41, False),
            ('А' * 100, False),
        ]
    )
    def test_add_new_book_add_books_with_different_names(self, name, expected_result):
        collector = BooksCollector()

        collector.add_new_book(name)

        # добавилась ли книга — сравниваем с ожидаемым результатом
        assert (name in collector.get_books_genre()) == expected_result

    # одну и ту же книгу можно добавить только один раз
    def test_add_new_book_same_book_added_once(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Гарри Поттер')

        assert len(collector.get_books_genre()) == 1

    # метод get_books_genre возвращает словарь со всеми добавленными книгами
    def test_get_books_genre_returns_all_added_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Оно')

        assert collector.get_books_genre() == {'Гарри Поттер': '', 'Оно': ''}

    
    # у добавленной книги ещё нет жанра — хранится пустая строка
    def test_get_book_genre_new_book_has_empty_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Мартин Иден')

        assert collector.get_book_genre('Мартин Иден') == ''

    # жанр из списка genre устанавливается книге
    @pytest.mark.parametrize(
        'name, genre',
        [
            ('Гарри Поттер', 'Фантастика'),
            ('Оно', 'Ужасы'),
            ('Шерлок Холмс', 'Детективы'),
            ('Том и Джерри', 'Мультфильмы'),
        ]
    )
    def test_set_book_genre_sets_genre(self, name, genre):
        collector = BooksCollector()

        collector.add_new_book(name)
        collector.set_book_genre(name, genre)

        assert collector.get_book_genre(name) == genre

    # жанр вне списка genre не устанавливается — жанр книги остаётся пустым
    @pytest.mark.parametrize('genre', ['Роман', 'Фэнтези', ''])
    def test_set_book_genre_unknown_genre_ignored(self, genre):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', genre)

        assert collector.get_book_genre('Гарри Поттер') == ''

    # get_books_with_specific_genre возвращает только книги с нужным жанром
    def test_get_books_with_specific_genre_returns_right_books(self):
        collector = BooksCollector()

        collector.add_new_book('Оно')
        collector.add_new_book('Мгла')
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Мгла', 'Ужасы')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')

        assert collector.get_books_with_specific_genre('Ужасы') == ['Оно', 'Мгла']

    # get_books_for_children не включает книги с жанрами, у которых есть возрастной рейтинг
    def test_get_books_for_children_excludes_age_rated(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')

        assert collector.get_books_for_children() == ['Гарри Поттер']

     # метод get_list_of_favorites_books возвращает только книги из избранного
    def test_get_list_of_favorites_books_returns_favorites(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Гарри Поттер')

        assert collector.get_list_of_favorites_books() == ['Гарри Поттер']
    
    # книгу можно добавить в избранное, повторно добавить нельзя
    def test_add_book_in_favorites_no_duplicates(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')

        assert collector.get_list_of_favorites_books() == ['Гарри Поттер']

    # книгу можно удалить из избранного, после удаления список пуст
    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()

        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.delete_book_from_favorites('Гарри Поттер')

        assert collector.get_list_of_favorites_books() == []

    # книгу, которой нет в books_genre, нельзя добавить в избранное
    def test_add_book_not_in_books_genre_not_added_to_favorites(self):
        collector = BooksCollector()

        collector.add_book_in_favorites('Нет такой книги')

        assert collector.get_list_of_favorites_books() == []