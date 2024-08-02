import { Button } from "@/checkout/components/Button";
import { IconButton } from "@/checkout/components/IconButton";
import { TrashIcon } from "@/checkout/ui-kit/icons";

interface AddressFormActionsProps {
	onDelete?: () => void;
	onCancel: () => void;
	onSubmit: () => void;
	loading: boolean;
}

export const AddressFormActions: React.FC<AddressFormActionsProps> = ({
	onSubmit,
	onDelete,
	onCancel,
	loading,
}) => {
	return (
		<div className="flex flex-row justify-end gap-2">
			{onDelete && (
				<div className="flex">
					<IconButton ariaLabel="Delete address" onClick={onDelete} icon={<TrashIcon aria-hidden />} />
				</div>
			)}

			<Button
				ariaLabel="Cancel editing"
				variant="secondary"
				onClick={onCancel}
				label="Cancel"
				clickId="c36-cancel-edit-address"
			/>
			{loading ? (
				<Button
					ariaDisabled
					ariaLabel="Save address"
					onClick={(e) => e.preventDefault()}
					label="Processing…"
					clickId="c37-save-address-processing"
				/>
			) : (
				<Button
					ariaLabel="Save address"
					onClick={onSubmit}
					label="Save address"
					clickId="c38-save-edit-address"
				/>
			)}
		</div>
	);
};
