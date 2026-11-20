from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from stories_site.api.check_file import cifar_app
from stories_site.database.db import engine
from stories_site.database.models import Base
from stories_site.api.crud import stories_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при старте (если они не созданы)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы в БД успешно созданы/проверены.")

    yield

    # Закрываем соединение с БД при завершении
    await engine.dispose()
    print("Соединение с БД закрыто.")


app = FastAPI(title="Group Service", lifespan=lifespan)
app.include_router(stories_router)
app.include_router(cifar_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)