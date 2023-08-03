import {NextApiRequest, NextApiResponse} from "next";
import withHandler, {ResponseType} from "@libs/server/withHandler";
import client from "@libs/server/client";
import {withApiSession} from "@libs/server/withSession";


async function handler(
	req: NextApiRequest,
	res: NextApiResponse<ResponseType>
) {

	const {
		query  : { id },
		session: { user }
	} = req
	const alreadyExists = await client.favorite.findFirst({
		where: {
			productId: +id.toString(),
			userId   : user?.id
		}
	})
	if (alreadyExists) {
		await client.favorite.delete({
			where: {
				id: alreadyExists.id
			}
		});
	} else {
		await client.favorite.create({
			data: {
				user: {
					connect: {
						id: user
					}
				}
			}
		})
	}

	res.json({
		ok: true,
	});
}

export default withApiSession(withHandler({
	methods: ["POST"],
	handler
}))