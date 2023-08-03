#include <bits/stdc++.h>

using namespace std;
int n, m, b, z;
vector<int> v;

int check(int num){
	int low = 0; int high = n - 1;
	if(num > v[high]) return 0;
	while(low <= high){
		int mid = (low + high) / 2;
		if(v[mid] == num){
			return 1;
		}else if(v[mid] > num){
			high = mid - 1;
		}else if(v[mid] < num){
			low = mid + 1;
		}
	}
	return 0;
}

int main() {

	ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);


	cin >> n;

	for (int i = 0; i < n; i++) {
		cin >> z;
		v.push_back(z);
	}
	sort(v.begin(), v.end());



	cin >> m;


	for (int i = 0; i < m; i++) {
		cin >> b;

		check(b) ? cout << "1\n" : cout << "0\n";
	}


	return 0;
}
