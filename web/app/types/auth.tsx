export interface ILoginRequest {
    login: string;
    password: string;
}

export interface ITokenResponse {
    access: string;
    refresh: string;
}

export enum UserType {
    CUSTOMER = "customer",
    MERCHANT = "merchant",
}

export interface IUser {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    user_type: UserType;
    is_active: boolean;
    last_login: string;
    date_joined: string;
    updated_at: string;
}
