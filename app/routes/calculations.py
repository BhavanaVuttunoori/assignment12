from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Calculation, User
from app.schemas import CalculationCreate, CalculationRead, CalculationUpdate, MessageResponse
from app.utils import calculate

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("", response_model=List[CalculationRead])
def browse_calculations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    user_id: int = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """
    Browse all calculations with optional pagination and filtering.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    - **user_id**: Optional filter by user ID
    """
    query = db.query(Calculation)
    
    if user_id:
        query = query.filter(Calculation.user_id == user_id)
    
    calculations = query.offset(skip).limit(limit).all()
    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(calculation_id: int, db: Session = Depends(get_db)):
    """
    Read a specific calculation by ID.
    
    - **calculation_id**: The ID of the calculation to retrieve
    """
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    return calculation


@router.post("", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(
    calc_data: CalculationCreate,
    user_id: int = Query(..., description="User ID performing the calculation"),
    db: Session = Depends(get_db)
):
    """
    Add a new calculation.
    
    - **operation**: Type of operation (add, subtract, multiply, divide)
    - **operand1**: First operand
    - **operand2**: Second operand
    - **user_id**: ID of the user creating the calculation
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Perform calculation
    try:
        result = calculate(calc_data.operation, calc_data.operand1, calc_data.operand2)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create new calculation
    new_calculation = Calculation(
        operation=calc_data.operation,
        operand1=calc_data.operand1,
        operand2=calc_data.operand2,
        result=result,
        user_id=user_id
    )
    
    db.add(new_calculation)
    db.commit()
    db.refresh(new_calculation)
    
    return new_calculation


@router.patch("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(
    calculation_id: int,
    calc_update: CalculationUpdate,
    db: Session = Depends(get_db)
):
    """
    Edit an existing calculation.
    
    - **calculation_id**: The ID of the calculation to update
    - **operation**: New operation (optional)
    - **operand1**: New first operand (optional)
    - **operand2**: New second operand (optional)
    """
    # Find calculation
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    # Update fields if provided
    if calc_update.operation is not None:
        calculation.operation = calc_update.operation
    if calc_update.operand1 is not None:
        calculation.operand1 = calc_update.operand1
    if calc_update.operand2 is not None:
        calculation.operand2 = calc_update.operand2
    
    # Recalculate result
    try:
        calculation.result = calculate(
            calculation.operation,
            calculation.operand1,
            calculation.operand2
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    db.commit()
    db.refresh(calculation)
    
    return calculation


@router.delete("/{calculation_id}", response_model=MessageResponse)
def delete_calculation(calculation_id: int, db: Session = Depends(get_db)):
    """
    Delete a calculation by ID.
    
    - **calculation_id**: The ID of the calculation to delete
    """
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    db.delete(calculation)
    db.commit()
    
    return {"message": f"Calculation {calculation_id} deleted successfully"}
