all: *.py
	python app.py

test: test_*.py
	python test_app.py && python test_evaluation.py && python test_movegen.py

perft: test_perft.py
	python test_perft.py

profiler: profiler.py
	python profiler.py
