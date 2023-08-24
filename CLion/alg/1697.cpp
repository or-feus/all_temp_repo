#include <bits/stdc++.h>

using namespace std;

int a[200004];
int s, e, ret;
int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	cin >> s >> e;

	queue<int> q;
	a[s] = 1;
	q.push(s);

	while (q.size()) {
		int go = q.front();
		q.pop();
		if(go == e){
			ret = a[go];
			break;
		}

		for (int next: {go - 1, go + 1, go * 2}) {
			if(a[next]) continue;
			if(next > 100000) continue;
			a[next] = a[go] + 1;
			q.push(next);
		}
	}

	cout << ret - 1 << "\n";

	return 0;
}