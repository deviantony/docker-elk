#!/usr/bin/env python3
#*******************************************
#   Author: Doc Harley, Benjamin Peterson (Updated by Evan Bostian)
#   Date: 11/13/2025 (Updated 2/23/2026)
#
#   Description: Performs automated calls to AI models with MCp tools defined when an alert is generated 
#
#   Execution: python3 AutomatedMCPCall.py
#
#*******************************************


import os, json, time, hashlib
import urllib3
from datetime import datetime, timedelta
import requests
from openai import OpenAI
from elasticsearch import Elasticsearch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------- CONFIG -------------------
# Elasticsearch (source for alerts)
ES_HOST = os.getenv("ES_HOST", "")
ES_USER = os.getenv("ES_USER", "")
ES_PASS = os.getenv("ES_PASS", "")

# Elasticsearch (destination for AI output)
ELK_HOST = os.getenv("ELK_HOST", "")   
ELK_API_KEY = os.getenv("ELK_API_KEY", "")
INDEX_PATTERN = os.getenv("INDEX_PATTERN", "ai-alerts")

# Global Elasticsearch base for tools (your original BASE_URL endpoints)
BASE_URL = os.getenv("BASE_URL", "")

# LM Studio (tool-capable chat)
LM_BASE = os.getenv("LM_BASE", "")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-20b")  # keep consistent

# Portable investigation guidance (generic by default)
INVESTIGATION_GUIDANCE = os.getenv(
    "INVESTIGATION_GUIDANCE",
    "Use the provided tools to gather context (related alerts, same host, same rule/ID) before concluding. "
    "Focus on likely cause, impact, and recommended actions. Be concise but actionable."
)

# ------------------- CLIENTS -------------------
src_es = Elasticsearch(ES_HOST, basic_auth=(ES_USER, ES_PASS), verify_certs=False, request_timeout=30)
dst_es = Elasticsearch(ELK_HOST, api_key=ELK_API_KEY, verify_certs=False, request_timeout=30)

# You can use either OpenAI client or raw requests; use the SDK for tools
client = OpenAI(base_url=LM_BASE, api_key="lm-studio")  # LM Studio ignores the key but requires a value

# ------------------- TOOLS (functions) -------------------
# Lists all the indicies in the ELK stack
def list_indicies():
    endpoint = "/_cat/indices?v"
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": "ApiKey <APIKey>",
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, verify=True, timeout=20)
        r.raise_for_status()
        #print("listIndicies")
        return r.text
    except requests.RequestException as e:
        return f"Error: {e}"

# Lists all the AI documents in the ELK stack
def list_ai_documents():
    endpoint = "/ai-alerts/_search"
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": "ApiKey <APIKey>",
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, verify=True, timeout=20)
        r.raise_for_status()
        #print("listAI")
        return r.text
    except requests.RequestException as e:
        return f"Error: {e}"

# Searches the ELK stack for fields within a specified time period
def search_elk(elkIndex: str, searchField: str, searchOption: str, searchDays: int):
    # Construct the URL based on what the AI model puts as output
    searchEnd = "_search"
    url = f"{BASE_URL}/{elkIndex}/{searchEnd}?q={searchField}:{searchOption}%20AND%20@timestamp:%5Bnow-{searchDays}d%20TO%20now%5D"
    
    # Debug Statement to print out the url
    #print(url)
    headers = {
        "Authorization": "ApiKey <APIKey>",
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, verify=True, timeout=20)
        r.raise_for_status()
        print("Search of Elasticsearch Sucessfull")
        return r.text
    except requests.RequestException as e:
        #print("ur cooked buddy")
        return f"Error: {e}"


# Tool definitions for AI model
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "list_indicies",
            "description": "List indices for Elasticsearch",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_ai_documents",
            "description": "Search AI alerts for Elasticsearch",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_elk",
            "description": "Search elk for a specific thing",
            "parameters": {"type": "object", "properties": {
                "elkIndex":{
                    "type": "string",
                    "description": "The index that will be called in an elasticsearch query"
                },
                "searchField":{
                    "type": "string",
                    "description": "The field that will be searched for in an elasticsearch query"
                },
                "searchOption":{
                    "type": "string",
                    "description": "The option that will be queried for within a field in an elasticsearch query"
                },
                "searchDays":{
                    "type": "int",
                    "description": "The option that will specify as an integer the amount of days to search for"
                }
            }},
            "required": ["elkIndex", "searchField", "searchOption", "searchDays"]
        },
    },
]

# Overall tool list for AI model
TOOL_IMPL = {
    "list_indicies": list_indicies,
    "list_ai_documents": list_ai_documents,
    "search_elk": search_elk,
}

# ------------------- CORE: tool-capable chat loop -------------------
def run_chat_with_tools(messages):
    """
    Runs a tool-aware loop until the model stops requesting tools.
    Returns the final assistant message content.
    """
    #print(messages)

    # first turn with tools available
    
    resp = client.chat.completions.create(
        model=AI_MODEL,
        messages=messages,
        tools=TOOLS_SPEC,
        stream=False,
    )

    while True:
        msg = resp.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None)

        

        # If the model made tool calls, execute them and send results back
        if tool_calls:
            # append assistant's tool-call message
            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments or "{}"
                        }
                    } for tc in tool_calls
                ],
            })

            # execute each tool and append its result
            for tc in tool_calls:
                fn_name = tc.function.name
                print("Name of tool called: " + fn_name)
                raw_args = tc.function.arguments or "{}"
                try:
                    args = json.loads(raw_args) if raw_args.strip() else {}
                except Exception:
                    args = {}

                impl = TOOL_IMPL.get(fn_name)
                if not impl:
                    # unknown tool: respond with an empty result to avoid deadlock
                    result = json.dumps({"error": f"unknown tool {fn_name}"})
                else:
                    try:
                        result = impl() if not args else impl(**args)
                        #print(result)
                    except TypeError:
                        result = impl()  # tools here take no args

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result if isinstance(result, str) else json.dumps(result),
                })

            #print(messages)
            # ask model to continue now that tools have returned
            resp = client.chat.completions.create(
                model=AI_MODEL,
                messages=messages,
                tools=TOOLS_SPEC,
                stream=False,
            )
            
            continue

        # No tool calls — return the assistant’s content
        msg = resp.choices[0].message
        #print(msg.content)
        return msg.content or ""

# ------------------- ALERT INGEST/WATCH -------------------
def fetch_new_alerts(window_minutes=1, size=5):
    now = datetime.utcnow()
    gte_time = now - timedelta(minutes=window_minutes)
    try:
        res = src_es.search(
            index="*",
            query={"range": {"@timestamp": {"gte": gte_time.isoformat()}}},
            sort=[{"@timestamp": {"order": "desc"}}],
            size=size,
        )
        return res.get("hits", {}).get("hits", [])
    except Exception as e:
        print(f"[fetch_new_alerts] Error: {e}")
        return []

def index_ai_response(alert_id, content):
    # Define the document that is being placed in the index
    doc = {
        "@timestamp": datetime.utcnow().isoformat(),
        "alert_id": alert_id,
        "response": content,
    }
    try:
        r = dst_es.index(index=INDEX_PATTERN, document=doc)
        return r
    except Exception as e:
        print(f"[index_ai_response] Error: {e}")
        return None

# ------------------- MAIN LOOP -------------------
def main(): 
    # Grab the previously evaluated alerts within the function
    seen_ids = set()
    print("Watching for new alerts with tool-enabled AI analysis...")

    while True:
        alerts = fetch_new_alerts(window_minutes=1, size=5)
        
        
        for hit in alerts:
            start_time = time.time()
            alert_id = hit.get("_id")
            if not alert_id or alert_id in seen_ids:
                continue
            seen_ids.add(alert_id)

            alert = hit.get("_source", {})
            alert_json = json.dumps(alert, indent=2)

            # Build the conversation that explicitly invites tool use
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an expert SOC analyst, specializing in alert investigation and correlation. Your primary goals are providing first accurate and second valuable information. You are being passed the context of an alert and you must determine likely cause, impact, and provide recommended actions. Use tools for context (indices and prior AI docs) before giving a final assessment. Be concise but actionable."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{INVESTIGATION_GUIDANCE}\n\n"
                        f"Here is the alert:\n\nALERT:\n{alert_json}"
                    ),
                },
            ]

            try:
                # Start the chat with the AI
                final_text = run_chat_with_tools(messages)

            except Exception as e:
                final_text = f"Error during tool-enabled analysis: {e}"

            # Return as a boolean if an alert was sucessuflly indexed
            r = index_ai_response(alert_id, final_text)

            # Print statements to terminal and time tracking
            elapsed = time.time() - start_time
            print(f"\nTime to process Alert: {elapsed:.2f} seconds")
            print(f"[{datetime.utcnow().isoformat()}] Processed alert {alert_id}. Indexed: {bool(r)}")


        time.sleep(60)  # <- actually reached each cycle

if __name__ == "__main__":
    main()
