import streamlit as st
from openai import OpenAI

class Agent:
    def __init__(self, name, instructions, functions=None):
        self.name = name
        self.instructions = instructions
        self.functions = functions or []

class Swarm:
    def __init__(self):
        # Use Streamlit secrets for OpenAI API key
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
    def run(self, agent, messages):
        # Prepare the conversation
        conversation = []
        for msg in messages:
            conversation.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add agent instructions
        system_message = f"You are {agent.name}. {agent.instructions}"
        
        # Make the API call
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_message},
                *conversation
            ]
        )
        
        # Check if we should transfer to another agent
        if agent.functions and response.choices[0].message.content.lower().find("transfer") != -1:
            next_agent = agent.functions[0]()
            return self.run(next_agent, messages + [{"role": "assistant", "content": response.choices[0].message.content}])
        
        return type('Response', (), {'messages': messages + [{"role": "assistant", "content": response.choices[0].message.content}]}) 