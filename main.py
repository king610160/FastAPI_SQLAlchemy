from fastapi import FastAPI
from router.adminUser import router as adminUser_router
from router.login import router as login_router

# create FastAPI instance
app = FastAPI()

# to include related route from target modules
app.include_router(adminUser_router)
app.include_router(login_router)