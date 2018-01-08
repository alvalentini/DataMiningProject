#include <algorithm>
#include <set>
#include <limits>
#include <iostream>

#include "utils.h"

double jaccard_similarity(const std::vector<std::string>& a, const std::vector<std::string>& b) {
    std::set<std::string> intersect;
    std::set<std::string> unionset;
    std::set_intersection (a.begin(), a.end(), b.begin(), b.end(), std::inserter(intersect, intersect.begin()));
    size_t int_size = intersect.size();
    if (int_size == 0) {
        return 0.;
    }
    else {
        std::set_union (a.begin(), a.end(), b.begin(), b.end(), std::inserter(unionset, unionset.begin()));
        return int_size/(double)unionset.size();
    }
}

std::vector<double> distances(std::vector<std::vector<std::string> > a) {
    std::vector<double> res;
    size_t c = 0;
    for (size_t i=0; i<a.size(); i++) {
        for (size_t j=i+1; j<a.size(); j++) {
            double sim = jaccard_similarity(a[i], a[j]);
            if (sim == 0) {
                res.push_back(std::numeric_limits<double>::max());
            }
            else {
                res.push_back(1/sim);
            }
            c++;
            if (c % 1000000 == 0) {
              std::cout << "Computed " << c << " jaccard similarity" << std::endl;
            }
        }
    }
    return res;
}
