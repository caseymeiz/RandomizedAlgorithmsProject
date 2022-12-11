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
    i++;
    Node* u = nodes[ui];
    Node* v = nodes[vi];
    Node* x = merge(u, v);
    if (x->size > thresh){
      for (auto p : nodes){
         delete p;
       } 
       nodes.clear();
      return i;
    }
  }
}


int main(){
  vector<int> nodes{
25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200
  };

  int trials = 10000;
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
