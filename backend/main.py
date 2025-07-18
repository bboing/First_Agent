from router.agent_orchestrator import route_query
from logger_config import setup_logging

def main():
    setup_logging()
    while True:
        user_input = input("User > ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = route_query(user_input)
        print("Agent >", response)

if __name__ == "__main__":
    main()