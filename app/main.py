from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
#from models import * 
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware



from fastapi import Cookie
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from app.models.workout import Workout
from fastapi import Response,Request
#from app.main import app
from app.models.users import Accounts
import uvicorn

# from circles import *
# from check import *
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow everything for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#import pdb; pdb.set_trace()

app.mount("/static", StaticFiles(directory="app/static/images"), name="static")
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")



def render_html(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
    

def past_workouts(db: Session = Depends(get_db)):
    workout_detail = db.query(Workout).all()
    return workout_detail




@app.get("/login", response_class=HTMLResponse)
def show_form():
    return render_html('app/templates/login.html')

class UserLogin(BaseModel):
    username: str
    password: str


#import pdb; pdb.set_trace()
@app.post("/verify-login", response_model=None)
def verify_form(login: UserLogin, 
                response: Response,
                db: Session=Depends(get_db),
                ):
    
    res=db.query(Accounts).filter(login.username==Accounts.login_name).first()
    if res:
        response.set_cookie(key="auth_code", value="X#!@", httponly=True)
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")


def verify_access(auth_code: str = Cookie(None)):
    if auth_code != "X#!@":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/", response_class=HTMLResponse, dependencies=[Depends(verify_access)])
def show_form():
    #workouts = past_workouts(db)
    return render_html('app/templates/calendar.html')
                # #return templates.TemplateResponse(
    #     "calendar.html",
    #     {"request": request, "workouts": workouts}
    # )

#import requests
from fastapi.responses import FileResponse


@app.get("/upload-img")
def upload_img():
    #import pdb; pdb.set_trace()
    #image_url = "http://127.0.0.1:8000/static/download.jpg"
    # return FileResponse(
    #     "app/static/images/download.jpg",
    #     media_type="image/jpeg"
    # )
    import pdb; pdb.set_trace()
    return FileResponse(
        "app/static/images/test.csv",
        media_type="text/csv",
        filename="test.csv"
    )
    


# RAZORPAY_KEY_ID = "rzp_test_1234567890abcdef"       # replace with your Test Key ID
# RAZORPAY_KEY_SECRET = "your_secret_key_here"       # replace with your Test Key Secret

# client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# @app.get("/pay")
# def create_payment():
#     # Create an order of Rs.100 (amount is in paise)
#     order = client.order.create({
#         "amount": 10000,       # 100 INR
#         "currency": "INR",
#         "payment_capture": 1   # automatic capture
#     })

#     # Redirect URL to Razorpay checkout page
#     payment_url = f"https://checkout.razorpay.com/v1/checkout.js?order_id={order['id']}"

#     return RedirectResponse(url=payment_url)




from datetime import date

@app.get("/week-consistency")
def workouts(db: Session = Depends(get_db)):
    today = datetime.today().date()
    earlier_7_days = today - timedelta(days=7)
    workouts=past_workouts(db)
    #import pdb; pdb.set_trace()
    if not workouts:
        return 0

    count = 0
    for w in workouts:
        workout_date = datetime.strptime(w.date, "%Y-%m-%d").date()   
        #import pdb; pdb.set_trace()
        if workout_date >= earlier_7_days:
            count += 1
    print("Days worked:", count//7*100)
    #import pdb; pdb.set_trace()
    return round((count / 7) * 100, 2)


@app.get("/month-consistency")
def workouts(db: Session = Depends(get_db)):
    #import pdb; pdb.set_trace()
    today = date.today()
    month_start = date(today.year, today.month, 1)
    workouts=past_workouts(db)
    if not workouts:
        return 0

    count = 0
    for w in workouts:
        workout_date = datetime.strptime(w.date, "%Y-%m-%d").date()   
        #import pdb; pdb.set_trace()
        if workout_date >= month_start:
            count += 1
    print("Days worked:", count//7*100)
    #import pdb; pdb.set_trace()
    return round((count / 30) * 100, 2)
  

@app.get("/workouts")
def workouts(request: Request, db: Session = Depends(get_db)):
    workouts = past_workouts(db)
    return [
        {
            "date_": w.date,
        
        }
        for w in workouts
    ]
    
    #return render_html('templates.calendar.html')

#{date_: "2025-11-11", worked_out: true, intensity: 50}
from datetime import date

class WorkoutData(BaseModel):
    date_:date
    worked_out:bool
    intensity: int

from datetime import datetime

@app.post("/workout")
def workout_detail(workout: WorkoutData, db: Session = Depends(get_db)):

    try:
        #import pdb; pdb.set_trace()
        if workout.date_==datetime.now().date():
            today_workout=True

        if today_workout:
            workout_data=Workout(   
                                date= workout.date_,
                                did_workout= workout.worked_out,
                                intensity = workout.intensity

                                )
            #import pdb; pdb.set_trace()
            db.add(workout_data)
            db.commit()
            db.refresh(workout_data)
            return {"success": True}
        else:
            return HTTPException(404,detail="you can log today's workout.")
    except Exception as e:
        return {"detail": e}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)