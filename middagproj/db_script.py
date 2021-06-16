import django
import os

# Set django variables, must be done before making calls to import apps
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middagproj.settings')
django.setup()

# Run management commands like makemigrations and migrate
from django.core import management

# Custom model/business logic
from dinnerevent.models import Event, Comment, Review
from django.contrib.auth.models import User
from users.models import Profile, Allergy

# Dicts

allergy_array = [
    'Gluten', 'Skalldyr', 'Egg', 'Fisk', 'Peanøtter', 'Soya', 'Melk',
    'Nøtter', 'Selleri', 'Sennep', 'Sesamfrø', 'Svoveldioksid og sulfitt',
    'Lupin', 'Bløtdyr'
]

users_dict = {
    '1': {
        'username': 'OlaNordmann', 'email': 'ola@nordmann.no', 'password': 'Passord1',
        'address': 'Gokk', 'allergies': ['Skalldyr', 'Bløtdyr']
    },
    '2': {
        'username': 'KariNordmann', 'email': 'kari@nordmann.no', 'password': 'Passord1',
        'address': 'Norge rundt', 'allergies': ['Gluten', 'Egg']
    },
    '3': {
        'username': 'bob_kaare', 'email': 'bob@kaare.no', 'password': 'Passord1',
        'address': 'Mostadmarka', 'allergies': ['Selleri', 'Soya']
    },
    '4': {
        'username': 'kungen', 'email': 'kungen@slottet.no', 'password': 'Passord1',
        'address': 'Det kongelige slott', 'allergies': ''
    },
    '5': {
        'username': 'demo', 'email': 'demo@middagsdeling.no', 'password': 'Passord1',
        'address': 'Demo', 'allergies': ''
    }
}

events_dict = {
    '1': {
        'user__pk': 1,
        'title': 'Tacokveld',
        'description': 'Har skikkelig fredagsstemning, så ta med godt humør og rømmedressing',
        'seats': 4,
        'place': 'Gokk',
        'expense': 100,
        'date': '2021-04-14',
        'time': '18:15:00',
        'ingredients': 'Kjøttdeig, tomat, salat, løk, bønner, lefser, tacokrydder, guacamole, paprika',
        'allergies': ['Gluten', 'Egg'],
        'guests': ['KariNordmann', 'kungen']
    },
    '2': {
        'user__pk': 1,
        'title': 'Spanderer Peppes, førstemann til mølla!',
        'description': 'Vant på skraplodd og føler jeg må være litt sjenerøs',
        'seats': 8,
        'place': 'Peppes Pizza Falkenborgveien',
        'expense': 0,
        'date': '2021-04-9',
        'time': '17:30:00',
        'ingredients': 'Veit ikke! Vi bestiller hva som helst',
        'allergies': ['Gluten'],
        'guests': ['bob_kaare'],
    },
    '3': {
        'user__pk': 2,
        'title': 'Suppekjøkken',
        'description': 'Har 1000L med suppe som må forsvinne ned kjeftet på folk, pronto',
        'seats': '200',
        'place': 'Frelsesarmeen',
        'expense': 0,
        'date': '2021-05-30',
        'time': '12:00:00',
        'ingredients': 'Er vel egentlig bare tomater',
        'allergies': [],
        'guests': [],
    },
    '4': {
        'user__pk': 3,
        'title': 'Pølser i hytt og i vær',
        'description': 'Corona satte en stopp på 17.mai feiring i fjor på slottet, så i år blir det fart på sakene. '
                       'Blir mange pølser, så bare å gafle i seg.',
        'seats': '40',
        'place': 'Slottet',
        'expense': 0,
        'date': '2021-05-17',
        'time': '11:00:00',
        'ingredients': 'Pølser (grill, wiener, ostegrill, etc), lompe fra Røros og pølsebrød fra Hatting',
        'allergies': ['Gluten'],
        'guests': [],
    },
    '5': {
        'user__pk': 4,
        'title': 'Sjødyrbuffet',
        'description': 'Vært på lofotfiske og fått en gedigen fangst, vær så snill jeg orker ikke mer sjømat',
        'seats': 14,
        'place': 'Sjarken te han bestefar',
        'expense': 0,
        'date': '2021-03-31',
        'time': '16:00:00',
        'ingredients': 'En hver levende orgranisme i havet',
        'allergies': ['Skalldyr', 'Bløtdyr', 'Fisk'],
        'guests': ['kungen', 'OlaNordmann'],
    },
    '6': {
        'user__pk': 4,
        'title': 'Fiskeburger',
        'description': 'Ekte lofotfisk',
        'seats': 3,
        'place': 'Hjemme hos meg',
        'expense': 150,
        'date': '2021-04-02',
        'time': '19:45:00',
        'ingredients': 'Mye rart oppiher',
        'allergies': ['Fisk', 'Gluten'],
        'guests': ['KariNordmann'],
    },
    '7': {
        'user__pk': 5,
        'title': 'DEMO ARRANGEMENT',
        'description': 'DEMO',
        'seats': 7,
        'place': 'Presentasjon',
        'expense': 0,
        'date': '2021-04-09',
        'time': '15:30',
        'ingredients': 'DEMO ARRANGEMENT',
        'allergies': '',
        'guests': [],
    },
}


# Functions

def create_allergies():
    for name in allergy_array:
        allergy = Allergy.objects.create(allergy=name)
        allergy.save()
        print(allergy)


def create_users():
    for user_id, user_info in users_dict.items():

        # User variables
        username = user_info['username']
        email = user_info['email']
        password = user_info['password']

        # Profile variables
        address = user_info['address']
        allergies = user_info['allergies']

        # DEBUG
        print(
            'Creating user={username}, email={email}, pwd={password}'.format(
                username=username, email=email, password=password
            )
        )

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        # DEBUG
        print(
            f'Creating profile with user={user}, address={address}, allergies={allergies}'
                .format(user=user, address=address, allergies=allergies)
        )

        # Create profile for user
        profile = Profile.objects.create(
            user=user, address=address
        )
        for allergy in allergies:
            profile.allergies.add(Allergy.objects.get(allergy=allergy))

        # Make the calls to commit in DB
        user.save()
        profile.save()


def create_superusers():
    admin = User.objects.create_superuser("admin", "admin@middagsdeling.no", "admin")
    Profile.objects.create(user=admin, address="Serveren")
    print(admin)


def create_events():
    for event_id, event_info in events_dict.items():

        # Event variables
        user = User.objects.get(pk=event_info['user__pk'])
        title = event_info['title']
        description = event_info['description']
        seats = event_info['seats']
        place = event_info['place']
        expense = event_info['expense']
        date = event_info['date']
        time = event_info['time']
        ingredients = event_info['ingredients']
        allergies = event_info['allergies']
        guests = event_info['guests']

        # Debug
        print(
            f'Creating event={title} made by user={user}'
                .format(title=title, user=user)
        )

        event = Event.objects.create(
            user=user, title=title, description=description, seats=seats, place=place,
            expense=expense, date=date, time=time, ingredients=ingredients
        )

        for allergy in allergies:
            event.allergies.add(Allergy.objects.get(allergy=allergy))

        for guest in guests:
            event.guests.add(User.objects.get(username=guest))

            # Likewise we add the relation to the guest (should have been a symmetric
            # relation, but because of Profile implementation this is not the case) and
            # we have to explicitly call an insert

            User.objects.get(username=guest).profile.events.add(event)

        # Commit to DB
        event.save()


def create_comments():
    print(Comment.objects.create(event=Event.objects.get(pk=1),
                                 user=User.objects.get(pk=2),
                                 content="Kommer det til å være guacamole?",
                                 ))
    print(Comment.objects.create(event=Event.objects.get(pk=1),
                                 user=User.objects.get(pk=4),
                                 content="Gleder meg!"
                                 ))
    print(Comment.objects.create(event=Event.objects.get(pk=2),
                                 user=User.objects.get(pk=3),
                                 content="Mmmm, gratis pizza..."
                                 ))


def create_reviews():
    print(Review.objects.create(event=Event.objects.get(pk=1),
                                user=User.objects.get(pk=2),
                                body="Kjempegode tacoer, i tillegg til en flott vert!",
                                rating=5
                                ))
    print(Review.objects.create(event=Event.objects.get(pk=1),
                                user=User.objects.get(pk=4),
                                body="Tacoene var helt greie, men verten virket litt sur",
                                rating=2
                                ))
    print(Review.objects.create(event=Event.objects.get(pk=2),
                                user=User.objects.get(pk=3),
                                body="Sier aldri nei til gratis pizza",
                                rating=4
                                ))


def main():
    print("MAKING MIGRATIONS...")
    management.call_command('makemigrations', verbosity=1)

    print("\n MIGRATING...")

    management.call_command('migrate', verbosity=1)

    print("\n CREATING DATABASE ENTRIES")

    print("\n -------------------------")
    print("CREATING ALLERGIES")
    print("-------------------------")
    create_allergies()

    print("\n -------------------------")
    print("CREATING USERS")
    print("-------------------------")
    create_users()

    print("\n -------------------------")
    print("CREATING EVENTS")
    print("-------------------------")
    create_events()

    print("\n -------------------------")
    print("CREATING COMMENTS")
    print("-------------------------")
    create_comments()

    print("\n -------------------------")
    print("CREATING REVIEWS")
    print("-------------------------")
    create_reviews()

    print("\n -------------------------")
    print("CREATING SUPERUSERS")
    print("-------------------------")
    create_superusers()


if __name__ == '__main__':
    main()
