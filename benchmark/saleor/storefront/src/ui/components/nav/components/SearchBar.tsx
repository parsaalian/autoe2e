"use client";
import { SearchIcon } from "lucide-react";
import { searchSubmit } from "@/serverLogic";
import { logToServer } from "@/logger";

export const SearchBar = ({ channel }: { channel: string }) => {
	return (
		<form
			action={(formData) => searchSubmit(channel, formData)}
			className="group relative my-2 flex w-full items-center justify-items-center text-sm lg:w-80"
			data-formid="f-search"
		>
			<label className="w-full">
				<span className="sr-only">search for products</span>
				<input
					type="text"
					name="search"
					placeholder="Search for products..."
					autoComplete="on"
					required
					className="h-10 w-full rounded-md border border-neutral-300 bg-transparent bg-white px-4 py-2 pr-10 text-sm text-black placeholder:text-neutral-500 focus:border-black focus:ring-black"
					onChange={() => logToServer("t3-search-term")}
					data-testid="t3-search-term"
				/>
			</label>
			<div className="absolute inset-y-0 right-0">
				<button
					type="submit"
					className="inline-flex aspect-square w-10 items-center justify-center text-neutral-500 hover:text-neutral-700 focus:text-neutral-700 group-invalid:pointer-events-none group-invalid:opacity-80"
					onClick={() => logToServer("c12-search-button")}
					data-testid="c12-search-button"
					data-submitid="f-search"
				>
					<span className="sr-only">search</span>
					<SearchIcon aria-hidden className="h-5 w-5" />
				</button>
			</div>
		</form>
	);
};
