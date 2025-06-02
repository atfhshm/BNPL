import { isValidPhoneNumber } from "react-phone-number-input";
import { z } from "zod";

export const signInSchema = z.object({
    login: z.string().min(1, { message: "Please enter your login" }),
    password: z
        .string()
        .min(8, { message: "Password must be at least 8 characters long" }),
});
export type SignInFormSchema = z.infer<typeof signInSchema>;

export const signUpSchema = z
    .object({
        first_name: z
            .string()
            .min(1, { message: "Please enter your first name" }),
        last_name: z
            .string()
            .min(1, { message: "Please enter your last name" }),
        email: z
            .string()
            .email({ message: "Please enter a valid email address" }),
        phone_number: z
            .string()
            .min(11, { message: "Please enter your phone number" })
            .refine((value) => isValidPhoneNumber(value), {
                message: "Invalid phone number",
            }),
        password: z
            .string()
            .min(8, { message: "Password must be at least 8 characters long" }),
        confirm_password: z
            .string()
            .min(8, { message: "Password must be at least 8 characters long" }),
    })
    .refine((data) => data.password === data.confirm_password, {
        message: "Passwords do not match",
        path: ["confirm_password"],
    });
export type SignUpFormSchema = z.infer<typeof signUpSchema>;
