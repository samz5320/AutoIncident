# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Mount static files for CSS and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Mock database for incidents
INCIDENTS_DB = {
    1: {
        "title": "Service Outage",
        "status": "Resolved",
        "summary": "There was an outage affecting multiple services.",
        "start_time": "2024-11-03 08:00 AM",
        "end_time": "2024-11-03 09:30 AM",
        "before_image": "/static/images/before.jpg",
        "after_image": "/static/images/after.jpg"
    },
    2: {
        "title": "Degraded Performance",
        "status": "Ongoing",
        "summary": "System experiencing slower response times.",
        "start_time": "2024-11-04 02:00 PM",
        "end_time": None,
        "before_image": "/static/images/before.jpg",
        "after_image": "/static/images/after.jpg"
    },
    # Additional incidents can be added here
}

class Incident(BaseModel):
    title: str
    status: str
    summary: str
    start_time: str
    end_time: Optional[str]
    before_image: Optional[str]
    after_image: Optional[str]

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """
    Status Dashboard that lists all incidents with brief information
    """
    incidents = INCIDENTS_DB.values()
    return templates.TemplateResponse("dashboard.html", {"request": request, "incidents": incidents})

@app.get("/incident/{incident_id}", response_class=HTMLResponse)
async def read_incident(incident_id: int, request: Request):
    """
    Incident Details Page for a specific incident
    """
    incident = INCIDENTS_DB.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return templates.TemplateResponse("incident_details.html", {"request": request, "incident": incident})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)