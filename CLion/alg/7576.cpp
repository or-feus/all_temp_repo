#include <bits/stdc++.h>

using namespace std;

int dy[4] = {0, 1, 0, -1};
int dx[4] = {1, 0, -1, 0};

int n, m, t;
int a[1004][1004];
pair<int, int> st, last;
int ret;

int exist_zero() {
	int zero = 0;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			if (!a[i][j]) {
				zero = true;
				break;
			}
		}
		if (zero) break;
	}
	return zero;
}

int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	cin >> n >> m;
	queue<pair<int, int>> q;

	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
//			cin >> a[i][j];
			cin >> t;

			if(t == 1){
				q.push({i, j});
			}
			a[i][j] = t;
		}
	}
	while (q.size()) {
		int y = q.front().first;
		int x = q.front().second;
		q.pop();

		last = {y, x};


		for (int i = 0; i < 4; i++) {
			int ny = y + dy[i];
			int nx = x + dx[i];

			if (ny < 0 || nx < 0 || ny >= m || nx >= n) continue;
			if (a[ny][nx] == -1 || a[ny][nx] > 0) continue;
			if(a[ny][nx] == 0) {
				a[ny][nx] = a[y][x] + 1;
				q.push({ny, nx});
			}
		}
	}



	cout << (exist_zero() ? ret = -1 : a[last.first][last.second] - 1) << '\n';

	return 0;
}