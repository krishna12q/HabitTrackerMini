from fastapi import FastAPI, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Point FastAPI to the templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Pass request as the first parameter or as a keyword argument
    return templates.TemplateResponse(
        request=request, 
        name="tracker.html", 
        context={
            "habits": {
                "gym": {
                    "icon": "💪",
                    "color": "blue",
                    "completed": [
                        "2026-08-01T18:30:00",
                        "2026-08-03T07:45:00",
                        "2026-08-05T19:10:00"
                    ]
                },
                "reading": {
                "icon": "📚",
                "color": "yellow",
                "completed": [
                    "2026-08-02T20:30:00",
                    "2026-08-04T21:00:00"
                ]
    }
  }
}
    )


