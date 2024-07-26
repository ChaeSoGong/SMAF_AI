# hook
from starlette.middleware.cors import CORSMiddleware
from src.hook.saveVoice import SaveVoiceAPI
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(SaveVoiceAPI.router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요에 따라 변경
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
   uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
   main()




