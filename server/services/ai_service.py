from openai import AsyncOpenAI
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def parse_rfp_description(description: str) -> dict:

    system_prompt = """You are an expert at parsing procurement RFP (Request for Proposal) descriptions.
Extract structured information from natural language descriptions.

Return a JSON object with these fields:
- title: A concise title for the RFP (string)
- requirements: Array of specific requirements mentioned (array of strings)
- budget: Total budget amount if mentioned (number, null if not mentioned)
- deadline_days: Number of days until deadline if mentioned (number, null if not mentioned)
- payment_terms: Payment terms if mentioned (string, null if not mentioned)
- warranty_terms: Warranty requirements if mentioned (string, null if not mentioned)

Example input: "I need 20 laptops with 16GB RAM. Budget $50k. Delivery in 30 days. Net 30 payment."

Example output:
{
  "title": "Laptop Procurement",
  "requirements": ["20 laptops", "16GB RAM"],
  "budget": 50000,
  "deadline_days": 30,
  "payment_terms": "Net 30",
  "warranty_terms": null
}
"""


    try:
        responce = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user" , "content": description}
            ],
            responce_format={"type":"json_object"},
            temperature=0
        )

        parsed_data = json.load(responce.choices[0].message.content)
        
        if parsed_data.get("deadline_days"):
            deadline = daterime.utcnow() + timedelta(day=parsed_data["deadline_days"])
            parsed_data["deadline"] = deadline.isoformat()
        else:
            parsed_data["deadline"] = None
        
        parsed_data.pop("deadline_days", None)

        return parsed_data

    except Exception as e:

        return {
            "title": "Untitled RFP",
            "requirements": [],
            "budget": None,
            "deadline": None,
            "payment_terms": None,
            "warranty_terms": None,
            "error": str(e)
        }