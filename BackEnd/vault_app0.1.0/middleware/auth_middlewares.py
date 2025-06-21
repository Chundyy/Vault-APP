from fastapi import Request, HTTPException
from security.session_manager import verify_token


async def auth_middleware(request: Request):
    if request.url.path in ["/login", "/static"]:
        return

    token = request.cookies.get("session_token")
    if not token or not verify_token(token):
        raise HTTPException(
            status_code=401,
            detail="Não autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.user = verify_token(token)



