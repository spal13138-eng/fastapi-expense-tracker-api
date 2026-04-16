from app.database import get_db
from app import models,schemas
from fastapi import FastAPI,HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import oauth2
from datetime import date,datetime
from sqlalchemy import func,extract

router=APIRouter(
    prefix="/expense",
    tags=["Expenses"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def postexpense(expense:schemas.ExpenseCreate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    new_expense=models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        owner_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/",response_model=list[schemas.ExpenseResponse])
def getAllExpense(limit:int=10,offset:int=0,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    

    expense=db.query(models.Expense).filter(models.Expense.owner_id==current_user.id)\
    .order_by(models.Expense.created_at.desc())\
    .offset(offset)\
    .limit(limit)\
    .all()

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="do not have any expense")
    

    return expense

# get daily expenditure

@router.get("/daily-expense",response_model=schemas.DailyExpense)
def getDailyExpense(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    
    today=date.today()
    total = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.owner_id == current_user.id,
        func.date(models.Expense.created_at) == today
    ).scalar()
    

    return {
        "date":str(today),
        "total_expense": total or 0
    }

# get monthly expenditure

@router.get("/monthly-expense",response_model=schemas.MonthlyExpense)
def getMonthlyExpense(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    today=datetime.today()
    month=today.month
    year=today.year

    total=db.query(func.sum(models.Expense.amount)).filter(models.Expense.owner_id==current_user.id,
                   extract("month",models.Expense.created_at)==month,
                   extract("year",models.Expense.created_at)==year).scalar()

    return {
        "month":month,
        "year":year,
        "total_expense":total or 0
    }


@router.get("/category/{category}",response_model=schemas.CategorywiseExpense)
def getCategoryWise(category:str,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    
    total=db.query(func.sum(models.Expense.amount)).filter(models.Expense.owner_id==current_user.id,models.Expense.category==category).scalar()

    if total is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You have no expenses on {category}")
    
    return {
        "category":category,
        "total_expense":float(total or 0)
    }

#category wise highest expenditure

@router.get("/highest-expense/{category}",response_model=schemas.highestExpense)
def highestExpense(category:str,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    
    highest_expense=db.query(models.Expense.amount).filter(models.Expense.owner_id==current_user.id,models.Expense.category==category)\
    .order_by(models.Expense.amount.desc()).first()


    return{
        "category":category,
        "highestExpense":highest_expense[0]
    }

#category wise lowest expenditure

@router.get("/lowest-expense/{category}",response_model=schemas.lowestExpense)
def highestExpense(category:str,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    
    lowest_expense=db.query(models.Expense.amount).filter(models.Expense.owner_id==current_user.id,models.Expense.category==category)\
    .order_by(models.Expense.amount.asc()).first()


    return{
        "category":category,
        "lowestExpense":lowest_expense[0]
    }

@router.get("/{id}",response_model=schemas.ExpenseResponse)
def getExpensebyId(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
     expense=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id).first()

     if expense is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="expense is not found")
     
     return expense

@router.put("/{id}")
def UpdateExpense(id:int,UpdateExpense:schemas.ExpenseUpdate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    expense=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id)

    if expense.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="expense is not found")
    
    expense.update({
        "title":UpdateExpense.title,
        "amount":UpdateExpense.amount,
        "category":UpdateExpense.category,
        "description":UpdateExpense.description
    })

    db.commit()

    return {"Expense with is Updated Successfully"}


@router.delete("/{id}")
def deleteExpense(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    expense=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id)

    if expense.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="expense is not found")
    
    expense.delete(synchronize_session=False)

    db.commit()
    return {"Expense  is successfully deleted"}