from fastapi import FastAPI
from pygments.lexers import q

from app.routers import auth, users, weather
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth-API",
              description='API documentation',
              version='1.0',
              contact={
                  "name": "developer",
                  "email": "wicaszmakowizer@gmail.com"
              })

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://0.0.0.0:8000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(weather.router)


from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static",html=True), name="static")

@app.get("/")
def index():
    return {"pong": True}

