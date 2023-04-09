import os
import fitz
import torch
import openai
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
#sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
openai.api_key = os.environ.get("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"


def get_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n\n".join([page.get_text() for page in doc])
    text_data = text.split('\n\n')
    return text_data


def get_token(documents):
    sentences = [documents]
#    sentence_embeddings = sbert_model.encode(sentences, convert_to_tensor=True)
    encod_np_array = np.array(sentence_embeddings)
    encod_list = encod_np_array.tolist()
    return encod_list[0]


def get_embedding_list(text):
    df = pd.DataFrame(text, columns=["text"])
    df['text'] = df['text'].str.lower()
    df['vector'] = df['text'].apply(get_token)
    return df


def get_embedding_from_csv(file):
    df = pd.read_csv(file)
    df['text'].str.lower()
    df['vector'] = df['text'].progress_apply(get_embedding)
    return df


def get_embedding(text):
    result = openai.Embedding.create(
      model=EMBEDDING_MODEL,
      input=text
    )
    return result["data"][0]["embedding"]


def get_similar_embeddings(query, df):
    context_text = []
    id_ps = ""
    source = []
    similarity = ""
    query = query.lower()
    query_embedding = get_embedding(query)
    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, df['vector'].tolist())[0]
    top_results = torch.topk(cos_scores, k=30)
    similarity += str(top_results[0])
    for idx in top_results[1]:
        context_text.append(df.iloc[int(idx), 0])
        source.append(df.iloc[int(idx), 1])
        id_ps += str(int(idx)) + ', '
    return context_text, id_ps, source, similarity


def load_embeddings(fname):
    """
    Read the document embeddings and their keys from a PKL.
    
    """
    
    df = pd.read_csv(fname, index_col=0)
    return df


def prepare_chunks(lst):
    returned_list = []
    chunk = ""
    for i in range(len(lst)):
        chunk = chunk + ' ' + lst[i]
        if len(chunk + ' ' + lst[i]) > 500:
            returned_list.append(chunk)
            chunk = ""
    return returned_list


def modify_context_order(context, source):
    wiki = []
    pme = []
    book = []
    podcasts = []
    for i in range(0, len(context)):
        if source[i] == 'Wikipedia':
            print("Wikipedia")
            wiki.append(context[i])
        elif source[i] == 'Others':
            pme.append(context[i])
        elif source[i] == 'book':
            book.append(context[i])
        elif source[i] == 'podcasts':
            podcasts.append(context[i])
    return wiki + pme + book + podcasts


def prepare_chunks_dual_para(context, src):
    context = modify_context_order(context, src)
    returned_list = []
    chunk = str(context[0])
    index = 1
    for i in range(1, len(context)):
        if len(chunk + ' ' + context[i]) > 3000 or index == 10:
            returned_list.append(chunk)
            index = 1
            chunk = context[i]
        else:
            chunk = chunk + ' ' + context[i]
            index += 1
    return returned_list

# def create_embeddings(file, name):
#     text = get_text_from_pdf(file)
#     embeddings = get_embedding_list(text)
#     embeddings.to_pickle(name+'.pkl')
