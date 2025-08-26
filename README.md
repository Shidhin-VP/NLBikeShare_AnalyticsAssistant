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

URL for Accessing the Sites:
https://bikeshareanalyticsassistant.streamlit.app/
For the Access Code, please DM. 
APK for the Mobile app can be find on the APK file that can be found in this main folder

# Demo
![undergif1](https://github.com/user-attachments/assets/ae2a2a90-e61e-4d04-88b2-d9c1bf4f2829)

