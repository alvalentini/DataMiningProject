#include <algorithm>
#include <set>

#include "utils.h"

double jaccard_similarity(const std::vector<std::string> a, const std::vector<std::string> b) {
    std::set<std::string> intersect;
    std::set<std::string> unionset;
    std::set_intersection (a.begin(), a.end(), b.begin(), b.end(), std::inserter(intersect, intersect.begin()));
    std::set_union (a.begin(), a.end(), b.begin(), b.end(), std::inserter(unionset, unionset.begin()));
    return intersect.size()/(double)unionset.size();
}
