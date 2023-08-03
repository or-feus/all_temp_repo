import {NextApiRequest, NextApiResponse} from 'next';
import client from "@libs/server/client"
import { prisma } from '@prisma/client';
import { hashPassword } from '@libs/server/auth';

async function handler(req: NextApiRequest, res: NextApiResponse) {
	if (req.method !== 'POST') {
		return;
	}

	const data = req.body;

	const { name, email, password } = data;
	if (!name || !email || !email.includes('@') || !password ||	password.trim().length < 7) {
		res.status(422).json({
			message:
				'password should also be at least 7 characters long.',
			error: true,
		});
		return;
	}
	const existingUser = await client.user.findUnique({
			where: {
				email: email,
			},
			select: {
				email: true, name: true,
			}
		}
	);

	if (existingUser) {
		res.status(422).json({ message: 'User Email already exists!', error: true });
		return;
	}



	const hashedPassword = await hashPassword(password);

	const result = await client.user.create({
		data: {
			name: name,
			email: email,
			password: hashedPassword,
		},
	});

	if (result) {
		res.status(201).json({ message: 'Created user!', error: false });
	} else {
		res.status(422).json({ message: 'Prisma error occured', error: true })
	}
}


export default handler;