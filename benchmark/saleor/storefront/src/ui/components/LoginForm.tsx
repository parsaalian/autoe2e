"use client";
import { loginSubmit } from "@/serverLogic";
import { logToServer } from "@/logger";

export async function LoginForm() {
	return (
		<div className="mx-auto mt-16 w-full max-w-lg">
			<form className="rounded border p-8 shadow-md" data-formid="f-login" action={loginSubmit}>
				<div className="mb-2">
					<label className="sr-only" htmlFor="email">
						Email
					</label>
					<input
						type="email"
						name="email"
						placeholder="Email"
						className="w-full rounded border bg-neutral-50 px-4 py-2"
						onChange={() => {
							logToServer("t1-login-email");
						}}
						data-testid="t1-login-email"
					/>
				</div>
				<div className="mb-4">
					<label className="sr-only" htmlFor="password">
						Password
					</label>
					<input
						type="password"
						name="password"
						placeholder="Password"
						autoCapitalize="off"
						autoComplete="off"
						className="w-full rounded border bg-neutral-50 px-4 py-2"
						onChange={() => {
							logToServer("t2-login-password");
						}}
						data-testid="t2-login-password"
					/>
				</div>

				<button
					className="rounded bg-neutral-800 px-4 py-2 text-neutral-200 hover:bg-neutral-700"
					type="submit"
					onClick={() => {
						logToServer("c6-login-button");
					}}
					data-testid="c6-login-button"
					data-submitid="f-login"
				>
					Log In
				</button>
			</form>
			<div></div>
		</div>
	);
}
