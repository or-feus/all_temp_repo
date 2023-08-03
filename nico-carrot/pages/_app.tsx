import "../styles/globals.css";
import type {AppProps} from "next/app";
import {SWRConfig} from "swr";
import Script from "next/script";
import { SessionProvider } from "next-auth/react";

function MyApp({ Component, pageProps }: AppProps) {
	return (
		<SessionProvider>
			<SWRConfig
				value={{
					fetcher: (url: string) =>
						fetch(url)
							.then((response) => response.json()),
				}}
			>
				<div className="w-full max-w-xl mx-auto">
					<Component {...pageProps} />
				</div>
				<Script
					src="https://developers.kakao.com/sdk/js/kakao.js"
					strategy="beforeInteractive"/>
			</SWRConfig>
		</SessionProvider>
	);
}

export default MyApp;
