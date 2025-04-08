from backend.database import db
from backend.models.user_log import UserLog
from backend.models.user import User

def log_user_action(user_id, action_text):
    try:
        new_log = UserLog(user_id=user_id, action=action_text)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        print(f"Log Insert Failed: {e}")
        db.session.rollback()

def get_recent_logs_for_org(organization_id, limit=5):
    logs = (
        db.session.query(UserLog, User.username)
        .join(User, User.user_id == UserLog.user_id)
        .filter(User.organization_id == organization_id)
        .order_by(UserLog.timestamp.desc())
        .limit(limit)
        .all()
    )

    result = []
    for log, username in logs:
        result.append({
            'log_id': log.log_id,
            'action': log.action,
            'timestamp': log.timestamp,
            'username': username
        })
    return result
