import unittest
from app import create_app, db, bcrypt
from app.models import User
from config import TestConfig
from flask_bcrypt import Bcrypt


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


class SignInTestCase(unittest.TestCase):
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


class GetUsersListTest(unittest.TestCase):
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


class ChangePasswordUserTest(unittest.TestCase):
    def setUp(self):
        # Set up the application and database for testing
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.bcrypt = Bcrypt(self.app)

        # Create a test user
        self.test_user = User(
            username="testuser",
            email="testuser@example.com",
            password=self.bcrypt.generate_password_hash("password123").decode("utf-8"),
        )
        db.session.add(self.test_user)
        db.session.commit()

        # Log in the test user
        self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_change_password_success(self):
        # Sign in the user and it also sets the current signing in user to be authenticated
        # So the user now can change the password
        # Step 1: Sign in the user
        login_response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        # Debugging: Print the login response for verification
        # print("Login Response:", login_response.data.decode())
        self.assertEqual(login_response.status_code, 200)  # Ensure login was successful

        # Step 2: Attempt to change password
        response = self.client.put(
            "/auth/change-password",
            json={"current_password": "password123", "new_password": "newpassword123"},
        )

        # Debugging: Check the response status code
        # print("Change Password Response Code:", response.status_code)
        # print("Change Password Response Data:", response.data.decode())

        # Check for a successful password change
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password updated successfully", response.data.decode())

        # Verify that the user's password has been changed in the database
        user = User.query.filter_by(email="testuser@example.com").first()
        self.assertTrue(bcrypt.check_password_hash(user.password, "newpassword123"))

    def test_change_password_incorrect_current(self):
        # Step 1: Sign in the user
        login_response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 200)

        # Step 2: Attempt to change the password with an incorrect current password
        response = self.client.put(
            "/auth/change-password",
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Incorrect current password", response.data.decode())

    def test_change_password_too_short(self):
        # Step 1: Sign in the user
        login_response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 200)

        # Step 2: Attempt to change the password with a new password that is too short
        response = self.client.put(
            "/auth/change-password",
            json={"current_password": "password123", "new_password": "short"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "New password must be at least 8 characters long", response.data.decode()
        )

    def test_change_password_missing_current_password(self):
        # Step 1: Sign in the user
        login_response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 200)

        # Step 2: Attempt to change the password with missing current password
        response = self.client.put(
            "/auth/change-password",
            json={"new_password": "newpassword123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Current password is required", response.data.decode())

    def test_change_password_missing_new_password(self):
        # Step 1: Sign in the user
        login_response = self.client.post(
            "/auth/signin",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 200)

        # Step 2: Attempt to change the password with missing new password
        response = self.client.put(
            "/auth/change-password",
            json={"current_password": "password123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("New password is required", response.data.decode())


if __name__ == "__main__":
    unittest.main()
