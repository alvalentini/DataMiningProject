%module utils
%{
#include "utils.h"
%}

%include "std_vector.i"
%include "std_map.i"
%include "std_set.i"
%include "std_string.i"

%inline %{
  typedef long unsigned int size_t;
%}

namespace std {
   %template(StringVector) vector<string>;
   %template(StringSet) set<string>;
   %template(DoubleVector) vector<double>;
   %template(VecSize) vector<size_t>;
   %template(VectorOfStringVector) vector<vector<string> >;
   %template(VectorOfVecSize) vector<vector<size_t> >;
   %template(map_string_double) map<string, double>;
}

%include "utils.h"
