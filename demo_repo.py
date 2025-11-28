import os
import django
from datetime import date
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore_project.settings")
django.setup()

def main():
    from store.repositories.unit_of_work import UnitOfWork
    from store.models import Store, Employee, Position, Author, Publisher, Book, Client, Purchase, PurchaseDetail, Genre

    repo = UnitOfWork()

    print("Очистка бази даних...")
    repo.clear_all()
    print(" Усі таблиці очищено!\n")

    store1 = repo.stores.create(
        name="The Book Loft",
        city="Columbus",
        address="631 South Third St.",
        phone="1234567891",
        email="info@bookloft.com")

    position1 = repo.positions.create(
        role="Store Manager",
        salary=Decimal("2500.00"))

    position2 = repo.positions.create(
        role="Sales Assistant",
        salary=Decimal("1200.00"))

    position3 = repo.positions.create(
        role="Inventory Specialist",
        salary=Decimal("1800.00"))

    position4 = repo.positions.create(
        role="Customer Support",
        salary=Decimal("1500.00"))

    employee1 = repo.employees.create(
        first_name="John",
        last_name="Doe",
        birth_date=date(1985, 4, 12),
        phone="+1-614-555-1234",
        email="john.doe@example.com",
        position=position1,
        store=store1
    )

    employee2 = repo.employees.create(
        first_name="Emily",
        last_name="Smith",
        birth_date=date(1990, 7, 22),
        phone="+1-212-555-5678",
        email="emily.smith@example.com",
        position=position2,
        store=store1
    )

    employee3 = repo.employees.create(
        first_name="Michael",
        last_name="Johnson",
        birth_date=date(1988, 2, 5),
        phone="+44-20-555-7890",
        email="michael.johnson@example.co.uk",
        position=position3,
        store=store1
    )

    employee4 = repo.employees.create(
        first_name="Sophie",
        last_name="Brown",
        birth_date=date(1995, 11, 30),
        phone="+1-503-555-3456",
        email="sophie.brown@example.com",
        position=position4,
        store=store1
    )

    author1 = repo.authors.create(
        first_name="Agatha", last_name="Christie", pseudonym=None,
        birth_date=date(1890, 9, 15), death_date=date(1976, 1, 12), country="UK"
    )

    author2 = repo.authors.create(
        first_name="Haruki", last_name="Murakami", pseudonym=None,
        birth_date=date(1949, 1, 12), death_date=None, country="Japan"
    )

    author3 = repo.authors.create(
        first_name="George", last_name="Orwell", pseudonym=None,
        birth_date=date(1903, 6, 25), death_date=date(1950, 1, 21), country="UK"
    )

    author4 = repo.authors.create(
        first_name="Ernest", last_name="Hemingway", pseudonym=None,
        birth_date=date(1899, 7, 21), death_date=date(1976, 7, 2), country="USA"
    )

    pub1 = repo.publishers.create(
        name="Penguin", email="contact@penguin.com", phone="1234567890", address="London, UK")

    pub2 = repo.publishers.create(
        name="Random House", email="info@randomhouse.com", phone="0987654321", address="New York, USA")

    pub3 = repo.publishers.create(
        name="Knopf Publishing Group", email="info@knopf.com", phone="0979812044", address="New York, USA")

    book1 = repo.books.create(name="Murder on the Orient Express",
                              isbn="9780062693662", price=Decimal("15.00"), publisher=pub2)

    book2 = repo.books.create(
        name="New Age Book", isbn="1234567890123", price=Decimal("20.00"), publisher=pub2)

    book3 = repo.books.create(
        name="Kafka on the Shore", isbn="9781400079278", price=Decimal("18.50"), publisher=pub3)

    book4 = repo.books.create(
        name="1984",
        isbn="9780451524935", price=Decimal("14.00"), publisher=pub3)

    book5 = repo.books.create(
        name="The Old Man and the Sea",
        isbn="9780684801223", price=Decimal("13.50"), publisher=pub2)

    client1 = repo.clients.create(
        first_name="Yaryna", last_name="Panychevska", email="pa.yaryna@gmail.com", phone="0979812088")

    client2 = repo.clients.create(
        first_name="Yaryna", last_name="Shcherban", email="yaryna.shcherban@gmail.com", phone="0979812099"
    )
    book1.author.add(author1)
    book2.author.add(author1)
    book3.author.add(author2)
    book4.author.add(author3)
    book5.author.add(author4)

    genre1 = repo.genres.create(name="Fiction")
    genre2 = repo.genres.create(name="Mystery")
    genre3 = repo.genres.create(name="Classic")
    genre4 = repo.genres.create(name="Adventure")
    genre5 = repo.genres.create(name="Dystopian")
    genre6 = repo.genres.create(name="Fantasy")
    genre7 = repo.genres.create(name="Self-Help")

    book1.genres.add(genre1, genre2, genre4)
    book2.genres.add(genre1, genre7)
    book3.genres.add(genre1, genre6, genre4)
    book4.genres.add(genre1, genre3, genre5)
    book5.genres.add(genre1, genre3, genre4)

    purchase1 = repo.purchases.create(
        client=client1, employee=employee2, store=store1, total_amount=Decimal("29.00"))

    purchase_detail1 = repo.purchase_details.create(
        purchase=purchase1, book=book1, quantity=1, price_at_purchase=book1.price)

    purchase_detail1_2 = repo.purchase_details.create(
        purchase=purchase1, book=book4, quantity=1, price_at_purchase=book4.price)

    purchase2 = repo.purchases.create(
        client=client2, employee=employee2, store=store1, total_amount=Decimal("33.50"))

    purchase_detail2 = repo.purchase_details.create(
        purchase=purchase2, book=book2, quantity=1, price_at_purchase=book2.price)

    purchase_detail2_1 = repo.purchase_details.create(
        purchase=purchase2, book=book5, quantity=1,
        price_at_purchase=book5.price)


def demo_queries():
    from store.repositories.unit_of_work import UnitOfWork
    repo = UnitOfWork()

    print("\n=== Демонстрація роботи репозиторіїв ===")

    print("\n Усі автори з Великобританії (UK):")
    for a in repo.authors.find_by_country("UK"):
        print(f"  - {a.first_name} {a.last_name}")

    print("\n Автори, які ще живі:")
    for a in repo.authors.get_alive_authors():
        print(f"  - {a.first_name} {a.last_name}")

    print("\n Книги, ціна яких нижча за 16.00:")
    for b in repo.books.get_books_cheaper_than(16.00):
        print(f"  - {b.name} ({b.price} $)")

    print("\n Книги, які видав Penguin:")
    publisher = repo.publishers.model.objects.get(name="Penguin")
    for b in repo.books.get_books_by_publisher(publisher.publisher_id):
        print(f"  - {b.name}")

    print("\n Усі працівники магазину:")
    for e in repo.employees.get_all():
        print(f"  - {e.first_name} {e.last_name}, {e.position.role}")

    print("\n Знайти працівників за посадою 'Sales Assistant':")
    for e in repo.employees.get_by_position("Sales Assistant"):
        print(f"  - {e.first_name} {e.last_name}")

    print("\n Пошук клієнта за email:")
    client = repo.clients.find_by_email("pa.yaryna@gmail.com")
    print(f"  - {client.first_name} {client.last_name}")

    print("\n Посади з окладом від 1200 до 2000:")
    for p in repo.positions.get_salary_range(1200, 2000):
        print(f"  - {p.role} ({p.salary} $)")

    print("\n Всі покупки:")
    for purchase in repo.purchases.get_all():
        print(
            f"  - Покупка #{purchase.purchase_id}, клієнт: {purchase.client.first_name}, сума: {purchase.total_amount} $")


if __name__ == "__main__":
    main()
    demo_queries()