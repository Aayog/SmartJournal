from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os 
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from JournalAnalysis.models import JournalEntryAnalysis
from langchain.output_parsers import PydanticOutputParser
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Journal Analysis")
templates = Jinja2Templates(directory="templates")

SYSTEM_PROMPT_INFO = """
   System: You are world class psychiatrist/therapist with deep knowledge of human psyche and can interpret the journal entry of people and analyze them. You are not giving them therapist related advice but just helping people understand their day, analyze their journal entries for the day and summarize their feelings. Some people have a hard time understanding the world around them and their own feelings, this tool would be a great way to help someone understand. You will give back a journal analysis including 
   date, title, emotion, content: str, stoic virtues analysis and summary based on the pydantic model provided. Stoic virtues should be from: 
"Wisdom", "Courage", "Justice", "Temperance". Also analyze the emotions from the content one of: "Joyful", "Excited", "Content", "Grateful", "Peaceful", "Bored", "Calm", "Curious", "Confused", "Lonely", "Disappointed", "Scared", "Frustrated", "Anxious", "Jealous", "Embarrassed", "Guilty".
   User: Here's the User's Journal entry for the day: 
    {journal_entry}

    {format_instructions}
"""
load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_MODEL =  'gpt-4'

@app.get("/")
async def get_journal_entry(request: Request):
    return templates.TemplateResponse("submit_entry.html", {"request": request})


@app.post("/analyze")
async def analyze_entry(request: Request, journal_entry: str = Form(...)):
    print(journal_entry)
    if journal_entry is None:
        journal_entry = """


        Date: January 15, 2023

        Today's Journal Prompt:
        What are my core values and how do they impact my decisions?

        Today I've been considering my core values and how they impact the decisions I make in my life. I realize that my values are an essential part of who I am, and they play a significant role in shaping my thoughts, actions, and choices.

        One of my core values is honesty. I believe that it's essential to be truthful with myself and others, even when it's difficult. When I'm faced with a decision, I always try to consider whether it aligns with my values of honesty and integrity. If I feel that a decision would compromise these values, I know that it's not the right choice for me.

        Another value that's important to me is kindness. I believe that everyone deserves to be treated with respect and compassion, regardless of their background or circumstances. When I'm making a decision, I try to consider how it will impact others and whether it aligns with my values of kindness and empathy.

        Finally, I value personal growth and self-improvement. I believe that life is a journey of learning and self-discovery, and I always strive to grow and evolve as a person. When I'm making a decision, I try to consider whether it will help me grow and develop as a person, both personally and professionally.

        Reflecting on my core values has helped me gain clarity on what's important to me and how I can make decisions that align with my values. I know that when I make choices that align with my values, I feel more fulfilled, purposeful, and true to myself.

        """
    parser = PydanticOutputParser(pydantic_object=JournalEntryAnalysis)
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)
    message = HumanMessagePromptTemplate.from_template(template=SYSTEM_PROMPT_INFO)
    prompt = ChatPromptTemplate.from_messages(messages=[message])

    prompt_with_values = prompt.format_prompt(journal_entry=journal_entry, format_instructions=parser.get_format_instructions())
    response = llm.invoke(prompt_with_values)
    analysis = parser.parse(response.content)
    
    return templates.TemplateResponse("journal_analysis.html", {"request": request, "analysis": analysis})