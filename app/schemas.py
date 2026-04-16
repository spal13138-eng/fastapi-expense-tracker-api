from pydantic import BaseModel
from datetime import datetime,date
from typing import Optional,Annotated
today=datetime.today()
month=today.month


class ExpenseResponse(BaseModel):
    id:int
    title:str
    amount:float
    category:str
    description:str
    created_at:datetime

    class Config:
        from_attributes=True


class ExpenseCreate(BaseModel):
    title:str
    amount:float
    category:str
    description:str
    class Config:
     from_attributes=True


class ExpenseUpdate(BaseModel):
    title:str
    amount:float
    category:str
    description:str

    class Config:
        from_attributes=True


class UserRegister(BaseModel):
    email:str
    password:str
    class Config:
        from_attributes=True

class UserOut(BaseModel):
    id:int
    email:str
    created_at:datetime     
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email:str
    password:str
    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token:str  
    token_type:str      

class Token_data(BaseModel):
    id:Optional[int]=None

class DailyExpense(BaseModel):
    date:str
    total_expense:float  
    class Config:
        from_attributes=True
class MonthlyExpense(BaseModel):
    month:int
    year:int
    total_expense:float 
    class Config:
        from_attributes=True

class CategorywiseExpense(BaseModel):
    category:str
    total_expense:float
    class config:
        from_attributes=True

class highestExpense(BaseModel):
    category:str
    highestExpense:float
    class config:
        from_attributes=True

class lowestExpense(BaseModel):
    category:str
    lowestExpense:float
    class config:
        from_attributes=True

