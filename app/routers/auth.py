from fastapi import APIRouter, HTTPException

from app import auth, storage
from app.models import AuthResponse, LoginRequest, SignUpRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=201)
def sign_up(payload: SignUpRequest) -> AuthResponse:
    user = storage.create_user(payload.email, auth.hash_password(payload.password))
    return AuthResponse(
        access_token=auth.create_access_token(user["user_id"], user["email"]),
        user_id=user["user_id"],
        email=user["email"],
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    user = storage.get_user_by_email(payload.email)

    if user is None or not auth.verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return AuthResponse(
        access_token=auth.create_access_token(user["user_id"], user["email"]),
        user_id=user["user_id"],
        email=user["email"],
    )
