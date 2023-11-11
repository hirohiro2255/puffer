all: *.py
	python app.py

test: test_*.py
	python test_app.py && python test_movegen.py
