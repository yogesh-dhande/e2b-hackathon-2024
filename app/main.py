from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import models, crud, database, schemas
from fastapi.responses import RedirectResponse

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="app/templates")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create the database tables at startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

# Dependency for getting the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db=db)  # Fetch items from the database
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

# Modify this function to accept form data
@app.post("/items/lost/")
def report_lost_item(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    lost_date: str = Form(...),
    db: Session = Depends(get_db)
):
    item_data = schemas.LostItemCreate(
        name=name,
        description=description,
        location=location,
        lost_date=lost_date
    )
    crud.create_lost_item(db=db, item=item_data)
    return RedirectResponse(url="/", status_code=303)

@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db=db)
