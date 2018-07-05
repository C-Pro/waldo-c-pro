.PHONY: test install

install:
	./setup.py install

test:
	cd waldo-match ; python3 match_test.py

