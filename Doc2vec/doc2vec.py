import os
import gensim
from gensim.test.utils import get_tmpfile

def get_path_to_save_user_model() -> str:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_directory, "user_doc2vec_model")
    return model_path

def get_path_to_save_api_model() -> str:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_directory, "api_doc2vec_model")
    return model_path

def tagged_document(list_of_list_of_words):
    for i, list_of_words in enumerate(list_of_list_of_words):
        yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])

def getModel(type = 'api'):
    if type == 'api': return gensim.models.Doc2Vec.load(get_path_to_save_api_model())
    else: return gensim.models.Doc2Vec.load(get_path_to_save_user_model())

def getDatasetUser() -> list: 
    res = []
    with open("user_unique.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            string_data = line.strip('[]')
            string_data = string_data.replace("'", "")
            string_data = string_data.replace("]", "")
            string_data = string_data.replace("\n", "")
            data_list = string_data.split(", ")
            res.append(data_list)
    return res

def getDatasetAPI() -> list: 
    res = []
    with open("api_unique.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if '$' in line: continue
            string_data = line.replace("\n", "")
            data_list = string_data.split("/")
            res.append(data_list)
    return res


def train_model(dataset, type = 'api'):
    data = [d for d in dataset]
    data_for_training = list(tagged_document(data))
    model = gensim.models.doc2vec.Doc2Vec(vector_size=40, min_count = 2, epochs=30, window=5)
    model.build_vocab(data_for_training)
    model.train(data_for_training, total_examples=model.corpus_count, epochs=model.epochs)
    if type == 'api': model.save(get_tmpfile(get_path_to_save_api_model()))
    if type == 'user': model.save(get_tmpfile(get_path_to_save_user_model()))

if __name__ == '__main__':
    train_model(getDatasetUser(), 'user')
    train_model(getDatasetAPI(), 'api')
    print("Train model done!!")
    