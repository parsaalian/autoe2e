import React from "react";
import { SignInFormContainer, type SignInFormContainerProps } from "../Contact/SignInFormContainer";
import { Button } from "@/checkout/components/Button";
import { PasswordInput } from "@/checkout/components/PasswordInput";
import { useResetPasswordForm } from "@/checkout/sections/ResetPassword/useResetPasswordForm";
import { FormProvider } from "@/checkout/hooks/useForm/FormProvider";

interface ResetPasswordProps extends Pick<SignInFormContainerProps, "onSectionChange"> {
	onResetPasswordSuccess: () => void;
}

export const ResetPassword: React.FC<ResetPasswordProps> = ({ onSectionChange, onResetPasswordSuccess }) => {
	const form = useResetPasswordForm({ onSuccess: onResetPasswordSuccess });

	return (
		<SignInFormContainer
			title="Reset password"
			redirectSubtitle="Remembered your password?"
			redirectButtonLabel="Sign in"
			onSectionChange={onSectionChange}
			subtitle="Provide a new password for your account"
		>
			<FormProvider form={form} formid="f-reset-password">
				<PasswordInput name="password" label="Password" required clickId="t8-checkout-reset-password" />
				<div className="mt-4 flex w-full flex-row items-center justify-end">
					<Button
						ariaLabel="Reset password"
						label="Reset password"
						type="submit"
						clickId="c30-checkout-reset-password-submit"
					/>
				</div>
			</FormProvider>
		</SignInFormContainer>
	);
};
