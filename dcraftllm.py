import os
import uuid
import threading
import time
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from io import StringIO

class DataModel:
    def __init__(self):
        api_key = os.getenv("GeminiAPI")
        datagen_prompt = """
        You are an expert in statistics, mathematics, and data analysis. Respond only to inquiries within these domains.
        When asked to generate synthetic structured data resembling real-life scenarios, ensure it follows statistical principles.
        - Output must start with the "~" character and be in markdown format.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=api_key,
            temperature=0,
            context=datagen_prompt
        )
        self.session_memory = {}
        self.session_activity = {}
        self.session_cleanup_thread = threading.Thread(target=self.clear_expired_sessions, daemon=True)
        self.session_cleanup_thread.start()

    def get_memory(self, session_id):
        if session_id not in self.session_memory:
            self.session_memory[session_id] = ConversationBufferMemory()
            self.session_activity[session_id] = datetime.now()
        else:
            self.session_activity[session_id] = datetime.now()
        return self.session_memory[session_id]

    def clear_expired_sessions(self, timeout_minutes=30):
        while True:
            time.sleep(300)
            current_time = datetime.now()
            expired_sessions = [
                session_id for session_id, last_activity in self.session_activity.items()
                if current_time - last_activity > timedelta(minutes=timeout_minutes)
            ]
            for session_id in expired_sessions:
                self.clear_session_memory(session_id)

    def clear_session_memory(self, session_id):
        if session_id in self.session_memory:
            del self.session_memory[session_id]
            del self.session_activity[session_id]

    def chatbot_response(self, user_input, session_id):
        memory = self.get_memory(session_id)
        conversation = ConversationChain(llm=self.llm, memory=memory, verbose=True)
        return conversation.predict(input=user_input)
