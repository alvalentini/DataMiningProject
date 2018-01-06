all: utils.h utils.cxx utils.i
	@swig -c++ -python utils.i
	@g++ -O2 -fPIC -c utils.cxx
	@g++ -O2 -fPIC -c utils_wrap.cxx -I/usr/include/python3.5/
	@g++ -shared utils.o utils_wrap.o -o _utils.so

.PHONY: clean

clean:
	@rm -f *.o *_wrap.cxx *~
