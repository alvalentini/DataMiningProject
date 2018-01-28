#include <vector>
#include <map>
#include <set>
#include <string>

double similarity(std::vector<std::string> a, std::vector<std::string> b);

std::map<std::string, double> distances(std::vector<std::vector<std::string> > a);

std::vector<std::size_t> clustering(std::vector<std::vector<std::string> > features, std::vector<std::vector<std::string> > links,
                                    std::vector<std::vector<std::string> > hashtags, std::vector<std::vector<std::string> > tags,
                                    double max_d);

std::vector<std::size_t> clustering_lsh(std::vector<std::vector<std::string> > features, std::vector<std::vector<std::string> > links,
                                        std::vector<std::vector<std::string> > hashtags, std::vector<std::vector<std::string> > tags,
                                        std::vector<std::vector<std::size_t> > candidates_lists, double max_d);
