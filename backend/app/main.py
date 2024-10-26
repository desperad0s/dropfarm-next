from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import automation
from .core.browser import browser_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await browser_manager.start()

@app.on_event("shutdown")
async def shutdown():
    await browser_manager.cleanup()

# Include routers
app.include_router(automation.router, prefix="/api/automation", tags=["automation"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}