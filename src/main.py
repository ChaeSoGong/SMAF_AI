# hook
import uvicorn
from starlette.middleware.cors import CORSMiddleware
# from src.hook.CreateTaskExecutor import CreateTaskExecutor
from src.hook.saveVoice import SaveVoiceAPI
from fastapi import FastAPI

app = FastAPI()
app.include_router(SaveVoiceAPI.router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요에 따라 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=5000)
#     completion_executor = CreateTaskExecutor()
#     response_text = completion_executor.execute()
#     print(response_text)

if __name__ == '__main__':
   main()