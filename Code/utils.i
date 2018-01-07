%module utils
%{
#include "utils.h"
%}

%include "std_vector.i"
%include "std_string.i"

namespace std {
   %template(StringVector) vector<string>;
   %template(DoubleVector) vector<double>;
   %template(VectorOfStringVector) vector<vector<string> >; 
}

%include "utils.h"
