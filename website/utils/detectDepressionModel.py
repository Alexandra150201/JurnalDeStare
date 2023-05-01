import numpy as np
import pickle
from keras.models import load_model
from keras.utils import pad_sequences
import  re

class DepressionDetector:

    __max_sequence_length = 300

    @staticmethod
    def __clean_text(s):
        s = re.sub(r'http\S+', '', s)
        s = re.sub('(RT|via)((?:\\b\\W*@\\w+)+)', ' ', s)
        s = re.sub(r'@\S+', '', s)
        s = re.sub('&amp', ' ', s)
        s = re.sub(r'[^a-zA-Z]',' ',s)
        s = re.sub(r'-{2,}\s',' ',s)
        return s

    @staticmethod
    def __get_stopwords_list(stop_file_path):
        """load stop words """
        with open(stop_file_path, 'r', encoding="utf-8") as f:
            stopwords = f.readlines()
            stop_set = set(m.strip() for m in stopwords)
            return list(frozenset(stop_set))

    @staticmethod
    def detectDepressionFromText(text):
        model= load_model('website/utils/modelRomanian.h5')
        stop_words = DepressionDetector.__get_stopwords_list('website/utils/romanian.txt')

        with open('website/utils/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        text = DepressionDetector.__clean_text(text)
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in stop_words])
        print(text)
        new_text_seq = tokenizer.texts_to_sequences(text)
        new_text_seq_padded = pad_sequences(new_text_seq, maxlen=DepressionDetector.__max_sequence_length)
        print(new_text_seq_padded)

        y_pred = model.predict([new_text_seq_padded, new_text_seq_padded])
        print('Predicted Target:', y_pred[0])
        y_pred = np.round(y_pred).flatten()
        print('Predicted Target:', y_pred[0])
        if(y_pred[0]==0.0):
            return 'depressed'
        else:
            return 'non-depressed'
