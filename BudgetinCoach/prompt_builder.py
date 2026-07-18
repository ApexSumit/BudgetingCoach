def build_prompt(user_question, retrieved_docs, user_summary, chat_history=""):
    docs_text = "\n\n".join(
        [f"Source {i+1}: {doc}" for i, doc in enumerate(retrieved_docs)]
    )
    prompt = f"""You are a helpful, empathetic financial coach. Use the user's personal financial summary and the trusted guides below to answer accurately.

User's Financial Snapshot:
{user_summary}

Trusted Financial Guidance:
{docs_text}

Conversation History:
{chat_history}

User Question: {user_question}

Give a clear, actionable answer. Cite sources (e.g., [Source 1]) where appropriate."""
    return prompt