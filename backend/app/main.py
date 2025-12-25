"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.database import test_connection
from .api import auth, dashboard

# Создаем FastAPI приложение
app = FastAPI(
    title=settings.APP_NAME,
    description="Персонализированный дашборд с данными из PostgreSQL и Planfix",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Dashboard Service API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервиса"""
    db_status = test_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "service": settings.APP_NAME
    }


@app.on_event("startup")
async def startup_event():
    """Событие при запуске приложения"""
    print(f"🚀 Starting {settings.APP_NAME}...")
    print(f"📊 Database: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"🔗 Planfix API: {settings.PLANFIX_API_URL}")
    
    # Проверяем подключение к базе данных
    if test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")


@app.on_event("shutdown")
async def shutdown_event():
    """Событие при остановке приложения"""
    print(f"👋 Shutting down {settings.APP_NAME}...")


# Обработчик ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Глобальный обработчик ошибок"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


