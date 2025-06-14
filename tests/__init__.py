import pytest

from jeddie import create_app
from jeddie.database import get_db, Base, engine
from jeddie.database.model import Guest, Party, Item, Gift


def load_database_test_data(session):
    party_1 = Party(
        name='Jane Doe and John Roe',
        uuid='97a0b846-a798-41a2-80de-cf0d81a1f596'
    )
    guest_1 = Guest(
        id=1,
        first_name='John',
        last_name='Doe',
        party=party_1,
        attending=True
    )
    guest_2 = Guest(
        id=2,
        first_name='Jane',
        last_name='Roe',
        party=party_1,
        attending=False
    )
    party_2 = Party(
        name='Ben and Becky Smith',
        uuid='40820dfd-fd9d-4be7-872f-c57df7506328'
    )
    guest_3 = Guest(
        id=3,
        first_name='Ben',
        last_name='Smith',
        party=party_2
    )
    guest_4 = Guest(
        id=4,
        first_name='Becky',
        last_name='Smith',
        party=party_2
    )
    party_3 = Party(
        name='James Doe',
        uuid='e8ea4d4d-c6ae-4b23-95a3-e91cc511521f'
    )
    guest_5 = Guest(
        id=5,
        first_name='James',
        last_name='Doe',
        party=party_3,
        attending=True
    )
    guest_6 = Guest(
        id=6,
        first_name='Guest of James',
        last_name='Doe',
        is_plus_one=True,
        party=party_3,
        attending=True
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
    for item in [party_1, guest_1, guest_2, party_2, guest_3, guest_4, party_3, guest_5, guest_6,
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
