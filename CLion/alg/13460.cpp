#include <bits/stdc++.h>

using namespace std;

int n, m;
char a[14][14];

int dy[4] = {0, 1, 0, -1};
int dx[4] = {1, 0, -1, 0};

int ry = 0, rx = 0, bx = 0, by = 0;
int it, ret= 9999999;
bool blue_in;

void update_pos() {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			if (a[i][j] == 'R') {
				ry = i;
				rx = j;
			} else if (a[i][j] == 'B') {
				by = i;
				bx = j;
			}
		}
	}
}

void init_mem() {
	cin >> n >> m;

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> a[i][j];
		}
	}
}

int obj_move(int rot) {
	// 0 -> success
	// 1 -> hole in one;
	// -1 -> failed;
	int flag = 99;

	while (1) {
		int ny = ry + dy[rot];
		int nx = rx + dx[rot];
		if(ny < 0 || nx < 0 || ny >= n || nx >= m || a[ny][nx] == '#' || a[ny][nx] == 'B') {
			flag = 0;
			break;
		}else if(a[ny][nx] == 'O'){
			a[ry][rx] = '.';
			flag = 1;
			break;
		}else {
			a[ny][nx] = 'R';
			a[ry][rx] = '.';
			ry = ny;
			rx = nx;
		}
	}
	while (1) {

		int ny = by + dy[rot];
		int nx = bx + dx[rot];
		if(ny < 0 || nx < 0 || ny >= n || nx >= m || a[ny][nx] == '#' || a[ny][nx] == 'R') {

			flag == 1? 1 :  0;
			break;
		}else if(a[ny][nx] == 'O'){
			flag = -1;
			break;
		}else {
			a[ny][nx] = 'B';
			a[by][bx] = '.';
			by = ny;
			bx = nx;
		}
	}
//	cout << flag << "\n";

	return flag;
}
void back_move(int nry, int nrx, int nby, int nbx){
	a[nry][nrx] = '.';
	a[nby][nbx] = '.';
	a[ry][rx] = 'R';
	a[by][bx] = 'B';
}
void go(int rot, int flag, int idx){
	if(idx > 10) return;
	if(flag == -1) {
		blue_in = true;
		return;
	}
	if(flag == 1) {
		cout << "here\n";
		ret = min(ret, idx);
		return;
	}

	for (int i = 0; i < 4; i++) {
		update_pos();
		int save_by = by, save_bx = bx, save_ry = ry, save_rx = rx;
		int f = obj_move(i);
		go(i, f, idx+1);
		back_move(save_ry, save_rx, save_by, save_bx);
	}
}
int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	// 회전 문제
	// 실패 기준
	// 1. 빨간 구슬과 파란 구슬이 동시에 구멍에 빠져도 실패
	// 2. 파란 구슬이 구멍에 들어가면 실패

	// 구슬이 움직이지 않을 때 까지 회전 가능
	// 10번 이상 넘어가면 return -1
	// 최소 몇 번만에 빨간 구슬을 구멍을 통해 빼낼 수 있는지 구하는 프로그램

	init_mem();

	update_pos();
	for (int i = 0; i < 4; i++) {
		obj_move(i);
	}

	go(-1, 99, 0);

//	for (int i = 0; i < n; i++) {
//		for (int j = 0; j < m; j++) {
//			cout << a[i][j] << " ";
//		}
//		cout << "\n";
//	}
	if(blue_in){
		cout << -1 << '\n';
	}else {
		cout << (ret == 9999999 ? -1 : ret) << '\n';
	}
	return 0;
}