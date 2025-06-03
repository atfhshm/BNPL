import { Avatar, AvatarFallback } from "~/components/ui/avatar";

interface Customer {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
}

interface PaymentPlan {
    id: number;
    customer: Customer;
    name: string;
}

interface Installment {
    id: number;
    payment_plan: PaymentPlan;
    amount: string;
    amount_currency: string;
    due_date: string;
    status: string;
}

interface UpcomingInstallmentsProps {
    data: Installment[];
}

export function UpcomingInstallments({ data }: UpcomingInstallmentsProps) {
    return (
        <div className="space-y-8">
            {data.map((installment) => {
                const { customer } = installment.payment_plan;
                const initials = `${customer.first_name[0]}${customer.last_name[0]}`;

                return (
                    <div
                        key={installment.id}
                        className="flex items-center gap-4"
                    >
                        <Avatar className="h-9 w-9">
                            <AvatarFallback>{initials}</AvatarFallback>
                        </Avatar>
                        <div className="flex flex-1 flex-wrap items-center justify-between">
                            <div className="space-y-1">
                                <p className="text-sm leading-none font-medium">
                                    {customer.first_name} {customer.last_name}
                                </p>
                                <p className="text-muted-foreground text-sm">
                                    {customer.email}
                                </p>
                            </div>
                            <div className="font-medium">
                                {installment.amount}{" "}
                                {installment.amount_currency}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
