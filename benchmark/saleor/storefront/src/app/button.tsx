"use client";
import axios from "axios";

export default function ServerButton({ text, left }: { text: string; left: number }) {
	const handleClick = () => {
		axios
			.get(`http://127.0.0.1:5000/${text}`)
			.then(function (response) {
				console.log(response.data);
			})
			.catch(function (error) {
				console.error("Request failed with status:", error.response.status);
			});
	};

	return <></>;
}

/*
<button style={{ position: "fixed", bottom: 0, left, zIndex: 10000 }} onClick={handleClick}>
	{text}
</button>
*/
