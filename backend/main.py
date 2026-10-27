from fastapi import FastAPI

app = FastAPI(
    title="Routine Tracker API",
    description="Backend API for Routine Tracker",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
