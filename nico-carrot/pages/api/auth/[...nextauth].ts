import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {verifyPassword} from "@libs/server/auth";
import client from "@libs/server/client"

export default NextAuth({
	providers: [
		CredentialsProvider({
			// The name to display on the sign in form (e.g. "Sign in with...")
			name: "Credentials",
			// The credentials is used to generate a suitable form on the sign in page.
			// You can specify whatever fields you are expecting to be submitted.
			// e.g. domain, username, password, 2FA token, etc.
			// You can pass any HTML attribute to the <input> tag through the object.
			credentials: {
				email: { label: "email", type: "email", placeholder: "jsmith@naver.com" },
				password: { label: "Password", type: "password" }
			},
			async authorize(credentials) {
				const user = await client.user.findUnique({
					where : {
						email: String(credentials.email),
					},
					select: {
						name: true, email: true, password: true
					},
				});

				if (!user) {
					throw new Error('No user found!');
				}

				const isValid = await verifyPassword(
					credentials.password,
					user.password
				);

				if (!isValid) {
					throw new Error('Could not log you in!');
				}
				return { name: user.name, email: user.email };
			}
		})
	],
	secret   : process.env.SECRET
})