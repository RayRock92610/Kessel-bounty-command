from enum import Enum
from fastapi import HTTPException, status, Depends
from app.models.domain import UserRole, User
from app.api.deps.auth import get_current_user

class Action(str, Enum):
    READ = "read"
    TRIAGE = "triage"
    ADMIN = "admin"

PERMISSION_MATRIX = {
    UserRole.ADMIN: [Action.READ, Action.TRIAGE, Action.ADMIN],
    UserRole.TRIAGER: [Action.READ, Action.TRIAGE],
    UserRole.RESEARCHER: [Action.READ]
}

def PermissionChecker(required_action: Action):
    def _check(current_user: User = Depends(get_current_user)):
        if required_action not in PERMISSION_MATRIX.get(current_user.role, []):
            raise HTTPException(status_code=403, detail="Kessel RL: Access Denied")
        return current_user
    return _check
