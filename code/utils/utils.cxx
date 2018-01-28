#include <algorithm>
#include <set>
#include <map>
#include <unordered_map>
#include <limits>
#include <iostream>
#include <sstream>

#include "utils.h"

using namespace std;

double similarity(vector<string> a, vector<string> b) {
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

vector<size_t> clustering(vector<vector<string> > a, double max_d) {
  map<double, set<pair<size_t, size_t> > > distances;
  size_t c1 = 0;
  size_t c2 = 0;
  for (size_t i=0; i<a.size(); i++) {
    for (size_t j=i+1; j<a.size(); j++) {
      double sim = jaccard_similarity(a[i], a[j]);
      if (sim != 0 && sim >= 1/max_d) {
        double d = 1/sim;
        pair<size_t, size_t> p = make_pair(i, j);
        auto it = distances.find(d);
        if (it == distances.end()) {
          set<pair<size_t, size_t> > s;
          s.insert(p);
          distances[d] = s;
        }
        else {
          it->second.insert(p);
        }
        c2++;
      }
      c1++;
      if (c1 % 1000000 == 0) {
        cout << "Computed " << c1 << " jaccard similarities" << endl;
      }
    }
  }
  cout << "All distances computed! " << c2 << endl;
  vector<size_t> res;
  for (size_t i=0; i<a.size(); i++) {
    res.push_back(i);
  }
  while(distances.size() > 0) {
    auto distances_it = distances.begin();
    size_t d = distances_it->first;
    if (d <= max_d) {
      set<pair<size_t, size_t> >& s = distances_it->second;
      auto it = s.begin();
      s.erase(it);
      pair<size_t, size_t> p = *it;
      if (s.size() == 0) {
        distances.erase(distances_it);
      }
      size_t i = p.first;
      size_t j = p.second;
      size_t r = res[j];
      if (r != res[i]) {
        for (size_t k=0; k<res.size(); k++) {
          if (res[k] == r) {
            res[k] = res[i];
          }
        }
      }
    }
    else {
      break;
    }
  }
  cout << "End C++" << endl << endl;
  return res;
}

vector<size_t> clustering_lsh(vector<vector<string> > a, vector<vector<size_t> > candidates_lists, double max_d) {
  cout << "Start c++" << endl;
  size_t c1 = 0;
  size_t c2 = 0;
  set<pair<size_t, size_t> > s;
  for (auto& list : candidates_lists) {
    for (size_t x = 0; x < list.size()-1; x++){
      for (size_t y = x+1; y < list.size(); y++){
        size_t i = list[x];
	size_t j = list[y];
        pair<size_t, size_t> p = make_pair(i, j);
        double sim = jaccard_similarity(a[i], a[j]);
        if (sim != 0 && sim >= 1/max_d) {
          s.insert(p);
          c2++;
        }
        c1++;
        if (c1 % 1000000 == 0) {
          cout << "Computed " << c1 << " jaccard similarities" << endl;
        }
      }
    }
  }
  cout << "All distances computed! " << c2 << endl;
  vector<size_t> res;
  for (size_t i=0; i<a.size(); i++) {
    res.push_back(i);
  }
  while(s.size() > 0) {
    auto it = s.begin();
    s.erase(it);
    pair<size_t, size_t> p = *it;
    size_t i = p.first;
    size_t j = p.second;
    size_t r = res[j];
    if (r != res[i]) {
      for (size_t k=0; k<res.size(); k++) {
        if (res[k] == r) {
          res[k] = res[i];
        }
      }
    }
  }
  cout << "End C++" << endl << endl;
  return res;
}
