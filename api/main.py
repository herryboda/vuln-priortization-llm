from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from db.init_db import get_db
from db import crud
from models.prioritize_model import prioritize_vulnerabilities
from utils.notifications import send_slack_alert, send_email_alert

app = FastAPI()

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Process CSV file
    data = await file.read()
    vulnerabilities = process_csv_data(data)
    for vuln in vulnerabilities:
        crud.add_vulnerability(db, vuln)
    return {"status": "CSV uploaded successfully"}

@app.get("/prioritize")
async def prioritize(db: Session = Depends(get_db)):
    vulnerabilities = crud.get_vulnerabilities(db)
    prioritized_vulns = prioritize_vulnerabilities(vulnerabilities)
    return prioritized_vulns

@app.post("/update-settings")
async def update_settings(user_id: int, cvss_weight: float, exploitability_weight: float, reachability_weight: float, db: Session = Depends(get_db)):
    settings = {"cvss_weight": cvss_weight, "exploitability_weight": exploitability_weight, "reachability_weight": reachability_weight}
    updated_settings = crud.update_user_settings(db, user_id, settings)
    return {"status": "Settings updated", "settings": updated_settings}

@app.post("/send-alerts")
async def send_alerts(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    vulnerabilities = crud.get_vulnerabilities(db)
    high_priority = [vuln for vuln in vulnerabilities if vuln.priority_score > 8.0]
    background_tasks.add_task(send_slack_alert, high_priority)
    background_tasks.add_task(send_email_alert, high_priority)
    return {"status": "Alerts sent"}
