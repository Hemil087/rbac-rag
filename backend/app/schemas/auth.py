from pydantic import BaseModel,EmailStr

class LoginRequest(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str

class CurrentUser(BaseModel):
    user_id: int
    org_id: int
    role_id: int
