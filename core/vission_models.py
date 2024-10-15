import base64
import aiohttp , openai
import requests
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel,Field
from typing import List

class OpenAIvissionStructured:

    def __init__(self,api_key,model_name) -> None:

        self.model_name = model_name
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key =api_key)

    def encode_image(self,image_path):
        """Encodes an image to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def get_output(self, question, image_path, max_tokens=4000, temperature=0, detail="high"):

        base64_image = self.encode_image(image_path)

        completion = await self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": question
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                        "detail": detail
                                    }
                                }
                            ]
                        }
                    ],
            temperature=temperature,
            max_tokens=max_tokens

        )

        try:
            output = completion.choices[0].message.tool_calls[0].function.parsed_arguments

            return [i.model_dump() for i in output.details]
        except Exception as e:
            return  []