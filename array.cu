#include <cstdio>
#include <array>

template <size_t N>
__global__ void printCumSum(std::array<int, N> arr) {
    printf("Cumsum 0: %d\n", arr[0]);
    for (size_t i = 1; i < arr.size(); ++i) {
        arr[i] += arr[i - 1];
        printf("Cumsum %llu: %d\n", i, arr[i]);
    }
}

int main() {
    std::array<int, 4> arr{10, 5, 20, 23};
    printCumSum<<<1, 1>>>(arr);
    cudaDeviceSynchronize();

    return 0;
}
