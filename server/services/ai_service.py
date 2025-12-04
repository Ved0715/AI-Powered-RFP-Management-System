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
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        parsed_data = json.loads(response.choices[0].message.content)
        
        if parsed_data.get("deadline_days"):
            deadline = datetime.utcnow() + timedelta(days=parsed_data["deadline_days"])
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


async def parse_vendor_proposal(email_body: str, email_subject: str = "") -> dict:
    """
    Parse vendor proposal email using AI to extract structured data
    
    Args:
        email_body: Email body content
        email_subject: Email subject line
        
    Returns:
        dict with: total_price, line_items, delivery_time, terms, warranty
    """
    
    system_prompt = """You are an expert at parsing vendor proposal emails.
Extract structured information from vendor responses to RFPs.

Return a JSON object with these fields:
- total_price: Total price/cost mentioned (number, null if not found)
- line_items: Array of items with their prices (array of objects with "item" and "price", empty if not found)
- delivery_time: Delivery/completion timeline mentioned (string, null if not found)
- terms: Payment terms or conditions (string, null if not found)
- warranty: Warranty information (string, null if not found)

Example input: "We can provide the 20 laptops at $800 each and 15 monitors at $300 each. Total: $19,500. Delivery in 25 days. Payment net 30. 2-year warranty included."

Example output:
{
  "total_price": 19500,
  "line_items": [
    {"item": "20 laptops", "price": 16000},
    {"item": "15 monitors", "price": 4500}
  ],
  "delivery_time": "25 days",
  "terms": "Net 30",
  "warranty": "2-year warranty"
}
"""
    
    full_text = f"Subject: {email_subject}\n\n{email_body}"
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_text}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        parsed_data = json.loads(response.choices[0].message.content)
        return parsed_data
        
    except Exception as e:
        return {
            "total_price": None,
            "line_items": [],
            "delivery_time": None,
            "terms": None,
            "warranty": None,
            "error": str(e)
        }