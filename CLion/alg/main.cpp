#include <bits/stdc++.h>

using namespace std;
string s;
int ret = 0;
int len;
int main() {

	ios::sync_with_stdio(false);

	cin >> len;

	for (int i = 0; i < len; i++) {
		char num = 0;
		scanf("%c", &num);
		ret += (int)num;
	}

	cout << ret << '\n';

	return 0;
}
