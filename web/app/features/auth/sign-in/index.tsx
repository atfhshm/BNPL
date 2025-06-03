import AuthLayout from "~/components/layouts/auth-layout";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "~/components/ui/card";
import { SignInForm } from "./components/sign-in-form";
import { Link } from "react-router";

export default function SignIn() {
    return (
        <AuthLayout>
            <Card className="gap-4">
                <CardHeader>
                    <CardTitle className="text-lg tracking-tight">
                        Sign In
                    </CardTitle>
                    <CardDescription>
                        Enter your credentials below to sign in <br />
                        Do not have an account?{" "}
                        <Link
                            to="/sign-up"
                            className="hover:text-primary underline underline-offset-4"
                        >
                            Sign Up
                        </Link>
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <SignInForm />
                </CardContent>
            </Card>
        </AuthLayout>
    );
}
