import datetime
from sqlite3 import Date
from django.test import TestCase
from rest_framework.test import APIClient
from artists.models import Artist, Expenses, Income, Show, Type
from model_bakery import baker

# Create your tests here.
class ArtistsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_artist_list(self):
        tp = baker.make("artists.Type")
        shw = baker.make("Show",type = tp,price = 12000)
        artist = baker.make("Artist",show = shw)

        #tp = Type.objects.create(
        #    show_type = "Световое шоу"
        #)
        
        #shw = Show.objects.create(
        #    name = "Индиго",
        #    type = tp,
        #    price = 12000,
        #)

        #artist = Artist.objects.create(
        #    name = "Валерия",
        #    show = shw,
        #)

        r = self.client.get('/api/artists/')
        data = r.json()
        print(data)

        assert artist.name == data[0]['name']
        assert artist.id == data[0]['id']
        assert artist.show.name == data[0]['show']['name']
        assert len(data) == 1

    def test_create_artist(self):
        tp = baker.make("artists.Type")
        shw = baker.make("Show",type = tp,price = 12000)
        #artist = baker.make("Artist",show = shw)

        r = self.client.post("/api/artists/",{
            "name": "Артист",
            "show": shw.id,
        })  

        new_artist_id = r.json()['id']

        artistn = Artist.objects.all()
        assert len(artistn) == 1

        new_artist = Artist.objects.filter(id=new_artist_id).first()
        assert new_artist.name == 'Артист'
        assert new_artist.show == shw

    def test_delete_artist(self):
        artists = baker.make("Artist",10)
        r = self.client.get('/api/artists/')
        data = r.json()
        assert len(data) == 10

        artist_id_to_delete = artists[3].id
        r = self.client.delete(f'/api/artists/{artist_id_to_delete}/')
 
        r = self.client.get('/api/artists/')
        data = r.json()
        assert len(data) == 9

        assert artist_id_to_delete not in [i['id'] for i in data]

    def test_update_artist(self):
        artists = baker.make("Artist",10)
        artist: Artist = artists[2]

        r = self.client.get(f'/api/artists/{artist.id}/')
        data = r.json()
        assert data['name'] == artist.name

        r = self.client.put(f'/api/artists/{artist.id}/',{
            "name":"Валерия"
        })
        assert r.status_code==200

        r = self.client.get(f'/api/artists/{artist.id}/')
        data = r.json()
        assert data['name'] == "Валерия"

        artist.refresh_from_db()
        assert data['name'] == artist.name

class ShowViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_show_list(self):
        tp = baker.make("artists.Type")
        show = baker.make("Show",type = tp,price = 12000)

        r = self.client.get('/api/show/')
        data = r.json()
        print(data)

        assert show.name == data[0]['name']
        assert show.id == data[0]['id']
        assert show.type.show_type == data[0]['type']['show_type']
        assert len(data) == 1

    def test_create_show(self):
        tp = baker.make("artists.Type")

        r = self.client.post("/api/show/",{
            "name": "Шоу",
            "type": tp.id,
            "price": 12000,
        })  

        new_show_id = r.json()['id']

        show = Show.objects.all()
        assert len(show) == 1

        new_show = Show.objects.filter(id=new_show_id).first()
        assert new_show.name == 'Шоу'
        assert new_show.price == 12000
        assert new_show.type.show_type == tp.show_type

    def test_delete_show(self):
        shows = baker.make("Show",10)
        r = self.client.get('/api/show/')
        data = r.json()
        assert len(data) == 10

        show_id_to_delete = shows[3].id
        r = self.client.delete(f'/api/show/{show_id_to_delete}/')
 
        r = self.client.get('/api/show/')
        data = r.json()
        assert len(data) == 9

        assert show_id_to_delete not in [i['id'] for i in data]

    def test_update_show(self):
        shows = baker.make("Show",10)
        show: Show = shows[2]

        r = self.client.get(f'/api/show/{show.id}/')
        data = r.json()
        assert data['name'] == show.name

        r = self.client.put(f'/api/show/{show.id}/',{
            "name":"Золото",
            "price": 1200,
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/show/{show.id}/')
        data = r.json()
        assert data['name'] == "Золото"
        assert data['price'] == 1200

        show.refresh_from_db()
        assert data['name'] == show.name
        assert data['price'] == show.price

class TypeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_type_list(self):
        type = baker.make("artists.Type")

        r = self.client.get('/api/type/')
        data = r.json()
        print(data)

        assert type.show_type == data[0]['show_type']
        assert type.id == data[0]['id']
        assert len(data) == 1

    def test_create_type(self):
        r = self.client.post("/api/type/",{
            "show_type": "Тип",
        })  

        new_type_id = r.json()['id']

        type = Type.objects.all()
        assert len(type) == 1

        new_type = Type.objects.filter(id=new_type_id).first()
        assert new_type.show_type == 'Тип'

    def test_delete_type(self):
        types = baker.make("Type",10)
        r = self.client.get('/api/type/')
        data = r.json()
        assert len(data) == 10

        type_id_to_delete = types[3].id
        r = self.client.delete(f'/api/type/{type_id_to_delete}/')
 
        r = self.client.get('/api/type/')
        data = r.json()
        assert len(data) == 9

        assert type_id_to_delete not in [i['id'] for i in data]

    def test_update_type(self):
        types = baker.make("Type",10)
        type: Type = types[2]

        r = self.client.get(f'/api/type/{type.id}/')
        data = r.json()
        assert data['show_type'] == type.show_type

        r = self.client.put(f'/api/type/{type.id}/',{
            "show_type":"Тип",
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/type/{type.id}/')
        data = r.json()
        assert data['show_type'] == "Тип"

        type.refresh_from_db()
        assert data['show_type'] == type.show_type

class IncomeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_income_list(self):
        sh = baker.make("artists.Show")
        income = baker.make("Income", date = "2024-09-12",place = "dvdfv",show = sh)

        r = self.client.get('/api/income/')
        data = r.json()
        print(data)

        assert income.date == data[0]['date']
        assert income.id == data[0]['id']
        assert income.place == data[0]['place']
        assert income.show.name == data[0]['show']['name']
        assert len(data) == 1

    def test_create_income(self):
        sh = baker.make("artists.Show")

        r = self.client.post("/api/income/",{
            "date": "2024-09-12",
            "place": "dvdfv",
            "show": sh.id,
        })  

        new_income_id = r.json()['id']

        income = Income.objects.all()
        assert len(income) == 1

        new_income = Income.objects.filter(id=new_income_id).first()
        assert new_income.date == datetime.date(2024, 9, 12)
        assert new_income.place == "dvdfv"
        assert new_income.show.name == sh.name

    def test_delete_income(self):
        incomes = baker.make("Income",10)
        r = self.client.get('/api/income/')
        data = r.json()
        assert len(data) == 10

        income_id_to_delete = incomes[3].id
        r = self.client.delete(f'/api/income/{income_id_to_delete}/')
 
        r = self.client.get('/api/income/')
        data = r.json()
        assert len(data) == 9

        assert income_id_to_delete not in [i['id'] for i in data]

    def test_update_income(self):
        incomes = baker.make("Income",10)
        income: Income = incomes[2]

        r = self.client.get(f'/api/income/{income.id}/')
        data = r.json()
        assert data['place'] == income.place

        r = self.client.put(f'/api/income/{income.id}/',{
            "date": "2024-09-12",
            "place": "dvdfv",
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/income/{income.id}/')
        data = r.json()
        assert data['date'] == "2024-09-12"
        assert data['place'] == "dvdfv"

        income.refresh_from_db()
        assert data['date'] == income.date.strftime('%Y-%m-%d')
        assert data['place'] == income.place


class ExpensesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()   

    def test_get_expenses_list(self):
        art = baker.make("artists.Artist")
        inc = baker.make("artists.Income")
        expense = baker.make("Expenses", salary=1750, artist=art, income=inc)

        r = self.client.get('/api/expense/')
        data = r.json()
        print(data)

        assert expense.salary == data[0]['salary']
        assert expense.id == data[0]['id']
        assert expense.artist.name == data[0]['artist']['name']
        assert expense.income.id == data[0]['income']['id']
        assert len(data) == 1

    def test_create_expense(self):
        art = baker.make("artists.Artist")
        inc = baker.make("artists.Income")

        r = self.client.post("/api/expense/",{
            "salary": 1750,
            "artist": art.id,
            "income": inc.id,
        })  

        new_expense_id = r.json()['id']

        income = Income.objects.all()
        assert len(income) == 1

        new_expense = Expenses.objects.filter(id=new_expense_id).first()
        assert new_expense.salary == 1750
        assert new_expense.artist.name == art.name
        assert new_expense.income.place == inc.place

    def test_delete_expense(self):
        expenses = baker.make("Expenses",10)
        r = self.client.get('/api/expense/')
        data = r.json()
        assert len(data) == 10

        expense_id_to_delete = expenses[3].id
        r = self.client.delete(f'/api/expense/{expense_id_to_delete}/')
 
        r = self.client.get('/api/expense/')
        data = r.json()
        assert len(data) == 9

        assert expense_id_to_delete not in [i['id'] for i in data]

    def test_update_expense(self):
        #incomes = baker.make("Income",10)
        #income: Income = incomes[2]
        expenses = baker.make("Expenses",10)
        expense: Expenses = expenses[2]

        r = self.client.get(f'/api/expense/{expense.id}/')
        data = r.json()
        assert data['salary'] == expense.salary

        r = self.client.put(f'/api/expense/{expense.id}/',{
            "salary": 1200,
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/expense/{expense.id}/')
        data = r.json()
        assert data['salary'] == 1200

        expense.refresh_from_db()
        assert data['salary'] == 1200