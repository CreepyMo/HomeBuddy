import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        logging.info(f"Finished test: {item.nodeid} with outcome: failed")
    elif call.when == "call":
        logging.info(f"Finished test: {item.nodeid} with outcome: passed")
