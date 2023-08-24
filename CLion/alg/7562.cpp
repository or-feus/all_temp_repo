#include <bits/stdc++.h>

using namespace std;

int n, l, sy, sx, ey, ex;
int a[304][304];
bool visited[304][304], can_go[304][304];

int dy[8] = {1, 2, 2, 1, -1, -2, -2, -1};
int dx[8] = {2, 1, -1, -2, -2, -1, 1, 2};

void mapping(int range){
	fill(&visited[0][0], &visited[0][0] + 304 * 304, false);
	fill(&a[0][0], &a[0][0] + 304 * 304, 0);
	fill(&can_go[0][0], &can_go[0][0] + 304 * 304, false);

	for (int i = 0; i < range; i++) {
		for (int j = 0; j < range; j++) {
			can_go[i][j] = true;
		}
	}
}

int bfs(int start_y, int start_x, int end_y, int end_x, int range){

	int ret = -1;

	visited[start_y][start_x] = 1;

	queue<pair<int, int>> q;
	q.push({start_y, start_x});

	while(q.size()){
		int y = q.front().first;
		int x = q.front().second;
		q.pop();
		if(y == end_y && x == end_x){
			ret = a[y][x];
			break;
		}

		for (int i = 0; i < 8; i++) {
			int ny = y + dy[i];
			int nx = x + dx[i];

			if(ny < 0 || nx < 0 || ny >= range || nx >= range || visited[ny][nx]) continue;
			a[ny][nx] = a[y][x] + 1;
			visited[ny][nx] = true;
			q.push({ny, nx});
		}
	}
	return ret;
}

int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	cin >> n;

	for (int i = 0; i < n; i++) {
		cin >> l;
		cin >> sy >> sx;
		cin >> ey >> ex;

		mapping(l);
		cout << bfs(sy, sx, ey, ex, l) << '\n';
	}

	return 0;
}