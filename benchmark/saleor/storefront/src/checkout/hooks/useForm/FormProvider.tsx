import { FormikProvider, Form } from "formik";
import { type PropsWithChildren } from "react";
import { type FormDataBase, type UseFormReturn } from "@/checkout/hooks/useForm";

export const FormProvider = <TData extends FormDataBase>({
	form,
	children,
	formid,
}: PropsWithChildren<{
	form: UseFormReturn<TData>;
	formid: string;
}>) => (
	// @ts-expect-error because we overwrite some methods
	<FormikProvider value={form}>
		<Form action="post" noValidate={true} onSubmit={form.handleSubmit} data-formid={formid}>
			{children}
		</Form>
		<button data-submitid={formid}>x</button>
	</FormikProvider>
);
