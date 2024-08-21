from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from models import User, Payment, Offre, analyse  # Assurez-vous que tous les modèles nécessaires sont importés
from routers import auth,ocr, document, payment, offre, user,analyse  # Import du routeur user
import uvicorn

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Set up CORS
origins = [
    "http://localhost:3000",  # Frontend URL
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.websocket("/ws/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

app.include_router(auth.router, prefix="/auth")
app.include_router(offre.router, prefix="/offre")
app.include_router(payment.router, prefix="/payment")
app.include_router(user.router, prefix="/users")
app.include_router(analyse.router, prefix="/analyse", tags=["analyse"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Ayoub  FastAPI backend!"}\
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
