import { Button } from "~/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "~/components/ui/form";
import { Input } from "~/components/ui/input";
import { PasswordInput } from "~/components/password-input";
import { cn, handleValidationErrors } from "~/lib/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { type HTMLAttributes } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";
import { toast } from "sonner";
import { signUpSchema, type SignUpFormSchema } from "../../schemas";
import { useMutation } from "@tanstack/react-query";
import {
    getCurrentUserRequest,
    signUpCustomerRequest,
    signUpMerchantRequest,
} from "../../services";
import { AxiosError } from "axios";
import { PhoneInput } from "~/components/phone-input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import { UserType } from "~/types/auth";

type SignUpFormProps = HTMLAttributes<HTMLFormElement>;

import { useUserStore } from "~/stores/user-store";
import { setTokens } from "~/lib/api";

export function SignUpForm({ className, ...props }: SignUpFormProps) {
    const navigate = useNavigate();
    const { setUser } = useUserStore();
    const form = useForm<SignUpFormSchema>({
        resolver: zodResolver(signUpSchema),
        defaultValues: {
            first_name: "",
            last_name: "",
            email: "",
            phone_number: "",
            password: "",
            confirm_password: "",
        },
    });

    const { mutate: mutateCustomer, isPending: isCustomerPending } =
        useMutation({
            mutationFn: signUpCustomerRequest,
            mutationKey: ["sign-up-customer"],
            onSuccess: async (data) => {
                navigate("/");
                setTokens(data.data);
                const { data: user } = await getCurrentUserRequest();
                setUser(user);
                navigate("/");
                toast.success("Customer account created successfully");
            },
            onError: handleError,
        });

    const { mutate: mutateMerchant, isPending: isMerchantPending } =
        useMutation({
            mutationFn: signUpMerchantRequest,
            mutationKey: ["sign-up-merchant"],
            onSuccess: async (data) => {
                navigate("/");
                setTokens(data.data);
                const { data: user } = await getCurrentUserRequest();
                setUser(user);
                navigate("/");
                toast.success("Merchant account created successfully");
            },
            onError: handleError,
        });

    function handleError(error: unknown) {
        if (error instanceof AxiosError) {
            if (error.response?.status === 400) {
                handleValidationErrors(error.response.data);
            } else {
                toast.error(error.response?.data.detail || "An error occurred");
            }
        } else {
            toast.error((error as Error).message);
        }
    }

    function onSubmit(data: SignUpFormSchema, userType: UserType) {
        if (userType === UserType.CUSTOMER) {
            mutateCustomer(data);
        } else {
            mutateMerchant(data);
        }
    }

    return (
        <Tabs defaultValue={UserType.CUSTOMER} className="w-full">
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value={UserType.CUSTOMER}>Customer</TabsTrigger>
                <TabsTrigger value={UserType.ADMIN}>Merchant</TabsTrigger>
            </TabsList>
            <TabsContent value={UserType.CUSTOMER}>
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit((data) =>
                            onSubmit(data, UserType.CUSTOMER)
                        )}
                        className={cn("grid gap-3", className)}
                        {...props}
                    >
                        <FormFields form={form} />
                        <Button className="mt-2" disabled={isCustomerPending}>
                            Sign Up as Customer
                        </Button>
                    </form>
                </Form>
            </TabsContent>
            <TabsContent value={UserType.ADMIN}>
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit((data) =>
                            onSubmit(data, UserType.ADMIN)
                        )}
                        className={cn("grid gap-3", className)}
                        {...props}
                    >
                        <FormFields form={form} />
                        <Button className="mt-2" disabled={isMerchantPending}>
                            Sign Up as Merchant
                        </Button>
                    </form>
                </Form>
            </TabsContent>
        </Tabs>
    );
}

// Separate component for form fields to avoid duplication
function FormFields({ form }: { form: any }) {
    return (
        <>
            <div className="grid grid-cols-2 gap-3">
                <FormField
                    control={form.control}
                    name="first_name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                                <Input placeholder="John" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="last_name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                                <Input placeholder="Doe" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </div>
            <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input
                                type="email"
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
                name="phone_number"
                render={({ field }) => (
                    <FormItem className="flex flex-col items-start">
                        <FormLabel className="text-left">
                            Phone Number
                        </FormLabel>
                        <FormControl className="w-full">
                            <PhoneInput
                                defaultCountry="SA"
                                placeholder="Enter a phone number"
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
                    <FormItem>
                        <FormLabel>Password</FormLabel>
                        <FormControl>
                            <PasswordInput placeholder="********" {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
            <FormField
                control={form.control}
                name="confirm_password"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>Confirm Password</FormLabel>
                        <FormControl>
                            <PasswordInput placeholder="********" {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
        </>
    );
}
