import { withIronSessionApiRoute} from "iron-session/next";
import { NextApiRequest, NextApiResponse } from "next";
import withHandler, { ResponseType } from "@libs/server/withHandler";
import client from "@libs/server/client";
import profile from "../../profile";
import { withApiSession } from "@libs/server/withSession";


async function handler(
	req: NextApiRequest,
	res: NextApiResponse<ResponseType>
) {
	const profile = await client.user.findUnique({
		where: {
			id: req.session.user?.id
			// id: undefined
		},
	})
	res.json({
		ok: true,
		...profile
	})

	res.status(200).end();
	console.log(profile)
}

export default withApiSession(withHandler({
	methods:["GET"],
	handler
}))