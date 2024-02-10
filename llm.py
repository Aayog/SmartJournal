from langchain_community.llms import Ollama
from JournalAnalysis.models import JournalEntryAnalysis
from pydantic import BaseModel
from pydantic import TypeAdapter
import json

# llm = Ollama(base_url='http://localhost:11434', model='mistral')
llm = Ollama(base_url='http://172.22.32.123:11434/', model='mistral')
question = """
how would you prse this data in python into an object defined as JournalEntryAnalysis:
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
"""
print(llm.invoke(question))