import Document, { Head, Html, Main, NextScript } from "next/document";

class CustomDocument extends Document {
	render(): JSX.Element {
		console.log("DOCUMENT IS RUNNING");
		return (
			<Html lang="ko">
				<Head>
					<link
						href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
						rel="stylesheet"
					/>
				</Head>
				<body>
				<Main/>
				<NextScript/>
				</body>
			</Html>
		);
	}
}

export default CustomDocument

// import {Head, Html, Main, NextScript} from "next/document";
//
//
// export default function MyDocument() {
// 	return (
// 		<Html lang="ko">
// 			<Head>
// 				<link
// 					href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR&family=Open+Sans:wght@300;400&display=swap"
// 					rel="stylesheet"/>
// 			</Head>
// 			<body>
// 			<Main/>
// 			<NextScript/>
// 			</body>
// 		</Html>
// 	)
// }
//
