![image](https://github.com/itsmethaju/story/assets/68291010/49fa59c4-f827-4034-8886-204df68c47a4)# Story Generator API

## Overview
This API allows you to create characters and generate short stories about them using FastAPI, Supabase, and Google Generative AI (PaLM).

## Endpoints

### 1. Create Character
- **Endpoint**: `/api/create_character`
- **Method**: `POST`
- **Description**: Create a new character.
- **Inputs**: `name`, `details`
- **Response**: Returns the created character with a 201 status code.

#### Example cURL Request
```sh
curl -X POST "http://localhost:8000/api/create_character" \
     -H "Content-Type: application/json" \
     -d '{"name": "Bilbo Baggins", "details": "Hobbit lives in the Shire owning a magic ring"}'
Example Response
json
{
  "id": 9,
  "created_at": "2024-05-14T07:14:22.132611+00:00",
  "name": "Bilbo Baggins",
  "details": "Hobbit lives in the Shire owning a magic ring"
}

2. Generate Story
Endpoint: /api/generate_story
Method: POST
Description: Generate a story with a character.
Inputs: character_name or id
Response: Returns the generated story with a 201 status code.

curl -X POST "http://localhost:8000/api/generate_story" \
     -H "Content-Type: application/json" \
     -d '{"character_name": "Bilbo Baggins"}'


### Response body

{
  "story": "Bilbo Baggins was a hobbit who lived in a comfortable hole in the Shire. He was content with his life until he was unexpectedly invited by the wizard Gandalf to join a group of dwarves on an adventure to reclaim their lost kingdom from Smaug the dragon. Bilbo reluctantly agreed and found himself on an epic journey that changed his life forever."
}


### Instructions

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/itsmethaju/story.git
    cd story
    ```

2. **Set Up Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables**:
    Create a `.env` file in the project root with the following content:
    ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    GOOGLE_API_KEY=your_google_api_key
    ```

4. **Run the FastAPI Application**:
    ```sh
    uvicorn main:app --reload
    ```

5. **Access API Documentation**:
    Open your browser and navigate to `http://localhost:8000/docs`.

### Notes:
- Ensure your Supabase project is properly configured with the necessary tables and permissions.
- Replace placeholder values in the `.env` file with your actual Supabase and Google API keys.

### Contributing:
- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Commit your changes (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.
