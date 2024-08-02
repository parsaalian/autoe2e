"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { type ComponentProps } from "react";
import { logToServer } from "@/logger";

export const LinkWithChannel = ({
	href,
	...props
}: Omit<ComponentProps<typeof Link>, "href"> & { href: string } & { clickId: string }) => {
	const { channel } = useParams<{ channel?: string }>();

	if (!href.startsWith("/")) {
		return (
			<Link
				{...props}
				href={href}
				onClick={() => {
					logToServer(props.clickId);
				}}
				data-testid={props.clickId}
			/>
		);
	}

	const encodedChannel = encodeURIComponent(channel ?? "");
	const hrefWithChannel = `/${encodedChannel}${href}`;
	return (
		<Link
			{...props}
			href={hrefWithChannel}
			onClick={() => {
				logToServer(props.clickId);
			}}
			data-testid={props.clickId}
		/>
	);
};
