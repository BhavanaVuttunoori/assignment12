import pytest
from tests.conftest import client


class TestCalculationBrowse:
    """Test suite for browsing calculations."""
    
    def test_browse_calculations_empty(self):
        """Test browsing when no calculations exist."""
        response = client.get("/calculations")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_browse_calculations_with_data(self, sample_user):
        """Test browsing calculations with existing data."""
        # Create test calculations
        calc1 = {"operation": "add", "operand1": 5, "operand2": 3}
        calc2 = {"operation": "multiply", "operand1": 4, "operand2": 2}
        
        client.post(f"/calculations?user_id={sample_user['id']}", json=calc1)
        client.post(f"/calculations?user_id={sample_user['id']}", json=calc2)
        
        response = client.get("/calculations")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_browse_calculations_with_pagination(self, sample_user):
        """Test browsing with pagination parameters."""
        # Create multiple calculations
        for i in range(5):
            calc = {"operation": "add", "operand1": i, "operand2": 1}
            client.post(f"/calculations?user_id={sample_user['id']}", json=calc)
        
        response = client.get("/calculations?skip=2&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_browse_calculations_filter_by_user(self, sample_user):
        """Test browsing calculations filtered by user ID."""
        # Create calculation for sample user
        calc = {"operation": "add", "operand1": 5, "operand2": 3}
        client.post(f"/calculations?user_id={sample_user['id']}", json=calc)
        
        # Create another user and calculation
        user2_data = {
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        }
        user2 = client.post("/users/register", json=user2_data).json()
        calc2 = {"operation": "subtract", "operand1": 10, "operand2": 5}
        client.post(f"/calculations?user_id={user2['id']}", json=calc2)
        
        # Filter by sample_user
        response = client.get(f"/calculations?user_id={sample_user['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_id"] == sample_user["id"]


class TestCalculationRead:
    """Test suite for reading individual calculations."""
    
    def test_read_calculation_success(self, sample_user):
        """Test successful calculation retrieval."""
        # Create calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Read calculation
        response = client.get(f"/calculations/{calc_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calc_id
        assert data["operation"] == "add"
        assert data["operand1"] == 10
        assert data["operand2"] == 5
        assert data["result"] == 15
    
    def test_read_calculation_not_found(self):
        """Test reading non-existent calculation."""
        response = client.get("/calculations/99999")
        
        assert response.status_code == 404
        assert "Calculation not found" in response.json()["detail"]


class TestCalculationAdd:
    """Test suite for adding calculations."""
    
    def test_add_calculation_addition(self, sample_user):
        """Test adding an addition calculation."""
        calc = {"operation": "add", "operand1": 7, "operand2": 3}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["operation"] == "add"
        assert data["operand1"] == 7
        assert data["operand2"] == 3
        assert data["result"] == 10
        assert data["user_id"] == sample_user["id"]
    
    def test_add_calculation_subtraction(self, sample_user):
        """Test adding a subtraction calculation."""
        calc = {"operation": "subtract", "operand1": 15, "operand2": 5}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 10
    
    def test_add_calculation_multiplication(self, sample_user):
        """Test adding a multiplication calculation."""
        calc = {"operation": "multiply", "operand1": 6, "operand2": 7}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 42
    
    def test_add_calculation_division(self, sample_user):
        """Test adding a division calculation."""
        calc = {"operation": "divide", "operand1": 20, "operand2": 4}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 5
    
    def test_add_calculation_division_by_zero(self, sample_user):
        """Test adding a calculation with division by zero."""
        calc = {"operation": "divide", "operand1": 10, "operand2": 0}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_add_calculation_invalid_operation(self, sample_user):
        """Test adding a calculation with invalid operation."""
        calc = {"operation": "power", "operand1": 2, "operand2": 3}
        response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_add_calculation_nonexistent_user(self):
        """Test adding a calculation for non-existent user."""
        calc = {"operation": "add", "operand1": 5, "operand2": 3}
        response = client.post("/calculations?user_id=99999", json=calc)
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]


class TestCalculationEdit:
    """Test suite for editing calculations."""
    
    def test_edit_calculation_operation(self, sample_user):
        """Test editing calculation operation."""
        # Create calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Edit operation
        update = {"operation": "multiply"}
        response = client.patch(f"/calculations/{calc_id}", json=update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["operation"] == "multiply"
        assert data["operand1"] == 10
        assert data["operand2"] == 5
        assert data["result"] == 50  # 10 * 5
    
    def test_edit_calculation_operands(self, sample_user):
        """Test editing calculation operands."""
        # Create calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Edit operands
        update = {"operand1": 20, "operand2": 8}
        response = client.patch(f"/calculations/{calc_id}", json=update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["operand1"] == 20
        assert data["operand2"] == 8
        assert data["result"] == 28  # 20 + 8
    
    def test_edit_calculation_all_fields(self, sample_user):
        """Test editing all calculation fields."""
        # Create calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Edit all fields
        update = {"operation": "divide", "operand1": 100, "operand2": 25}
        response = client.patch(f"/calculations/{calc_id}", json=update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["operation"] == "divide"
        assert data["operand1"] == 100
        assert data["operand2"] == 25
        assert data["result"] == 4
    
    def test_edit_calculation_not_found(self):
        """Test editing non-existent calculation."""
        update = {"operation": "add"}
        response = client.patch("/calculations/99999", json=update)
        
        assert response.status_code == 404
        assert "Calculation not found" in response.json()["detail"]
    
    def test_edit_calculation_division_by_zero(self, sample_user):
        """Test editing calculation to cause division by zero."""
        # Create calculation
        calc = {"operation": "divide", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Edit to division by zero
        update = {"operand2": 0}
        response = client.patch(f"/calculations/{calc_id}", json=update)
        
        assert response.status_code == 400
        assert "Division by zero" in response.json()["detail"]


class TestCalculationDelete:
    """Test suite for deleting calculations."""
    
    def test_delete_calculation_success(self, sample_user):
        """Test successful calculation deletion."""
        # Create calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        create_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        calc_id = create_response.json()["id"]
        
        # Delete calculation
        response = client.delete(f"/calculations/{calc_id}")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify deletion
        get_response = client.get(f"/calculations/{calc_id}")
        assert get_response.status_code == 404
    
    def test_delete_calculation_not_found(self):
        """Test deleting non-existent calculation."""
        response = client.delete("/calculations/99999")
        
        assert response.status_code == 404
        assert "Calculation not found" in response.json()["detail"]


class TestCalculationIntegration:
    """Integration tests for complete calculation workflows."""
    
    def test_complete_crud_workflow(self, sample_user):
        """Test complete CRUD workflow for calculations."""
        # 1. Add calculation
        calc = {"operation": "add", "operand1": 10, "operand2": 5}
        add_response = client.post(
            f"/calculations?user_id={sample_user['id']}", 
            json=calc
        )
        assert add_response.status_code == 201
        calc_id = add_response.json()["id"]
        
        # 2. Read calculation
        read_response = client.get(f"/calculations/{calc_id}")
        assert read_response.status_code == 200
        assert read_response.json()["result"] == 15
        
        # 3. Edit calculation
        update = {"operation": "multiply"}
        edit_response = client.patch(f"/calculations/{calc_id}", json=update)
        assert edit_response.status_code == 200
        assert edit_response.json()["result"] == 50
        
        # 4. Browse calculations
        browse_response = client.get("/calculations")
        assert browse_response.status_code == 200
        assert len(browse_response.json()) >= 1
        
        # 5. Delete calculation
        delete_response = client.delete(f"/calculations/{calc_id}")
        assert delete_response.status_code == 200
        
        # 6. Verify deletion
        verify_response = client.get(f"/calculations/{calc_id}")
        assert verify_response.status_code == 404
