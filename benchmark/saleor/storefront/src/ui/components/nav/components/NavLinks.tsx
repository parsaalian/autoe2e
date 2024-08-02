import Link from "next/link";
import { NavLink } from "./NavLink";
import { executeGraphQL } from "@/lib/graphql";
import { MenuGetBySlugDocument } from "@/gql/graphql";

export const NavLinks = async ({ channel }: { channel: string }) => {
	const navLinks = await executeGraphQL(MenuGetBySlugDocument, {
		variables: { slug: "navbar", channel },
		revalidate: 60 * 60 * 24,
	});

	return (
		<>
			<NavLink href="/products" clickId="c13-navbar-products">
				All
			</NavLink>
			{navLinks.menu?.items?.map((item) => {
				if (item.category) {
					return (
						<NavLink key={item.id} href={`/categories/${item.category.slug}`} clickId="c14-navbar-categories">
							{item.category.name}
						</NavLink>
					);
				}
				if (item.collection) {
					return (
						<NavLink
							key={item.id}
							href={`/collections/${item.collection.slug}`}
							clickId="c15-navbar-collections"
						>
							{item.collection.name}
						</NavLink>
					);
				}
				if (item.page) {
					return (
						<NavLink key={item.id} href={`/pages/${item.page.slug}`} clickId="c16-navbar-pages">
							{item.page.title}
						</NavLink>
					);
				}
				if (item.url) {
					// TODO: move to new component and import
					return (
						<Link key={item.id} href={item.url}>
							{item.name}
						</Link>
					);
				}
				return null;
			})}
		</>
	);
};
