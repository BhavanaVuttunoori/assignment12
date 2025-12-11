import pytest
from tests.conftest import client


class TestUserRegistration:
    """Test suite for user registration endpoint."""
    
    def test_register_user_success(self):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_register_user_duplicate_username(self, sample_user):
        """Test registration with duplicate username."""
        user_data = {
            "username": "testuser",  # Same as sample_user
            "email": "different@example.com",
            "password": "password123"
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]
    
    def test_register_user_duplicate_email(self, sample_user):
        """Test registration with duplicate email."""
        user_data = {
            "username": "differentuser",
            "email": "test@example.com",  # Same as sample_user
            "password": "password123"
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_user_invalid_email(self):
        """Test registration with invalid email format."""
        user_data = {
            "username": "newuser",
            "email": "invalid-email",
            "password": "password123"
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_register_user_short_username(self):
        """Test registration with username too short."""
        user_data = {
            "username": "ab",  # Less than 3 characters
            "email": "user@example.com",
            "password": "password123"
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_register_user_short_password(self):
        """Test registration with password too short."""
        user_data = {
            "username": "newuser",
            "email": "user@example.com",
            "password": "12345"  # Less than 6 characters
        }
        response = client.post("/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test suite for user login endpoint."""
    
    def test_login_success(self, sample_user):
        """Test successful user login."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = client.post("/users/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "Login successful" in data["message"]
        assert "testuser" in data["message"]
    
    def test_login_wrong_password(self, sample_user):
        """Test login with incorrect password."""
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/users/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent username."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/users/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]


class TestUserRetrieval:
    """Test suite for user retrieval endpoint."""
    
    def test_get_user_success(self, sample_user):
        """Test successful user retrieval."""
        user_id = sample_user["id"]
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_user_not_found(self):
        """Test retrieval of non-existent user."""
        response = client.get("/users/99999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
