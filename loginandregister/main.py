from fastapi import FastAPI, HTTPException
from mysql.connector import connect, Error
from pydantic import BaseModel


app = FastAPI()

db_config = {
    "host": "127.0.0.1",
    "user": "Login Name",
    "password": "BBIBBI",
    "database": "login",
}


class User(BaseModel):
    username: str
    password: str
    


def connect_db():
    try:
        conn = connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        return conn
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



@app.post("/register")
async def register(user: User):
  
    conn = connect_db()


    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (user.username, user.password))
            conn.commit()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "User registration is a success!"}


@app.post("/login")
async def login(user: User):
   
    conn = connect_db()

    try:
        
        with conn.cursor() as cursor:
            sql = "SELECT id FROM users WHERE username=%s AND password=%s"
            cursor.execute(sql, (user.username, user.password))
            result = cursor.fetchone()

        if result:
           
            return {"message": "Login is a success!"}
        else:
          
            raise HTTPException(status_code=401, detail="Incorrect input of username or password")

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
