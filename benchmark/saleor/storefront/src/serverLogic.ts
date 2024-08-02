"use server";
import { redirect } from "next/navigation";
import { getServerAuthClient } from "@/app/config";

export async function loginSubmit(formData) {
    const email = formData.get("email")?.toString();
    const password = formData.get("password")?.toString();

    if (!email || !password) {
        throw new Error("Email and password are required");
    }

    const { data } = await getServerAuthClient().signIn({ email, password }, { cache: "no-store" });

    if (data.tokenCreate.errors.length > 0) {
        // setErrors(data.tokenCreate.errors.map((error) => error.message));
        // setFormValues(DefaultValues);
    }
}

export async function searchSubmit(channel: string, formData: FormData) {
    const search = formData.get("search") as string;
    if (search && search.trim().length > 0) {
        redirect(`/${encodeURIComponent(channel)}/search?query=${encodeURIComponent(search)}`);
    }
}