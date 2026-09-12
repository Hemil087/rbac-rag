from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.repositories.organization_repository import get_organization_by_email_domain
from app.db.repositories.user_repository import get_user_by_org_and_email

def authenticate_user(db:Session,email:str,password:str):
    email = email.strip().lower()
    if '@' not in email : 
        return None
    email_domain = email.rsplit('@',1)[1]
    organization = get_organization_by_email_domain(db=db,email_domain=email_domain,)
    if organization is None:
        return None
    user = get_user_by_org_and_email(db=db, org_id=organization.id, email=email,)
    if user is None:
        return None
    if not verify_password(password,user.hashed_password,): 
        return None

    return user