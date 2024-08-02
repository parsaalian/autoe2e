"use client";

import { useTransition } from "react";
import { deleteLineFromCheckout } from "./actions";
import { logToServer } from "@/logger";

type Props = {
	lineId: string;
	checkoutId: string;
};

export const DeleteLineButton = ({ lineId, checkoutId }: Props) => {
	const [isPending, startTransition] = useTransition();

	return (
		<button
			type="button"
			className="text-sm text-neutral-500 hover:text-neutral-900"
			onClick={() => {
				if (isPending) return;
				startTransition(() => deleteLineFromCheckout({ lineId, checkoutId }));
				logToServer("c25-remove-line-from-cart");
			}}
			aria-disabled={isPending}
			data-testid="c25-remove-line-from-cart"
		>
			{isPending ? "Removing" : "Remove"}
			<span className="sr-only">line from cart</span>
		</button>
	);
};
