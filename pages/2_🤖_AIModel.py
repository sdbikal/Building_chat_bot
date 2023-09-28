import streamlit as st
from transformers import BertTokenizer
from keras.models import load_model
import numpy as np 
from keras import backend as K
import tensorflow as tf
from predic import *

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
new_text = st.session_state['uploaded_text']


if "result" not in st.session_state:
    st.session_state.result = None

# with st.sidebar:
#         if st.button("Progress"):
#             with st.spinner("Progressing"):

encoded_text = tokenizer.encode_plus(
                    new_text,
                    add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
                    max_length=512,  # Max length to truncate/pad
                    return_attention_mask=True,  # Construct attention masks
                    return_tensors='tf',  # Return as TensorFlow tensors
                    truncation=True,  # Explicitly truncate to max length
                    padding='max_length'  # Pad to max length
                )
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']
                
st.session_state['result'] = predict(input_ids)               

st.write("Result:",st.session_state['result'])
