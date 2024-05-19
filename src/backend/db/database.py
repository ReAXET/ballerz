from prisma import Prisma
import pprint

# Prisma instance 
def db_connect_instance():
    db = Prisma()
    db.connect()

    test_users = db.user.create(
        {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password',
            'hasSubscription': False,

        }
    )
    pprint(f'created user: {test_users.json(indent=2, sort_keys=True)}')
    db.disconnect()

    return test_users


