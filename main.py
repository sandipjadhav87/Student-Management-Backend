from fastapi import FastAPI,HTTPException   #not importing whole library, just FastAPI class
import psycopg2

app=FastAPI()
connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='8767485861'
)
cursor = connection.cursor()
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