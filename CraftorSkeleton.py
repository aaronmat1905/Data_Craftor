from dcraftllm import DataModel
import pandas as pd
import gradio as gr
import uuid
from io import StringIO

class Craftor(DataModel):
  def __init__(self):
    super().__init__()
    self.conversion_prompts = {
            "python": "Convert the generated synthetic data from memory into Python code to create a pandas DataFrame.",
            "SQL": "Convert the generated synthetic data from memory into SQL code.",
            "csv": "Convert the generated synthetic data from memory into CSV format.",
            "json": "Convert the generated synthetic data from memory into JSON format.",
            "R": "Convert the generated synthetic data from memory into R code."
        }
  def generate_session_id(self):
      return str(uuid.uuid4())
  
  def respond(self, message, chat_history, session_id):
        bot_message = self.chatbot_response(message, session_id)
        chat_history.append((message, bot_message))
        updated_df = self.import_from_chat(session_id)
        return chat_history, "", updated_df  
  def clear_memory(self, session_id):
        self.clear_session_memory(session_id)
        return []

    def upload_file(self, file):
        if file is None:
            return pd.DataFrame()
        try:
            return pd.read_csv(file.name)
        except Exception as e:
            return pd.DataFrame({"Error": [f"Failed to upload file: {str(e)}"]})

    def add_to_prompt(self, file, session_id):
        df = self.upload_file(file)
        if df.empty:
            return "No data found in the uploaded file. Please upload a valid CSV file.", ""
        df_json = df.to_json(orient='records')
        msg = "Use this data for future interactions:\n" + df_json
        self.get_memory(session_id).save_context({"input": msg}, {"output": "Data set in memory: Ask anything!"})
        return "Data uploaded and added to memory.", ""

    def convert_data(self, typeCode="python", session_id=None):
        if session_id not in self.session_memory:
            return "Session not found in memory."
        
        memory_object = self.session_memory[session_id]
        prompt = self.conversion_prompts.get(typeCode)
        if not prompt:
            return f"Invalid typeCode: '{typeCode}'. Choose from 'python', 'SQL', 'csv', 'json', 'R'."
        
        memory_data = str(memory_object.load_memory_variables({}))
        try:
            output = self.llm.invoke(prompt + f"\nContext from memory:\n{memory_data}").content
            return output.strip(f'```{typeCode}\n').strip('```')
        except Exception as e:
            return f"Error during conversion: {str(e)}"

    def import_from_chat(self, session_id):
        if session_id not in self.session_memory:
            return pd.DataFrame({"Error": ["Session memory not found."]})
        
        try:
            data = self.convert_data("json", session_id)
            return pd.read_json(StringIO(data))
        except ValueError as e:
            return pd.DataFrame({"Error": [str(e)]})
    
    
