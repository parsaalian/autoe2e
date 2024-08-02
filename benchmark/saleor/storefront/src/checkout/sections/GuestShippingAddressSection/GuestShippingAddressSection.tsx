import React from "react";
import { AddressForm } from "@/checkout/components/AddressForm";
import { FormProvider } from "@/checkout/hooks/useForm/FormProvider";
import { useAvailableShippingCountries } from "@/checkout/hooks/useAvailableShippingCountries";
import { useGuestShippingAddressForm } from "@/checkout/sections/GuestShippingAddressSection/useGuestShippingAddressForm";

export const GuestShippingAddressSection = () => {
	const { availableShippingCountries } = useAvailableShippingCountries();

	const form = useGuestShippingAddressForm();

	const { handleChange, handleBlur } = form;

	return (
		<FormProvider form={form} formid="f-guest-shipping">
			<AddressForm
				title="Shipping address"
				availableCountries={availableShippingCountries}
				fieldProps={{
					onChange: handleChange,
					onBlur: handleBlur,
				}}
			/>
		</FormProvider>
	);
};
