# Import required libraries
import os
import datetime
import ast
import uuid
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.bot.openai import openai_api
from app.bot.utils import get_similar_embeddings
from app.bot.utils import load_embeddings, prepare_chunks_dual_para
from app.schema import Question, Logs, Feedbacks, FeedBack
from app.crud import add_logs, add_feedback, update_feedback

# models.Base.metadata.create_all(bind=engine)


# Create FastAPI instance
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Predict route to display parsed results
async def discuss(question: Question, background_tasks: BackgroundTasks):
    # start_time = time.time()
    try:
        # if question.name not exist:
        # code here to added for creation of embeddings
        directory = os.getcwd()
        embeddings = load_embeddings(directory + '/app/embeddings/' + question.name + '.csv')#paul_english for now only
        embeddings['vector'] = embeddings['vector'].apply(ast.literal_eval)
        context_text, id_ps, source, similarity = get_similar_embeddings(question.question, embeddings)
        context_text = prepare_chunks_dual_para(context_text, source)
        source = ' '.join(source)
        question_id = uuid.uuid1()
        # context_text = prepare_chunks_dual_para(context_text)
        if context_text is not None:
            context = str(context_text[0])
            query_and_context = 'Context:\n' + context_text[0] + '\n\n Answer as Paul ' \
                                                                 'English.\n\n Question:' + question.question + '\n\n'
            answer, tokens = openai_api(query_and_context)
            if "Sorry, can't answer right now." in answer:
                for i in range(len(context_text)):
                    context = str(context_text[i])
                    if "Sorry, can't answer right now." in answer:
                        query_and_context = str('Context:\n' +
                                                context_text[i]) + '\n\n Answer as Paul English.' \
                                                                   '\n\nQuestion:' + question.question + '\n\n'
                        answer, tokens = openai_api(query_and_context)
                    else:
                        print("Complete Prompt: " + query_and_context)
            print('Question: ' + question.question + '\nContext IDs: ' + id_ps + '\n Similarity: ' + similarity +
                  '\nContext: ' + context + '\nContext Source: ' + source + '\nAnswer: ' + answer +
                  '\nEntity: ' + question.name)
            if 'Answer:' in answer:
                prefix, answer = answer.split('Answer:', 1)
            log_request = Logs(
                question_id=question_id,
                question=question.question,
                context_id=id_ps,
                context_source=source
                )
            #background_tasks.add_task(add_logs, log_request)
            default_feedback = Feedbacks(
                question_id=question_id,
                question=question.question,
                person=question.name,
                answer=answer
            )
            #background_tasks.add_task(add_feedback, default_feedback)

            return {'timestamp': datetime.datetime.now(),
                    "answer": answer,
                    "person_id": str(question.name),
                    "question_id": str(question_id)}
        else:
            print('Question: ' + question.question + ' No Context Found' + 'Entity:' + question.name)
            return {'timestamp': datetime.datetime.now(),
                    "answer": "Sorry! bot is yet to train more to answer this.",
                    "person_id": str(question.name),
                    "question_id": str(question_id)}
    except Exception as e:
        print('Question: ' + question.question + '\n\nError: ' + str(e))
        return {'timestamp': datetime.datetime.now(),
                'error': str(e),
                'TypeError': type(e).__name__,
                'error file': __file__,
                'error line': e.__traceback__.tb_lineno}


def feedback(feed_back: FeedBack):
    try:
        update_feedback(feed_back)
    except Exception as e:
        return {'timestamp': datetime.datetime.now(),
                'error': str(e),
                'TypeError': type(e).__name__,
                'error file': __file__,
                'error line': e.__traceback__.tb_lineno}


# Routes
# router = APIRouter(dependencies=[Depends(validate_auth)])
router = APIRouter()
router.add_api_route("/discuss", discuss, methods=["POST"])
router.add_api_route("/feedback", feedback, methods=["POST"])

app.include_router(router)
