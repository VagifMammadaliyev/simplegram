from app.core import initialize_application
from app.endpoints.urls import api_router

app = initialize_application()
app.include_router(api_router)
