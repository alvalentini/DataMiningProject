#include <algorithm>
#include <set>
#include <limits>

#include "utils.h"

double jaccard_similarity(std::vector<std::string> a, std::vector<std::string> b) {
    std::set<std::string> intersect;
    std::set<std::string> unionset;
    std::set_intersection (a.begin(), a.end(), b.begin(), b.end(), std::inserter(intersect, intersect.begin()));
    std::set_union (a.begin(), a.end(), b.begin(), b.end(), std::inserter(unionset, unionset.begin()));
    return intersect.size()/(double)unionset.size();
}

std::vector<double> distances(std::vector<std::vector<std::string> > a) {
    std::vector<double> res;
    for (size_t i=0; i<a.size(); i++) {
        for (size_t j=i+1; j<a.size(); j++) {
            double sim = jaccard_similarity(a[i], a[j]);
            if (sim == 0) {
                res.push_back(std::numeric_limits<double>::max());
            }
            else {
                res.push_back(1/sim);
            }
        }
    }
    return res;
}
