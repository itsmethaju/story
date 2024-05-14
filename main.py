from fastapi import FastAPI, HTTPException
import openai
from supabase import create_client, Client
import os
import google.generativeai as palm
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

load_dotenv()
# Configure Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Configure AI
# openai.api_key = os.getenv("OPENAI_API_KEY")

#gen ai 
palm.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model init
class Character(BaseModel):
    name: str
    details: str

class StoryRequest(BaseModel):
    character_name: Optional[str] = Field(None, example="Bilbo Baggins")
    id: Optional[int] = Field(None, example=1)


@app.post("/api/create_character", status_code=201)
async def create_character(character: Character):
    try:
        response = supabase.table("characters").insert({
            "name": character.name,
            "details": character.details
        }).execute()

        print("Supabase response:", response)

        # Check for errors in the response
        if response.data is None:
            raise HTTPException(status_code=500, detail="Failed to create character: No data returned from Supabase")
        
        return response.data
    except Exception as e:
        # Log the exception 
        print("Exception:", str(e))
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")




# open ai code .
# @app.post("/api/generate_story", status_code=201)
# async def generate_story(story_request: StoryRequest):
#     try:
#         response = supabase.table("characters").select("*").eq("name", story_request.character_name).execute()

#         # Log the full response for debugging
#         print("Supabase response:", response)
        
#         if not response.data or len(response.data) == 0:
#             raise HTTPException(status_code=404, detail="Character not found")

#         character = response.data[0]
#         prompt = (
#             f"{character['name']}, {character['details']}. "
#             "Generate a short story about this character."
#         )
#         openai_response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a story generator."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=100
#         )

#         story = openai_response.choices[0].message['content'].strip()
#         return {"story": story}
#     except Exception as e:
#         print("Exception:", str(e))
#         raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")



@app.post("/api/generate_story", status_code=201)
async def generate_story(story_request: StoryRequest):
    try:
        if story_request.id is not None:
            response = supabase.table("characters").select("*").eq("id", story_request.id).execute()
        elif story_request.character_name:
            response = supabase.table("characters").select("*").eq("name", story_request.character_name).execute()
        else:
            raise HTTPException(status_code=400, detail="Either character_name or id must be provided")


        # full response 
        print("Supabase response:", response)
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Character not found")

        character = response.data[0]
        prompt = (
            f"{character['name']}, {character['details']}. "
            "Generate a short story about this character.4 to 5 sentences is enough"
        )

        #  Google Generative AI (PaLM)
        openai_response = palm.generate_text(
            model="models/text-bison-001",  # model ID
            prompt=prompt,
            max_output_tokens=100
        )

        story = openai_response.result
        print(story)
        return {"story": story}
    except Exception as e:
        print("Exception:", str(e))
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
