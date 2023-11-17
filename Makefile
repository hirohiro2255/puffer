all: *.py
	python app.py

test: test_*.py
	python test_app.py && python test_evaluation.py

perft: test_movegen.py
	python test_movegen.py
