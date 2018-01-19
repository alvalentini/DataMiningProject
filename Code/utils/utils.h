#include <vector>
#include <map>
#include <set>
#include <string>

std::map<std::string, double> distances(std::vector<std::vector<std::string> > a);

std::vector<std::size_t> clustering(std::vector<std::vector<std::string> > a, int max_d);

std::vector<std::size_t> clustering_lsh(std::vector<std::vector<std::string> > a, std::set<std::string> pairs, int max_d);
