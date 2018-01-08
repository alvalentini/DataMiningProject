#include <algorithm>
#include <set>
#include <map>
#include <limits>
#include <iostream>
#include <sstream>

#include "utils.h"

using namespace std;

double jaccard_similarity(const vector<string>& a, const vector<string>& b) {
  set<string> intersect;
  set<string> unionset;
  set_intersection (a.begin(), a.end(), b.begin(), b.end(), inserter(intersect, intersect.begin()));
  size_t int_size = intersect.size();
  if (int_size == 0) {
    return 0.;
  }
  else {
    set_union (a.begin(), a.end(), b.begin(), b.end(), inserter(unionset, unionset.begin()));
    return int_size/(double)unionset.size();
  }
}

map<string, double> distances(vector<vector<string> > a) {
  map<string, double> res;
  size_t c = 0;
  for (size_t i=0; i<a.size(); i++) {
    for (size_t j=i+1; j<a.size(); j++) {
      double sim = jaccard_similarity(a[i], a[j]);
      if (sim != 0) {
        ostringstream ss;
        ss << i << ";" << j;
        res[ss.str()] = 1/sim;
      }
      c++;
      if (c % 1000000 == 0) {
        cout << "Computed " << c << " jaccard similarity" << endl;
      }
    }
  }
  return res;
}
