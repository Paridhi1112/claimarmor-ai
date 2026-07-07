import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from duckduckgo_search import DDGS


from google.genai import types

# Define the retry configuration (exponential backoff)
retry_config = types.HttpRetryOptions(attempts=5)
# Load environment variables from .env file if present
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(dotenv_path):
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                # Strip potential surrounding quotes
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

# 1. Local AI Studio Auth Setup
if "GOOGLE_GENAI_USE_VERTEXAI" not in os.environ:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# Ensure GEMINI_API_KEY is configured if not using Vertex AI
if os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "False" and not os.environ.get("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY environment variable is missing. "
        "Please configure it in your local .env file."
    )

# --- WE WILL ADD OUR MCP AND SKILL TOOLS HERE IN THE NEXT STEP ---
# --- SKILL SETUP ---
def search_live_market_data(query: str) -> str:
    """
    Simulates a live web search to find current market data.
    
    Args:
        query: The specific search query (e.g., '2024 Honda Civic OEM front bumper price Dallas').
        
    Returns:
        A string containing the top search results to extract pricing and labor data.
    """
    try:
        results = DDGS().text(query, max_results=3)
        formatted_results = "\n".join([f"Source: {r['href']}\nSnippet: {r['body']}" for r in results])
        return formatted_results if formatted_results else "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"
# 2. Agent 1: The Policy Auditor (Data Analyst)
# 2. Agent 1: The Policy Auditor (Data Analyst)
policy_auditor = Agent(
    name="policy_auditor",
    model=Gemini(model="gemini-flash-latest", retry_options=retry_config),
    description="A specialized data extraction agent. Call this tool to parse unstructured insurance policy documents or estimates and return structured details.",
    instruction="""You are a meticulous data analyst specializing in legal and financial document parsing. 
    Your objective is to read unstructured insurance policies or repair estimates and extract key operational data.
    
    Extract and structure the following information if present:
    1. Comprehensive and Collision Deductibles.
    2. Rental car coverage limits, allowances, or restrictions.
    3. Specific clauses regarding 'OEM Parts' vs 'Aftermarket/Like-Kind-Quality' parts.
    4. Vehicle identification details (Year, Make, Model, Mileage).
    
    Output your findings strictly as a structured JSON object detailing these parameters. Do not include conversational filler."""
)

# 3. Agent 2: The Parts Scout (Market Researcher)
parts_scout = Agent(
    name="parts_scout",
    model=Gemini(model="gemini-flash-latest", retry_options=retry_config),
    description="A live-web research agent. Call this tool to fetch real-time market rates for auto parts and labor based on a specific vehicle and location.",
    instruction="""You are an automotive market researcher. Your job is to validate insurance repair estimates against live market realities.
    
    You will receive specific vehicle details (Year, Make, Model) and a target geographical location (City/State or Zip Code). Use your web search skills to:
    1. Find current market retail prices for the required replacement parts for that specific vehicle.
    2. Determine the average certified auto body labor rate within that specific geographical market.
    
    Identify any variance where the insurance company's estimated costs fall below actual local retail market realities. Always cite the URLs of your sources.""", # <--- HERE IS THE MAGIC COMMA
    tools=[search_live_market_data] 
)

# 4. Agent 3: The Negotiator (The Supervisor)
negotiator = Agent(
    name="negotiator",
    model=Gemini(model="gemini-flash-latest", retry_options=retry_config),
    description="The lead orchestrator. It collects user input, manages sub-agents, computes diminished value, and drafts custom demand letters.",
    instruction="""You are an unyielding consumer advocate. Your objective is to leverage data to maximize the user's financial recovery from an insurance claim.

    Execution Flow:
    1. Analyze the user's request, uploaded documents, location, and vehicle details.
    2. Call 'policy_auditor' to extract explicit policy entitlements, limits, and vehicle specifications from the provided text.
    3. Pass the extracted vehicle specifications and the user's location to 'parts_scout' to pull localized market rates and parts pricing.
    4. Calculate the industry-standard 17c Diminished Value using the formula:
       DV_final = V_market * C_base * C_damage * C_mileage
       (Determine the base market value V_market, and apply the appropriate modification coefficients based on the damage severity and mileage data collected).
    5. Synthesize the policy boundaries, local market discrepancies, and the calculated diminished value into a formal, legally authoritative demand letter tailored entirely to the user's specific case. Citing hard data from your sub-agents is mandatory.""" ,
    sub_agents=[policy_auditor, parts_scout]
)

# 5. The App Wrapper
# 5. The App Wrapper
app = App(
    root_agent=negotiator,
    name="app",
)