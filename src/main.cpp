#include <stdio.h> 
#include <vector>
#include <math.h>
#include <iostream>
#include <fstream>

unsigned int count(std::vector<std::vector<bool> > grid, int i, int j, int N, std::vector<std::vector<int> > neighbours) {
    // Returns the number of occupied cells
    unsigned int current = 0;
    for(std::vector<int> off : neighbours) {
        int x = (i + off[0]) % N;
        int y = (j + off[1]) % N;
        if(x < 0) x += N;
        if(y < 0) y += N;

        if(grid[x][y])
            current++;
    }
    return current;
}

float p(int x, float T) {

    return exp(- ((float) x) * T / 6.0);

}
int main() {

    // Define the grid, classic.
    int ITERATIONS = 100000;
    int N = 100;
    std::vector<std::vector<bool> > grid(N, std::vector<bool>(N, 0));
    std::vector<std::vector<int> > neighbours{{-1, 0}, {-1, 1}, {0, 1}, {1, 0}, {1, -1}, {0, -1}};
    
    int start = N / 2;
    grid[start][start] = true;
    for(int n=0; n < 6; n++) {
            grid[start + neighbours[n][0]][start + neighbours[n][1]] = true;
    }      

    int x;
    int y;
    for(int iter=0; iter < ITERATIONS; iter++) {
        if(iter % 100 == 0)
            std::cout << iter << "\n";            
        
        x = rand() % N;
        y = rand() % N;

        float prob = p(count(grid, x, y, N, neighbours), 5.41);
        if (prob < 1)
            std::cout << prob << std::endl;
        if(prob < 0.5) {
            grid[x][y] = true; 
        }
        /*
        for(int i=0; i < N; i++) {
            for(int j=0; j < N; j++) {
                if(!grid[i][j]) {
                    float derp =exp(- (float) count(grid, i, j, N, neighbours));
                    if(derp < (float) rand() / (float) RAND_MAX) {
                        grid[i][j] = true;
                    }
                }
            }
        }
        */
    }
    
    std::ofstream out("flaky.csv");

    for(int i=0; i < N; i++) {
        for(int j=0; j < N; j++) {
           out << grid[i][j] << ","; 
        }
        out << "\n";
    }
    out.close();
    return 0;
}