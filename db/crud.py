from sqlalchemy.orm import Session
from .models import Vulnerability, UserSettings

def get_vulnerabilities(db: Session):
    return db.query(Vulnerability).all()

def get_user_settings(db: Session, user_id: int):
    return db.query(UserSettings).filter(UserSettings.user_id == user_id).first()

def update_user_settings(db: Session, user_id: int, settings):
    user_settings = get_user_settings(db, user_id)
    if user_settings:
        for key, value in settings.items():
            setattr(user_settings, key, value)
    else:
        user_settings = UserSettings(user_id=user_id, **settings)
        db.add(user_settings)
    db.commit()
    db.refresh(user_settings)
    return user_settings
