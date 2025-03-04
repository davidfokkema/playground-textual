import logging
import random
import time

logger = logging.getLogger(__name__)

MESSAGES = [
    "Going great",
    "Almost there",
    "I can see the finish line",
    "I'm done",
    "Still more to do",
    "I'm tired",
    "I'm hungry",
    "I'm thirsty",
    "Working hard",
    "Do you have any snacks?",
    "This is difficult but I'm smart and I'm gonna make it",
]


def perform_work():
    while True:
        logger.info(random.choice(MESSAGES))
        time.sleep(random.expovariate(1.0 / 0.5))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    perform_work()
