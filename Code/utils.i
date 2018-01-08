%module utils
%{
#include "utils.h"
%}

%include "std_vector.i"
%include "std_map.i"
%include "std_string.i"

namespace std {
   %template(StringVector) vector<string>;
   %template(DoubleVector) vector<double>;
   %template(VectorOfStringVector) vector<vector<string> >;
   %template(map_string_double) map<string, double>;
}

%include "utils.h"
