import {NextApiRequest, NextApiResponse} from "next";
import withHandler, {ResponseType} from "@libs/server/withHandler";
import client from "@libs/server/client";
import {withApiSession} from "@libs/server/withSession";


async function handler(
	req: NextApiRequest,
	res: NextApiResponse<ResponseType>
) {

	const {
		body: { name, price, description },
		session: { user },
	} = req;


	if (req.method === "POST") {
		const stream = await client.stream.create({
			data: {
				name,
				price: +price,
				description,
				user: {
					connect: {
						id: user?.id,
					},
				},
			},
		});
		res.json({
			ok: true,
			stream,
		});
	}else if (req.method === "GET") {
		const streams = await client.stream.findMany()
		res.json({
			ok: true,
			streams
		})
	}

}

export default withApiSession(withHandler({
	methods: ["GET", "POST"],
	handler
}))