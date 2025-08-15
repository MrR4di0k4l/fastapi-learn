from fastapi import FastAPI, Query, status, Depends, HTTPException, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import random
from typing import Optional
from typing import List

from contextlib import asynccontextmanager
from schemas import ItemCreateSchemas, ItemResponseSchemas, ItemUpdateSchemas
from sqlalchemy.orm import Session
from database import get_db, Base, engine  # وارد کردن تابع get_db از database.py
from models import User  # فرض کنید مدل User از قبل در models.py تعریف شده است


@asynccontextmanager
async def lifespan(app: FastAPI):
    # عملیات‌های شروع
    print("Application startup")
    # Base.metadata.create_all(bind=engine)
    # مثلاً: اتصال به دیتابیس یا مقداردهی کش
    yield  # این خط اجرای برنامه را به اپلیکیشن می‌دهد

    # عملیات‌های پایان
    print("Application shutdown")
    # مثلاً: بستن اتصال به دیتابیس یا پاک‌سازی منابع

app = FastAPI(lifespan=lifespan)

names_db = [
    {
        "id": 1,
        "name": "ali"
    },
    {
        "id": 2,
        "name": "maryam"
    },
    {
        "id": 3,
        "name": "arousha"
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/names")
# def names_list():
#     return names_db

# @app.get("/names")
# def names_list(q: str | None = None):
#     if q:
#         filtered_names = [name for name in names_db if q.lower() in name["name"].lower()]
#         return filtered_names
#     return names_db


@app.get("/names", response_model=List[ItemResponseSchemas])
def names_list(q: Optional[str] = Query(None, max_length=50, pattern='^[^0-9]*$'), db: Session = Depends(get_db)):
    query = db.query(User)
    if q:
        query.filter_by(name=q)
    result = query.all()
    return result
        # result = [name for name in names_db if q.lower() in name["name"].lower()]
        # return [name for name in names_db if q.lower() in name["name"].lower()]
    # return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@app.get("/names/{name_id}", response_model=ItemResponseSchemas)
def names_detail(name_id: int = Path(description="The id of the item to get", pattern='^[1-9]+[0-9]*$')):
    for name in names_db:
        if name["id"] == name_id:
            return name
            # return JSONResponse(content=name, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


# @app.post("/names", status_code=status.HTTP_201_CREATED)
# def names_create(name: str = Form()):
#     new_name = {"id": random.randint(6,1000), "name": name}
#     names_db.append(new_name)
#     return JSONResponse(content=new_name, status_code=status.HTTP_201_CREATED)
@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=ItemResponseSchemas)
def names_create(item: ItemCreateSchemas, db: Session = Depends(get_db)):
    # new_name = {"id": random.randint(6,1000), "name": item.name}
    new_name = User(name=item.name, age=item.age)
    db.add(new_name)
    db.commit()
    return new_name
    # return JSONResponse(content=new_name, status_code=status.HTTP_201_CREATED)


@app.put("/names/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponseSchemas)
# def names_update(item_id: int = Path(), name: str = Form()):
def names_update(item: ItemUpdateSchemas, item_id: int = Path(), db: Session = Depends(get_db)):
    # for n in names_db:
    #     if n["id"] == item_id:
    #         n["name"] = item.name
    #         return n
    person = db.query(User).filter_by(id=item_id).one_or_none()
    if person:
        person.name = item.name
        person.age = item.age
        db.commit()
        db.refresh(person)
        return person
            # return JSONResponse(content={"message": f"Name with ID {item_id} updated successfully"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/names/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def names_delete(item_id: int, db: Session = Depends(get_db)):
    # for i, n in enumerate(names_db):
    #     if n["id"] == item_id:
    #         del names_db[i]
    #         # names_db.remove(n)
    #         return JSONResponse(content={"message": f"Name with ID {item_id} deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)
    person = db.query(User).filter_by(id=item_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@app.post("/upload/")
async def upload_file(file: bytes = File(...)):
    # طول داده‌های فایل را چاپ می‌کنیم
    return {"file_size": len(file)}


@app.post("/uploadfile2/")
async def upload_file2(file: UploadFile):
    # اطلاعات فایل را می‌خوانیم
    content = await file.read()
    print(file.__dict__)
    return {"filename": file.filename, "content_type": file.content_type, "file_size": len(content)}


@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)