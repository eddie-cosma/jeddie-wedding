import pytest

from jeddie import create_app
from jeddie.database import get_db, Base, engine
from jeddie.database.model import Guest, Party, Item, Gift


def load_database_test_data(session):
    party_1 = Party(name='Jane Doe and John Roe')
    guest_1 = Guest(
        first_name='John',
        last_name='Doe',
        party=party_1
    )
    guest_2 = Guest(
        first_name='Jane',
        last_name='Roe',
        party=party_1
    )
    party_2 = Party(name='Ben and Becky Smith')
    guest_3 = Guest(
        first_name='Ben',
        last_name='Smith',
        party=party_2
    )
    guest_4 = Guest(
        first_name='Becky',
        last_name='Smith',
        party=party_2
    )
    party_3 = Party(name='James Doe')
    guest_5 = Guest(
        first_name='James',
        last_name='Doe',
        party=party_3
    )
    item_1 = Item(
        name='Test Item 1',
        name_ro='Test Item 1 RO',
        description='This is the first test item.',
        description_ro='Acesta este primul element de testare.',
        price=1000,
        max_quantity=3,
        public=True
    )
    item_2 = Item(
        name='Test Item 2',
        name_ro='Test Item 2 RO',
        description='This is the second test item.',
        description_ro='Acesta este al doilea element de testare.',
        price=20000,
        max_quantity=1,
        public=True
    )
    gift_1 = Gift(
        buyer_name='John and Jane',
        item=item_2,
        quantity=1
    )
    for item in [party_1, guest_1, guest_2, party_2, guest_3, guest_4, party_3, guest_5,
                 item_1, item_2, gift_1]:
        session.add(item)
    session.commit()
    session.close()


@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        load_database_test_data(get_db())
        yield app
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
