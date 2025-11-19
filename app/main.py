from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
#from models import * 
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from app.models.workout import Workout
from fastapi import Response,Request
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

app.mount("/static", StaticFiles(directory="static"), name="static")
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")



def render_html(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
    

def past_workouts(db: Session = Depends(get_db)):
    workout_detail = db.query(Workout).all()
    return workout_detail


@app.get("/", response_class=HTMLResponse)
def show_form():
    #workouts = past_workouts(db)
    return render_html('templates/calendar.html')
                # #return templates.TemplateResponse(
    #     "calendar.html",
    #     {"request": request, "workouts": workouts}
    # )



from datetime import date

@app.get("/week")
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


