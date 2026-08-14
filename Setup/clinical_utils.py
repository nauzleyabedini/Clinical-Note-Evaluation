import os
import pandas as pd
import time
import random
from anthropic import Anthropic, APIStatusError, OverloadedError
from anthropic.types import TextBlock
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from openai import OpenAI, RateLimitError, APIError

def setup_clients(anthropic_key, openai_key, gemini_key):
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["GEMINI_API_KEY"] = gemini_key

    genai.configure(api_key=gemini_key)

    anthropic_client = Anthropic()
    openai_client = OpenAI()
    gemini_model = genai.GenerativeModel('gemini-3.6-flash')

    print("APIs successfully initialized.")
    return anthropic_client, openai_client, gemini_model

def load_aci_bench():
    url = "https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/refs/heads/main/data/aci-bench/challenge_data/train.csv"
    df = pd.read_csv(url)
    print(f"Successfully loaded {len(df)} encounter records from ACI-BENCH.")
    return df.copy()
