from speech_to_text import recognize_from_mic
from text_to_speech import speak
from dialogue_manager import generate_reply
from utils import save_call_data
from datetime import datetime


def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Hello"

def run_call(customer_id="test_user"):
    conversation = ""
    transcript = ""
    call_data = {
        "customer_id": customer_id,
        "transcript": "",
        "employment_status": None,
        "monthly_salary": None,
        "net_monthly_takehome_salary": None,
        "current_emi": None,
        "desired_loan": None,
        "age": None,
    }

    greet = f"{get_time_greeting()}! I'm an AI Assistant calling from RupeeQ Finance for overdraft facilicty. May I speak to you for 2 minutes?"
    speak(greet)
    conversation += f"Agent: {greet}\n"

    
    customer_input = recognize_from_mic(timeout=6)
    if customer_input and any(word in customer_input.lower() for word in ["after", "later", "not now", "another time", "not interested", "no"]):
        goodbye = "No Problem! We will connect you after sometime. Thank you for your time! Have a great day. Goodbye!"
        speak(goodbye)
        conversation += f"Customer: {customer_input}\nAgent: {goodbye}\n"
        call_data["transcript"] = conversation
        save_call_data(call_data, customer_id)
        return

    if customer_input:
        conversation += f"Customer: {customer_input}\n"
        transcript += f"Customer: {customer_input}\n"

    while True:
        if not customer_input:
            customer_input = recognize_from_mic(timeout=6)
            if not customer_input:
                continue
            print("Customer:", customer_input)
            transcript += f"Customer: {customer_input}\n"

        if any(word in customer_input.lower() for word in ["bye", "goodbye", "thank you"]):
            goodbye = "Thank you for your time! Have a great day. Goodbye!"
            speak(goodbye)
            conversation += f"Agent: {goodbye}\n"
            break

        agent_reply = generate_reply(conversation, customer_input)
        conversation += f"Customer: {customer_input}\nAgent: {agent_reply}\n"
        speak(agent_reply)
        customer_input = None

    call_data["transcript"] = conversation
    save_call_data(call_data, customer_id)

if __name__ == "__main__":
    run_call()


