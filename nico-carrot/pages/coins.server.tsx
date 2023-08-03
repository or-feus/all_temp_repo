import {Suspense} from "react"

const cache: any = {}

function fetchData(url: string) {
	if (!cache[url]) {
		throw fetch(url)
			.then(res => res.json())
			.then(json => cache[url] = json),
			new Promise(resolve => setTimeout(resolve, Math.round(Math.random() * 15555)))
	}
	return cache[url]
}

function Coin({ id, name, symbol }: any) {
	const { quotes: { USD: { price } } } = fetchData(`https://api.coinpaprika.com/v1/tickers/${id}`)
	console.log(price)
	return (
		<span>
			{name} / {symbol}: ${price}
		</span>
	)
}

function List() {

	const coins = fetchData("https://api.coinpaprika.com/v1/coins")
	return (
		<div>
			<h4>List is done</h4>
			<ul>
				{coins.slice(0, 10)
					.map((coin: any) =>
						<li	key={coin.id}>
							<Suspense
								fallback={<div>Coin ${coin.name} is loading</div>}>
								<Coin key={coin.id} {...coin} />
							</Suspense>
						</li>
					)}
			</ul>
		</div>
	)
}

export default function CoinsServer() {
	return (
		<div>
			<h1>Welcome to RSC</h1>
			<Suspense fallback="rendering in the Server">
				<List/>
			</Suspense>
		</div>
	)
}