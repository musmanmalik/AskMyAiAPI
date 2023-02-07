# Import required libraries
import time
import datetime
from fastapi import FastAPI, Body, APIRouter, Depends, BackgroundTasks
from personalities.database import add_error, add_personality, is_persnality_exist
from personalities.models import Question
#from auth import validate_auth



# Create FastAPI instance
app = FastAPI()


# Predict route to display parsed results
async def discuss(question: Question ,background_tasks: BackgroundTasks):
    #start_time = time.time()
    try:
        personality = {'timestamp': datetime.datetime.now(),
                        'name': question.name, 
                        'personality_id': question.person_id}
        if not is_persnality_exist(question.person_id):
            print("is_persnality_exist(question.person_id) is None")

            background_tasks.add_task(add_personality, personality)
        return {"Answer": "The bot for " + question.name + " is in progress", 
                "person_id": str(question.person_id),
                "question_id": str(question.question_id),
                "session_id": str(question.session_id)
        }
    except Exception as e:

        logging_info = {'timestamp': datetime.datetime.now(),
                        'Error': str(e), 'TypeError': type(e).__name__,
                        'ErrorFile': __file__, 'ErrorLine': e.__traceback__.tb_lineno}
        background_tasks.add_task(add_error, logging_info)

        return {'Error': str(e),
               'TypeError': type(e).__name__,
               'Error File': __file__,
               'Error Line': e.__traceback__.tb_lineno}


# Routes
#router = APIRouter(dependencies=[Depends(validate_auth)])
router = APIRouter()
router.add_api_route("/discuss", discuss, methods=["POST"])
app.include_router(router)


import uvicorn
if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8002)
