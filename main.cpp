#include <iostream>
#include <algorithm>
#include <vector>
#include <numeric>
#include <set>
#include <utility>
#include <random>
#include <fstream>
#include <time.h>

using namespace std;
std::random_device rd;

class Node {
    public: Node* parent;
    public: int size;
};

Node* find(Node *x){
  if (x->parent != x) {
    x->parent = find(x->parent);
    return x->parent;
  }
  return x;
}

Node* merge(Node *u, Node *v){
  Node* x = find(u);
  Node* y = find(v);
  if (x == y){
    return x;
  }
  if (x->size < y->size){
    swap(x, y);
  }
  y->parent = x;
  x->size += y->size;
  return x;
}


int algo(int n){
  vector<Node*> nodes(n);
  for (int i = 0; i < n; ++i) {
    nodes[i] = new Node();
    nodes[i]->parent = nodes[i];
    nodes[i]->size = 1;
  }
  double thresh = n/2.;
  set<pair<int, int>> seen = {};
  std::mt19937 rng(rd());
  std::uniform_int_distribution<int> uni(0,n-1);

  auto i = 0;
  while (true) {
    auto ui = uni(rng);
    auto vi = uni(rng);
    if (ui == vi){
      continue;
    }
    if (ui < vi){
      swap(ui, vi);
    }
    if (seen.contains(make_pair(ui, vi))){
      continue;
    }
    i ++;
    Node* u = nodes[ui];
    Node* v = nodes[vi];
    Node* x = merge(u, v);
    if (x->size > thresh){
      for (auto p : nodes){
         delete p;
       } 
       nodes.clear();
      return i+1;
    }
  }
}


int main(){
  vector<int> nodes{
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
  };

  int trials = 1000;
  vector<double> avg(nodes.size());
  vector<double> duration(nodes.size());
  for (int i = 0; i < nodes.size(); ++i) {
    cout << i << "\n" << endl;
    double avg_m = 0;
    double duration_m = 0;
    for (int j = 0; j <trials; ++j) {
      const clock_t start = clock();
      auto m = algo(nodes[i]);
      duration_m += (clock () - start)*1.0/trials;
      avg_m += (1.*m)/trials;
    }
    avg[i] = avg_m;
    duration[i] = duration_m/CLOCKS_PER_SEC;
  }
  std::ofstream trials_file("./trials.txt");
  std::ofstream avg_m_file("./avg_m.txt");
  std::ofstream avg_t_file("./avg_t.txt");
  std::ofstream nodes_file("./nodes.txt");
  trials_file << trials << "\n";
  for (const auto &e : avg) avg_m_file << e << "\n";
  for (const auto &e : duration) avg_t_file << e << "\n";
  for (const auto &e : nodes) nodes_file << e << "\n";
  return 0;
}
