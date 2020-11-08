#include <iostream>
#include <vector>

using namespace std;

bool isReceptive(vector<vector<float>> grid, int i, int j, vector<vector<int> > neighbours, int N) {
    bool receptive = false;
    for(vector<int> offset : neighbours) {
        int x = (i + offset[0]);
        int y = j + offset[0];
        
        if (x < 0 || x >= N || y < 0 || y >= N)
            continue;
        else if(grid[x][y])
            return true;
    }
    return false;
}
int main() {
    int size = 256 + 2;
    
    float alpha = 1.0;
    float beta = 0.3;
    float gamma = 0.01;

    vector<vector<float> > grid = vector<vector<float> >(size, vector<float>(size, 0.0));
    grid[size / 2][size / 2] = 1;


}