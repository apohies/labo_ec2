# worker.py
from celery import Celery
import time

# Configurar Celery (usando Redis como broker)
app = Celery(
    "worker_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Configuración opcional
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@app.task(name="process_message")
def process_message(message):
    """
    Tarea simple que recibe un mensaje y lo procesa
    En un caso real, aquí se procesaría el video
    """
    print(f"Recibido mensaje: {message}")
    print("Procesando...")
    
    # Simulamos un procesamiento que toma tiempo
    time.sleep(2)
    
    result = f"¡Mensaje procesado!: {message}"
    print(result)
    
    return result

if __name__ == "__main__":
    app.start()