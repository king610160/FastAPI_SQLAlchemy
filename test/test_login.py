from fastapi.testclient import TestClient
from db.database import Base, engine, Session, User

# import checkhash
from utils.hashPassword import hash_password, check_password

# import app
from main import app

# import related router
from router.login import router as login_router

app.include_router(login_router)

# Before test, setup table
def setup_function():
    Base.metadata.create_all(bind=engine)
    # append some info into database
    session = Session()
    password1 = hash_password('password1')
    password2 = hash_password('password2')
    session.add_all([
        User(name='User1', email='user1@example.com', password=password1),
        User(name='User2', email='user2@example.com', password=password2),
    ])
    session.commit()

# After test, clean table
def teardown_function():
    Base.metadata.drop_all(bind=engine)

# test login
def test_post_a_user():
    client = TestClient(app)
    user = {
        'name': 'User1',
        'email': 'user1@example.com',
        'password': 'password1'
    }

    # router go to /users to get_a_user
    response = client.post('/login', json=user)
    js = response.json()
    password = js['user']['password']
    result = check_password('password1', password)

    assert response.status_code == 200
    assert js['status'] == 'Success'
    assert js['user']['id'] == 1
    assert js['user']['name'] == 'User1'
    assert js['user']['email'] == 'user1@example.com'
    assert result == True

# test login with fail password
def test_post_a_user_with_wrong_password():
    client = TestClient(app)
    user = {
        'name': 'User1',
        'email': 'user1@example.com',
        'password': 'password2'
    }

    # router go to /users to get_a_user
    response = client.post('/login', json=user)

    assert response.status_code == 400
    assert response.json() == {
            "detail": {
                'status': 'Fail', 
                'error-message': 'Email or password is not correct'
            }
        }

# test login with not exist user
def test_post_a_user_with_not_existed_user():
    client = TestClient(app)
    user = {
        'name': 'User3',
        'email': 'user3@example.com',
        'password': 'password3'
    }

    # router go to /users to get_a_user
    response = client.post('/login', json=user)

    assert response.status_code == 400
    assert response.json() == {
            "detail": {
                'status': 'Fail', 
                'error-message': 'Email or password is not correct'
            }
        }
