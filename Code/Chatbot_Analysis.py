import pandas as pd
import re
import os
from google import genai
from google.api_core.exceptions import ResourceExhausted

##ChatBOT Insights
chatbot_insights_df = pd.read_csv(
    r"C:\Vaishu__Docs\BITS Documents\Final_Project_Requirements\Datasets_needed_For_ChatBot\Bayesian_Model_Results.csv"
)



#Preparing final Chatbot table
# Sort by ROI (best first)
chatbot_insights_df = chatbot_insights_df.sort_values(
    by="ROI", ascending=False
).reset_index(drop=True)

# Add Rank
chatbot_insights_df["Rank"] = chatbot_insights_df.index + 1


#Overall summary
def get_overall_summary():
    best_channel = chatbot_insights_df.sort_values(
        by="ROI", ascending=False
    ).iloc[0]["Channel"]

    return {
        "total_spend": round(chatbot_insights_df["Spend"].sum(), 2),
        "total_revenue_contribution": round(chatbot_insights_df["Revenue_Contribution"].sum(), 2),
        "average_roi": round(
            chatbot_insights_df["Revenue_Contribution"].sum() /
            chatbot_insights_df["Spend"].sum(), 2
        ),
        "best_channel": best_channel
    }

def get_top_channels(n=3):
    return chatbot_insights_df.head(n)[
        ["Channel", "ROI", "Contribution_Share_%", "Rank"]
    ].to_dict(orient="records")

def get_channel_details(channel):
    row = chatbot_insights_df[
        chatbot_insights_df["Channel"].str.lower() == channel.lower()
    ]

    if row.empty:
        return {"error": f"Channel '{channel}' not found"}

    row = row.iloc[0]

    return {
        "channel": row["Channel"],
        "spend": round(row["Spend"], 2),
        "revenue_contribution": round(row["Revenue_Contribution"], 2),
        "roi": round(row["ROI"], 2),
        "contribution_share_pct": round(row["Contribution_Share_%"], 2),
        "effectiveness": round(row["Effectiveness"], 2),
        "elasticity": float(row["Elasticity"]),
        "rank": int(row["Rank"])
    }

def simulate_budget_change(channel, pct_change):
    row = chatbot_insights_df[
        chatbot_insights_df["Channel"].str.lower() == channel.lower()
    ]

    if row.empty:
        return {"error": f"Channel '{channel}' not found"}

    row = row.iloc[0]

    base_revenue = float(row["Revenue_Contribution"])
    elasticity = float(row["Elasticity"])

    revenue_change = base_revenue * elasticity * (pct_change / 100)

    return {
        "channel": row["Channel"],
        "budget_change_pct": pct_change,
        "estimated_revenue_change": round(float(revenue_change), 2),
        "direction": "Increase" if revenue_change > 0 else "Decrease"
    }


def extract_channel_from_query(user_query):
    query = user_query.lower()
    for channel in chatbot_insights_df["Channel"].unique():
        if channel.lower() in query:
            return channel
    return None


def extract_percentage(user_query):
    match = re.search(r'(\d+)\s*%', user_query)
    if match:
        return int(match.group(1))

    match = re.search(r'(\d+)\s*percent', user_query.lower())
    if match:
        return int(match.group(1))

    return None

def detect_intent(user_query):
    q = user_query.lower()

    if "increase" in q or "what if" in q:
        return "WHAT_IF"
    elif "best" in q or "top" in q:
        return "RANKING"
    elif "summary" in q or "overall" in q:
        return "SUMMARY"
    else:
        return "CHANNEL_DETAIL"

def build_gemini_prompt(user_query, computed_result):
    return f"""
You are a marketing analytics assistant.

User question:
{user_query}

Computed MMM insights:
{computed_result}

Explain the answer in simple business language.
Avoid technical terms like regression or coefficients.
Provide clear recommendations if possible.
"""

def chatbot_response(user_query):
    intent = detect_intent(user_query)

    if intent == "SUMMARY":
        result = get_overall_summary()

    elif intent == "RANKING":
        result = get_top_channels()

    elif intent == "WHAT_IF":
        channel = extract_channel_from_query(user_query)
        pct = extract_percentage(user_query)

        if channel is None or pct is None:
            result = {"error": "Could not understand the scenario"}
        else:
            result = simulate_budget_change(channel, pct)

    else:
        channel = extract_channel_from_query(user_query)

        if channel is None:
            result = {"error": "Channel not found"}
        else:
            result = get_channel_details(channel)

    return build_gemini_prompt(user_query, result)


##GEMINI Setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyCxyXz6k0nxrmXy9N_036fyCDZtDdOtPlc"
client = genai.Client()


##Gemini Call Function


def call_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except ResourceExhausted:
        return (
            "⚠️ The AI service is temporarily busy due to free-tier limits.\n\n"
            "Please wait for about a minute and try again.\n\n"
                    )


