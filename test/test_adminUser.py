from fastapi.testclient import TestClient
from db.database import Base, engine, Session, User

# import checkhash
from utils.hashPassword import check_password

# import app
from main import app

# import related router
from router.adminUser import router as adminUser_router

app.include_router(adminUser_router)

# Before test, setup table
def setup_function():
    Base.metadata.create_all(bind=engine)
    # append some info into database
    session = Session()
    session.add_all([
        User(name='User1', email='user1@example.com', password='password1'),
        User(name='User2', email='user2@example.com', password='password2'),
    ])
    session.commit()

# After test, clean table
def teardown_function():
    Base.metadata.drop_all(bind=engine)

# test get all users
def test_get_all_users():
    # use TestClient create client side
    client = TestClient(app)

    # router go to /users to get_all_user
    response = client.get('/users')
    
    # check status_code and data
    assert response.status_code == 200
    assert response.json() == {
        'status': 'Success',
        'users': [
            {'id': 1, 'name': 'User1', 'email': 'user1@example.com', 'password':'password1'},
            {'id': 2, 'name': 'User2', 'email': 'user2@example.com', 'password':'password2'},
        ]
    }

# test get a existed user
def test_get_a_user():
    client = TestClient(app)
    response = client.get('/users/1')

    # check status_code and data
    assert response.status_code == 200
    assert response.json() == {
        'status': 'Success',
        'user': {
            'id': 1, 
            'name': 'User1', 
            'email': 'user1@example.com', 
            'password':'password1'
        }
    }

# test get not existed user id=3
def test_get_not_existed_user():
    client = TestClient(app)
    response = client.get('/users/3')
    
    # check status_code and data
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "status": "Fail",
            "error-message": "Cannot found the user"
        }
    }

# test create user3
def test_post_a_user():
    client = TestClient(app)
    newUser = {
        'name': 'User3',
        'email': 'user3@example.com',
        'password': 'password3'
    }

    # router go to /users to get_a_user
    response = client.post('/users/create', json=newUser)
    js = response.json()
    password = js['user']['password']
    result = check_password('password3', password)

    assert response.status_code == 200
    assert js['status'] == 'Success'
    assert js['user']['id'] == 3
    assert js['user']['name'] == 'User3'
    assert js['user']['email'] == 'user3@example.com'
    assert result == True

# test create with blank field in email
def test_post_a_user_with_email_blank():
    client = TestClient(app)
    newUser = {
        'name': 'User4',
        'email': '  ',
        'password': 'password4'
    }
    response = client.post('/users/create', json=newUser)
    assert response.status_code == 400
    assert response.json() == {
            "detail": {
                "status": "Fail",
                "error-message": "Please fill all the fields and not fill with blank."
            }
        }

# test create with a registered email
def test_post_a_user_with_existed_email():
    client = TestClient(app)
    newUser = {
        'name': 'User1',
        'email': 'user1@example.com',
        'password': 'password1'
    }
    response = client.post('/users/create', json=newUser)
    assert response.status_code == 400
    assert response.json() == {
            "detail": {
                "status": "Fail",
                "error-message": "Email has existed"
            }
        }

# test edit user1
def test_edit_a_user():
    client = TestClient(app)
    newUser = {
        'name': 'User11',
        'email': 'user11@example.com',
        'password': 'password11'
    }

    # router go to /users to get_a_user
    response = client.put('/users/1', json=newUser)
    js = response.json()
    password = js['user']['password']
    result = check_password('password11', password)

    assert response.status_code == 200
    assert js['status'] == 'Success'
    assert js['user']['id'] == 1
    assert js['user']['name'] == 'User11'
    assert js['user']['email'] == 'user11@example.com'
    assert result == True

# test delete user1
def test_delete_user1():
    client = TestClient(app)
    response = client.delete('/users/1')

    # check status_code and data
    assert response.status_code == 200
    assert response.json() == {
        'status': 'Success'
    }

    response = client.get('/users/1')
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "status": "Fail",
            "error-message": "Cannot found the user"
        }
    }

# test delete not existed user
def test_delete_not_existed_user():
    client = TestClient(app)
    response = client.delete('/users/3')

    # check status_code and data
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            'status': 'Fail', 
            'error-message': 'Cannot found the user'
        }
    }