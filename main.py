from fastapi import FastAPI,HTTPException   #not importing whole library, just FastAPI class
import psycopg2
from pydantic import BaseModel

app=FastAPI()
connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='8767485861'
)
cursor = connection.cursor()

class Student(BaseModel):
    id: int = None
    name: str = None
    course: str = None

#get all Students
@app.get('/students')#@app is decorator and /student is api endpoint
def get_all_students():
    cursor.execute('SELECT * FROM students')
    rows=cursor.fetchall()     #it returns list of tuple consist of row by row 
    result=[]
    for row in rows:
        result.append({
            'id':row[0],
            'name':row[1],
            'course':row[2]
        })
    return result

#Get single student
@app.get('/students/{id}')
def get_single_student(id: int):
    try:
        cursor.execute('SELECT * FROM students WHERE id=%s',(id,))
        row=cursor.fetchone()
        return{
            'id':row[0],
            'name':row[1],
            'course':row[2]
        }
    except:
        raise HTTPException(status_code=404,detail='Inavalid Student id')

# create student record
@app.post('/students')
def create_student_record(student: Student):
    try:
        cursor.execute('INSERT INTO students VALUES (%s,%s,%s)',(student.id,student.name,student.course))
        connection.commit()
        raise HTTPException(status_code=201,detail='Student record created successfully')
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=404,detail='Student id allready exist')

#update student record
@app.put('/students/{id}')
def update_student_record(student:Student,id:int):
    cursor.execute('UPDATE students SET id=%s, name=%s,course=%s WHERE id=%s',(student.id,student.name,student.course,id))
    if(cursor.rowcount == 0):
            raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    raise HTTPException(status_code=200,detail='Student record update successfully')
   

#Partial Update 
@app.patch('/students/{id}')
def partial_update(id:int,student:Student):
    if(student.id != None):
        cursor.execute('UPDATE students SET id=%s WHERE id=%s',(student.id,id))
    if(student.name != None):
        cursor.execute('UPDATE students SET name=%s WHERE id=%s',(student.name,id))
    if(student.course != None):
        cursor.execute('UPDATE students SET course=%s WHERE id=%s',(student.course,id))
    if(cursor.rowcount == 0):
        raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    raise HTTPException(status_code=200,detail='Partially update successfully')

@app.delete('/students/{id}')
def delete_student_record(id:int):
    cursor.execute('DELETE FROM students WHERE id=%s',(id,))
    if(cursor.rowcount == 0):
         raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    raise HTTPException(status_code=200,detail='Record delete Successfully')