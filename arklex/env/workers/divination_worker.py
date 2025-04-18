from arklex.env.workers.worker import BaseWorker, register_worker
from arklex.env.workers.divination_agent.divination_agent import DivinationAgent
import re
import traceback

@register_worker
class DivinationWorker(BaseWorker):
    description = "A worker for generating hexagrams and providing I-Ching interpretations."

    def __init__(self, api_key: str = None):
        super().__init__()
        self.agent = DivinationAgent(api_key=api_key)

    def _execute(self, msg_state):
        """
        Execute the hexagram generation and interpretation.
        """
        # Extract user input from msg_state
        user_input = msg_state.user_message.message
        
        # Use regex to extract six-digit number
        numbers_match = re.search(r"\d{6}", user_input)
        numbers = numbers_match.group(0) if numbers_match else None
        
        # Extract query by removing the number part
        query = user_input.replace(numbers, "").strip() if numbers else user_input.strip()



        # Validate numbers
        if not numbers or len(numbers) != 6 or not numbers.isdigit():
            msg_state.response = "To begin your divination, please share the area of life you’d like to explore (e.g., travel, love, career, or studies), along with a 6-digit number, such as 123456."
            return msg_state

        # Validate query (optional)
        if not query:
            query = "Travel fortune"  # Default direction if no query is provided

        print(f"Extracted numbers: {numbers}")
        print(f"Extracted query: {query}")

        # Perform divination
        try:
            result = self.agent.divine(numbers=numbers, query=query)
        except Exception as e:
            msg_state.response = "The divination could not be completed at this time. Please try again later, when the timing is right."
            traceback.print_exc()  # 这行会把完整的错误堆栈打印到终端
            return msg_state

        # Update message state with the result
        msg_state.response = result
        return msg_state