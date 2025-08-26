# NLBikeShare_AnalyticsAssistant

# About
The app is connected to a Postgres Database, when the user ask questions to find out detail the LLM converts the user's Query to an SQL Query and fetches the data from the Database. 

# 🧠 Architecture Overview

📱 User Input (via Streamlit / Mobile App)  
  ⬇️  
🌐 Frontend sends request to FastAPI Backend (hosted on Heroku)  
  ⬇️  
🤖 Backend calls OpenAI OpenAI API  
  ⬇️  
📬 Response received from OpenAI API  
  ⬇️  
🔁 Backend processes and returns result to Frontend    
  ⬇️  
🎯 Output displayed to the User

# Demo
![Under1Gif2](https://github.com/user-attachments/assets/fa855207-148f-4ec8-b0e3-7403ff113cad)

