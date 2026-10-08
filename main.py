from fastapi import FastAPI,HTTPException   #not importing whole library, just FastAPI class
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allows all request
    allow_credentials=False,          # Allows cookies and authentication headers
    allow_methods=["*"],             # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],             # Allows all custom and standard HTTP headers
)
# connection = psycopg2.connect(
#     host=os.getenv('DB_HOST'),
#     port=os.getenv('DB_PORT'),
#     database=os.getenv('DB_DATABASE'),
#     user=os.getenv('DB_USER'),
#     password=os.getenv('DB_PASS')
# )
connection = psycopg2.connect('postgresql://neondb_owner:npg_JhfjA1lNcG9S@ep-withered-tooth-b3xk3q0a-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')


class Student(BaseModel):
    id: int = None
    name: str = None
    course: str = None

#get all Students
@app.get('/students')#@app is decorator and /student is api endpoint
def get_all_students():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM students')
    rows=cursor.fetchall()     #it returns list of tuple consist of row by row 
    result=[]
    for row in rows:
        result.append({
            'id':row[0],
            'name':row[1],
            'course':row[2]
        })
    cursor.close()
    return result

#Get single student
@app.get('/students/{id}')
def get_single_student(id: int):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students WHERE id=%s',(id,))
        row=cursor.fetchone()
        cursor.close()
        return{
            'id':row[0],
            'name':row[1],
            'course':row[2]
        }
    except:
        cursor.close()
        raise HTTPException(status_code=404,detail='Inavalid Student id')

# create student record
@app.post('/students')
def create_student_record(student: Student):
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students VALUES (%s,%s,%s)',(student.id,student.name,student.course))
        connection.commit()
        cursor.close()
        raise HTTPException(status_code=201,detail='Student record created successfully')
        
    except psycopg2.IntegrityError:
        cursor.close()
        connection.rollback()
        raise HTTPException(status_code=404,detail='Student id allready exist')

#update student record
@app.put('/students/{id}')
def update_student_record(student:Student,id:int):
    cursor = connection.cursor()
    cursor.execute('UPDATE students SET id=%s, name=%s,course=%s WHERE id=%s',(student.id,student.name,student.course,id))
    if(cursor.rowcount == 0):
            raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    cursor.close()
    raise HTTPException(status_code=200,detail='Student record update successfully')
   

#Partial Update 
@app.patch('/students/{id}')
def partial_update(id:int,student:Student):
    cursor = connection.cursor()
    if(student.id != None):
        cursor.execute('UPDATE students SET id=%s WHERE id=%s',(student.id,id))
    if(student.name != None):
        cursor.execute('UPDATE students SET name=%s WHERE id=%s',(student.name,id))
    if(student.course != None):
        cursor.execute('UPDATE students SET course=%s WHERE id=%s',(student.course,id))
    if(cursor.rowcount == 0):
        cursor.close()
        raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    cursor.close()
    raise HTTPException(status_code=200,detail='Partially update successfully')


#Delete student record
@app.delete('/students/{id}')
def delete_student_record(id:int):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM students WHERE id=%s',(id,))
    if(cursor.rowcount == 0):
         cursor.close()
         raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    cursor.close()
    raise HTTPException(status_code=200,detail='Record delete Successfully')