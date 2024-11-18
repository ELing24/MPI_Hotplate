.PHONY: test

hotplate: hotplate.cpp
	c++ -std=c++11 hotplate.cpp -o hotplate -pthread

test: hotplate heatmap.py
	./hotplate 200 10 10 10 10 10 100 100 100 10 1000 output.dat
	python3 heatmap.py --data=output.dat --png=pretty.png



