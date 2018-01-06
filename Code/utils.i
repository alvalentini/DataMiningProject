%module utils
%{
#include "utils.h"
%}

%include "std_vector.i"
%include "std_string.i"

namespace std {
   %template(StringVector) vector<string>;
}

%include "utils.h"
