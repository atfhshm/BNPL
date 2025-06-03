import { Button } from "~/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "~/components/ui/form";
import axios, { AxiosError } from "axios";
import { Input } from "~/components/ui/input";
import { PasswordInput } from "~/components/password-input";
import { AuthAPI, setTokens } from "~/lib/api";
import { cn } from "~/lib/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { type HTMLAttributes, useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";
import { toast } from "sonner";
import { z } from "zod";
import { signInSchema, type SignInFormSchema } from "../../schemas";
import { useMutation } from "@tanstack/react-query";
import { getCurrentUserRequest, signInRequest } from "../../services";
import { useUserStore } from "~/stores/user-store";
import { UserType } from "~/types/auth";

type SignInFormProps = HTMLAttributes<HTMLFormElement>;

export function SignInForm({ className, ...props }: SignInFormProps) {
    const { setUser } = useUserStore();
    const navigate = useNavigate();
    const form = useForm<SignInFormSchema>({
        resolver: zodResolver(signInSchema),
        defaultValues: {
            login: "",
            password: "",
        },
    });

    const { mutate, isPending } = useMutation({
        mutationFn: signInRequest,
        mutationKey: ["sign-in"],
        onSuccess: async (data) => {
            setTokens(data.data);
            const { data: user } = await getCurrentUserRequest();
            setUser(user);
            const path =
                user.user_type === UserType.MERCHANT
                    ? "/merchants"
                    : "/customers";
            navigate(path);
            toast.success("Login successful");
        },
        onError: (error) => {
            if (error instanceof AxiosError) {
                toast.error(error.response?.data.detail);
            } else {
                toast.error(error.message);
            }
        },
    });

    function onSubmit(data: SignInFormSchema) {
        mutate(data);
    }

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className={cn("grid gap-3", className)}
                {...props}
            >
                <FormField
                    control={form.control}
                    name="login"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="name@example.com"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem className="relative">
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <PasswordInput
                                    placeholder="********"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button className="mt-2" disabled={isPending}>
                    Sign In
                </Button>
            </form>
        </Form>
    );
}
