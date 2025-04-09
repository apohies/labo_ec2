# app.py
from fastapi import FastAPI, HTTPException
from celery import Celery
from pydantic import BaseModel

# Crear la aplicación FastAPI
app = FastAPI(title="API Demo Celery")

# Configurar Celery para conectarse al Redis (en producción, cambiarás la IP)
celery_app = Celery(
    "worker_tasks",
    broker="redis://localhost:6379/0",  # En producción: redis://IP-DEL-WORKER:6379/0
    backend="redis://localhost:6379/0"  # En producción: redis://IP-DEL-WORKER:6379/0
)

# Modelo para la solicitud
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "API funcionando. Usa POST /send-message para enviar mensajes a Celery."}

@app.post("/send-message")
def send_message(request: MessageRequest):
    """
    Endpoint para enviar un mensaje al worker de Celery
    """
    try:
        # Enviar tarea al worker de Celery
        task = celery_app.send_task(
            "process_message",  # Nombre exacto de la tarea en el worker
            args=[request.message],
            kwargs={}
        )
        
        return {
            "status": "Mensaje enviado al worker",
            "task_id": task.id,
            "message": request.message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar mensaje: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)