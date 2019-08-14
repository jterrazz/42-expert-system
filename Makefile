# TO COMPLETE

NAME = expert_system

.PHONY: expert_system all tests

install:
    python3 -m pip install -r requirements.txt

test: # install
    python3 -m pytest -v
