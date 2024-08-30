import unittest
from app import create_app, db, bcrypt
from app.models import User
from config import TestConfig


class SignUpTestCase(unittest.TestCase):
    def setUp(self):
        # Call the function create_app() with a specific configuration 'TestConfig', which is for testing
        # Use a separate testing configuration ensures that the tests do not interfere with the development and production environments
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()  # Make the app context active during the tests

        # Create a test client for the application
        self.client = self.app.test_client()

        db.create_all()  # Ensure this is creating the tables

    def tearDown(self):
        # Remove the session and drop all tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test case: Successful sign-up
    def test_signup_success(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",  # Valid password length (8-20 characters)
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"User created successfully", response.data)

    # Test case: Sign-up fails with an existing email
    def test_signup_existing_email(self):
        # Create a user first
        self.client.post(
            "/auth/signup",
            json={
                "username": "existinguser",
                "email": "existinguser@example.com",
                "password": "password123",
            },
        )

        # Attempt to sign up with the same email
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "existinguser@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Username or email already exists", response.data)

    # Test case: Sign-up fails with an existing username
    def test_signup_existing_username(self):
        # Create a user first
        self.client.post(
            "/auth/signup",
            json={
                "username": "existinguser",
                "email": "unique@example.com",
                "password": "password123",
            },
        )

        # Attempt to sign up with the same username
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "existinguser",
                "email": "newemail@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Username or email already exists", response.data)

    def test_signup_username_too_short(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "ab",  # Too short
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Username must be between 3 and 20 characters long", response.data
        )

    def test_signup_username_too_long(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "a" * 21,  # Too long
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Username must be between 3 and 20 characters long", response.data
        )

    def test_signup_email_too_long(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "a" * 121 + "@example.com",  # Too long
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email must be 120 characters or fewer", response.data)

    def test_signup_password_too_short(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "short",  # Too short
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Password must be between 8 and 20 characters long", response.data
        )

    def test_signup_password_too_long(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "a" * 21,  # Too long
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Password must be between 8 and 20 characters long", response.data
        )

    # Test case: Sign-up fails with an invalid email format
    def test_signup_invalid_email(self):
        response = self.client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "invalidemail",  # Invalid email format
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid email address", response.data)

    # Test case: Sign-up fails with missing username
    def test_signup_missing_username(self):
        response = self.client.post(
            "/auth/signup",
            json={"email": "newuser@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Username is required", response.data)

    # Test case: Sign-up fails with missing email
    def test_signup_missing_email(self):
        response = self.client.post(
            "/auth/signup", json={"username": "newuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email is required", response.data)

    # Test case: Sign-up fails with missing password
    def test_signup_missing_password(self):
        response = self.client.post(
            "/auth/signup", json={"username": "newuser", "email": "newuser@example.com"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Password is required", response.data)


class SignUpTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

        # Create a test user
        self.test_user = User(
            username="testuser",
            email="testuser@example.com",
            password=bcrypt.generate_password_hash("password123").decode("utf-8"),
        )
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test case: Sign-in with incorrect password
    def test_signin_incorrect_password(self):
        response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid email or password", response.data)

    # Test case: Sign-in with non-existent email
    def test_signin_nonexistent_email(self):
        response = self.client.post(
            "/auth/signin",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid email or password", response.data)

    def test_signin_invalid_email_format(self):
        response = self.client.post(
            "/auth/signin",
            json={"email": "invalid-email-format", "password": "password123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid email address", response.data)

    def test_signin_email_too_long(self):
        response = self.client.post(
            "/auth/signin",
            json={
                "email": "a" * 121 + "@example.com",  # Email too long
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email must be 120 characters or fewer", response.data)

    def test_signin_password_too_short(self):
        response = self.client.post(
            "/auth/signin",
            json={
                "email": "testuser@example.com",
                "password": "short",  # Password too short
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Password must be between 8 and 20 characters long", response.data
        )

    def test_signin_password_too_long(self):
        response = self.client.post(
            "/auth/signin",
            json={
                "email": "testuser@example.com",
                "password": "a" * 21,  # Password too long
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Password must be between 8 and 20 characters long", response.data
        )

    def test_signin_missing_email(self):
        response = self.client.post("/auth/signin", json={"password": "password123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email is required", response.data)

    def test_signin_missing_password(self):
        response = self.client.post(
            "/auth/signin", json={"email": "testuser@example.com"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Password is required", response.data)


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create some test users
        self.test_user1 = User(
            username="testuser1", email="testuser1@example.com", password="password123"
        )
        self.test_user2 = User(
            username="testuser2", email="testuser2@example.com", password="password123"
        )

        db.session.add(self.test_user1)
        db.session.add(self.test_user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test case: Ensure /users route returns the correct list of users
    def test_users_list(self):
        response = self.client.get("/auth/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["username"], "testuser1")
        self.assertEqual(response.json[1]["username"], "testuser2")

    # Test case: Ensure /users route handles no users in the database
    def test_users_list_empty(self):
        # First, clear the users from the database
        db.session.query(User).delete()
        db.session.commit()

        response = self.client.get("/auth/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # Should return an empty list


if __name__ == "__main__":
    unittest.main()
