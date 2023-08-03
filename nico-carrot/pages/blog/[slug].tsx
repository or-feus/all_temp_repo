import {GetStaticProps, NextPage} from "next";
import {readdirSync} from "fs";
import files from "../api/files";
import matter from "gray-matter";
import {unified} from "unified";
import remarkParse from "remark-parse";
import remarkHtml from "remark-html";

const Post: NextPage<{ post: string }> = ({ post }) => {
	return (
		<div dangerouslySetInnerHTML={{ __html:post }}/>
	)
}


export function getStaticPaths() {
	return {
		paths   : [],
		fallback: "blocking"
	}
}


export const getStaticProps: GetStaticProps = async (context) => {
	const { content } = matter.read(`./posts/${context.params?.slug}.md`);

	const { value } = await unified()
		.use(remarkParse)
		.use(remarkHtml)
		.process(content);
	return {
		props: {
			post: value,
		}
	}
}

export default Post