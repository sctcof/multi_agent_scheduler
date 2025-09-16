# main.py
from examples.medical_dialogue_demo import medical_dialogue_flow
import asyncio

if __name__ == "__main__":
    asyncio.run(medical_dialogue_flow())