all: clean utils.h utils.cxx utils.i
	@swig -c++ -python utils.i
	@g++ -std=c++11 -O2 -fPIC -c utils.cxx
	@g++ -std=c++11 -O2 -fPIC -c utils_wrap.cxx -I/usr/include/python3.5/
	@g++ -shared utils.o utils_wrap.o -o _utils.so
	@rm -f *.o *_wrap.cxx *~
	@mv *.so ../
	@mv utils.py ../

.PHONY: clean

clean:
	@rm -f *.o *_wrap.cxx *~ *.so utils.py ../*.so ../utils.py
