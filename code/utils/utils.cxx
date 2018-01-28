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

bool intersect(const vector<string>& a, const vector<string>& b) {
  set<string> intersect;
  set_intersection (a.begin(), a.end(), b.begin(), b.end(), inserter(intersect, intersect.begin()));
  return intersect.size() > 0;
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

vector<size_t> perform_clustering(set<pair<size_t, size_t> >& s, size_t size) {
  vector<size_t> res;
  for (size_t i=0; i<size; i++) {
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

vector<size_t> clustering(vector<vector<string> > features, vector<vector<string> > links,
                          vector<vector<string> > hashtags, vector<vector<string> > tags,
                          double max_d) {
  cout << "Start c++" << endl;
  size_t c1 = 0;
  size_t c2 = 0;
  set<pair<size_t, size_t> > s;
  size_t t_size = features.size();
  for (size_t i=0; i<t_size; i++) {
    for (size_t j=i+1; j<t_size; j++) {
      double threshold = 1/max_d;
      if (intersect(links[i], links[j]) ||
          intersect(hashtags[i], hashtags[j]) ||
          intersect(tags[i], tags[j]) ||
          jaccard_similarity(features[i], features[j]) >= threshold) {
        pair<size_t, size_t> p = make_pair(i, j);
        s.insert(p);
        c2++;
      }
      c1++;
      if (c1 % 1000000 == 0) {
        cout << "Computed " << c1 << " jaccard similarities" << endl;
      }
    }
  }
  cout << "All distances computed! " << c2 << endl;
  return perform_clustering(s, t_size);
}

vector<size_t> clustering_lsh(vector<vector<string> > features, vector<vector<string> > links,
                              vector<vector<string> > hashtags, vector<vector<string> > tags,
                              vector<vector<size_t> > candidates_lists, double max_d) {
  cout << "Start c++" << endl;
  size_t c1 = 0;
  size_t c2 = 0;
  set<pair<size_t, size_t> > s;
  size_t t_size = features.size();
  for (auto& list : candidates_lists) {
    for (size_t x = 0; x < list.size()-1; x++){
      for (size_t y = x+1; y < list.size(); y++){
        size_t i = list[x];
	size_t j = list[y];
        double threshold = 1/max_d;
        if (intersect(links[i], links[j]) ||
            intersect(hashtags[i], hashtags[j]) ||
            intersect(tags[i], tags[j]) ||
            jaccard_similarity(features[i], features[j]) >= threshold) {
          pair<size_t, size_t> p = make_pair(i, j);
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
  return perform_clustering(s, t_size);
}
