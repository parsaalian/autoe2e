import { type SelectHTMLAttributes, type ChangeEvent, type ReactNode, useState } from "react";
import { useField } from "@/checkout/hooks/useForm/useField";
import { logToServer } from "@/logger";

export interface Option<TData extends string = string> {
	label: ReactNode;
	value: TData;
	disabled?: boolean;
	icon?: ReactNode;
	[key: string]: unknown;
}

interface SelectProps<TName extends string, TData extends string>
	extends SelectHTMLAttributes<HTMLSelectElement> {
	name: TName;
	label?: ReactNode;
	onChange?: (event: ChangeEvent<HTMLSelectElement>) => void;
	options: Option<TData>[];
	clickId: string;
}

export const Select = <TName extends string, TData extends string>({
	name,
	placeholder,
	onChange,
	options,
	label,
	clickId,
	...rest
}: SelectProps<TName, TData>) => {
	const { error, handleBlur, ...fieldProps } = useField(name);

	const [showPlaceholder, setShowPlaceholder] = useState(!!placeholder);

	const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
		if (!event.currentTarget.value) {
			return;
		}

		setShowPlaceholder(false);
		onChange?.(event);
		fieldProps.onChange(event);
	};

	return (
		<div className="space-y-0.5">
			<label className="flex flex-col">
				<span className="text-xs text-neutral-700">{label}</span>
				<select
					{...fieldProps}
					{...rest}
					onBlur={handleBlur}
					onChange={(e) => {
						handleChange(e);
						logToServer(clickId);
					}}
					data-testid={clickId}
					className="mt-1 block w-full rounded-md border-neutral-300 shadow-sm focus:border-neutral-300 focus:ring focus:ring-neutral-200 focus:ring-opacity-50"
				>
					{showPlaceholder && (
						<option disabled value="">
							{placeholder}
						</option>
					)}
					{options.map(({ label, value, disabled = false }) => (
						<option value={value} disabled={disabled} key={label?.toString() + "_" + value}>
							{label}
						</option>
					))}
				</select>
			</label>
			{error && <p className="text-sm text-red-500">{error}</p>}
		</div>
	);
};
