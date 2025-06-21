from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from db.database import conectar_bd
from security.auth import verify_password
from fastapi.responses import HTMLResponse
from security.session_manager import generate_session_token
from controllers.auth_controller import AuthController
from middlewares.auth_middleware import auth_middleware

app = FastAPI()
app.middleware("http")(auth_middleware)

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Configuração de templates
templates = Jinja2Templates(directory="frontend/templates")

# Rota para favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("frontend/static/favicon.ico")

# Rota principal que renderiza login.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota alternativa para /login (se necessário)
@app.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def handle_login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    try:
        # Normalização e limpeza dos inputs
        username = username.strip().lower()
        password = password.strip()

        print(f"\n[DEBUG] Tentativa de login para: {username}")  # Log detalhado

        # Conexão com o banco de dados
        conn = conectar_bd()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT id, username, password_hash, email FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()

            if not user:
                print(f"[DEBUG] Usuário não encontrado: {username}")
                raise ValueError("Credenciais inválidas")

            print(f"[DEBUG] Usuário encontrado: ID {user['id']}")
            print(f"[DEBUG] Hash armazenado: {user['password_hash']}")

            # Verificação detalhada da senha
            is_valid = verify_password(user['password_hash'], password)
            print(f"[DEBUG] Resultado da verificação: {'VÁLIDO' if is_valid else 'INVÁLIDO'}")

            if is_valid:
                # Autenticação bem-sucedida
                response = RedirectResponse("/dashboard", status_code=303)

                # Configuração de sessão segura
                session_token = generate_session_token(user['id'])
                response.set_cookie(
                    key="session_token",
                    value=session_token,
                    httponly=True,
                    secure=True,  # Apenas HTTPS em produção
                    samesite="Lax",
                    max_age=3600  # Expira em 1 hora
                )

                print(f"[DEBUG] Login bem-sucedido para {username}")
                return response

            raise ValueError("Credenciais inválidas")

    except ValueError as e:
        print(f"[ERRO] Falha de autenticação: {str(e)}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciais inválidas"},
            status_code=401
        )
    except Exception as e:
        print(f"[ERRO CRÍTICO] {str(e)}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Erro interno do servidor"},
            status_code=500
        )
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session_token")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)