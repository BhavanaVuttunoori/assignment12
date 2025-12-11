from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common attributes."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserRead(UserBase):
    """Schema for reading user data (response)."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Calculation Schemas
class CalculationBase(BaseModel):
    """Base calculation schema with common attributes."""
    operation: str = Field(..., pattern="^(add|subtract|multiply|divide)$")
    operand1: float
    operand2: float

    @validator('operand2')
    def check_division_by_zero(cls, v, values):
        """Validate that division by zero is not allowed."""
        if 'operation' in values and values['operation'] == 'divide' and v == 0:
            raise ValueError('Division by zero is not allowed')
        return v


class CalculationCreate(CalculationBase):
    """Schema for creating a new calculation."""
    pass


class CalculationUpdate(BaseModel):
    """Schema for updating an existing calculation."""
    operation: Optional[str] = Field(None, pattern="^(add|subtract|multiply|divide)$")
    operand1: Optional[float] = None
    operand2: Optional[float] = None

    @validator('operand2')
    def check_division_by_zero(cls, v, values):
        """Validate that division by zero is not allowed."""
        if v is not None and 'operation' in values and values.get('operation') == 'divide' and v == 0:
            raise ValueError('Division by zero is not allowed')
        return v


class CalculationRead(CalculationBase):
    """Schema for reading calculation data (response)."""
    id: int
    result: float
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Response schemas
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
