import {useSession} from "next-auth/react";
import Link from "next/link";


export default function AuthState(){

	const { data: session, status } = useSession()

	if (status === "authenticated") {
		console.log("authenticated");
		return (
			<div className="mt-16">Signed in as {session?.user?.email}</div>
		)
	}

	return (
		<a className="mt-16" href="/api/auth/signin">Signed in as {session?.user?.email}</a>
	)
}