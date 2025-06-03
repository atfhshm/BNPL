import { AuthAPI, PublicAPI } from "~/lib/api";
import type { SignInFormSchema, SignUpFormSchema } from "./schemas";
import type { ITokenResponse, IUser } from "~/types/auth";
import type { AxiosResponse } from "axios";

export async function signInRequest(
    data: SignInFormSchema
): Promise<AxiosResponse<ITokenResponse>> {
    return await PublicAPI.post("/api/v1/auth/login/", data);
}

export async function signUpCustomerRequest(
    data: SignUpFormSchema
): Promise<AxiosResponse<ITokenResponse>> {
    return await PublicAPI.post("/api/v1/auth/customer-register/", data);
}
export async function signUpMerchantRequest(
    data: SignUpFormSchema
): Promise<AxiosResponse<ITokenResponse>> {
    return await PublicAPI.post("/api/v1/auth/merchant-register/", data);
}

export async function getCurrentUserRequest(): Promise<AxiosResponse<IUser>> {
    return await AuthAPI.get("/api/v1/auth/me/");
}
