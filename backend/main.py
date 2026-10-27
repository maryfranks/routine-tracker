from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import auth, clock, views, tasks, history, utilities

app = FastAPI(
    title="Routine Tracker API",
    description="Backend API for Routine Tracker",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "message": "Invalid request input"},
    )


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(auth.router)
app.include_router(clock.router)
app.include_router(views.router)
app.include_router(tasks.router)
app.include_router(history.router)
app.include_router(utilities.router)
