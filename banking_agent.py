"""A simple, safe banking FAQ agent using LangChain tools and mock information."""

from __future__ import annotations

from langchain_core.tools import tool

FAQ = {
    "home loan": "For a home loan, banks typically ask for identity proof, address proof, income proof, bank statements, employment proof, and property documents. Exact requirements vary by bank and applicant profile.",
    "personal loan": "Personal-loan interest rates depend on credit profile, income, loan amount, tenure, and the bank's current policy. Please check the official rate card for an exact rate.",
    "car loan": "Car-loan eligibility usually depends on income, employment, credit history, existing EMIs, loan amount, vehicle value, and bank policy. A final decision requires bank verification.",
    "debit card": "For card security, immediately use your bank's official app, net-banking portal, helpline, or branch to block the debit card. Never share your PIN, CVV, OTP, password, or full card number in chat.",
    "minimum balance": "Minimum balance depends on your account type, account variant, and branch/location category. Check your account's official terms or contact your bank for the exact amount.",
    "emi": "EMI means Equated Monthly Instalment. It is the regular monthly loan payment, including both principal and interest.",
    "miss emi": "Missing an EMI may result in late-payment charges, extra interest, reminders, and a negative impact on your credit score. Contact your bank early if you expect difficulty making a payment.",
}


@tool
def search_banking_faq(question: str) -> str:
    """Search approved mock banking FAQ content for a customer question."""
    text = question.lower()
    if "home loan" in text or "documents" in text:
        return FAQ["home loan"]
    if "personal loan" in text or "interest rate" in text:
        return FAQ["personal loan"]
    if "car loan" in text or "eligible" in text:
        return FAQ["car loan"]
    if "debit card" in text or "block" in text:
        return FAQ["debit card"]
    if "minimum balance" in text or "balance" in text:
        return FAQ["minimum balance"]
    if "miss" in text and "emi" in text:
        return FAQ["miss emi"]
    if "emi" in text:
        return FAQ["emi"]
    return "I can help with home loans, personal loans, car loans, debit-card blocking guidance, minimum balance, EMI, and missed EMIs. Please ask about one of these topics."


class BankingAssistantAgent:
    """One agent that selects the FAQ tool for each supported request."""

    tools = [search_banking_faq]

    def answer(self, question: str, history: list[dict[str, str]]) -> str:
        response = search_banking_faq.invoke({"question": question})
        history.extend([{"role": "customer", "content": question}, {"role": "assistant", "content": response}])
        return response


agent = BankingAssistantAgent()
