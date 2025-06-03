import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Wallet, Users, Clock, AlertCircle } from "lucide-react";

interface NumericalAnalytics {
    total_number: number;
    total_amount: string;
    paid_number: number;
    paid_amount: string;
    pending_number: number;
    pending_amount: string;
    overdue_number: number;
    overdue_amount: string;
}

interface StatCardsProps {
    data: NumericalAnalytics;
}

export default function StatCards({ data }: StatCardsProps) {
    return (
        <div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Total Amount
                        </CardTitle>
                        <Wallet className="text-muted-foreground h-4 w-4" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {data.total_amount} SAR
                        </div>
                        <p className="text-muted-foreground text-xs">
                            {data.total_number} total installments
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Paid Amount
                        </CardTitle>
                        <Users className="text-muted-foreground h-4 w-4" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {data.paid_amount} SAR
                        </div>
                        <p className="text-muted-foreground text-xs">
                            {data.paid_number} paid installments
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Pending Amount
                        </CardTitle>
                        <Clock className="text-muted-foreground h-4 w-4" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {data.pending_amount} SAR
                        </div>
                        <p className="text-muted-foreground text-xs">
                            {data.pending_number} pending installments
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Overdue Amount
                        </CardTitle>
                        <AlertCircle className="text-muted-foreground h-4 w-4" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {data.overdue_amount} SAR
                        </div>
                        <p className="text-muted-foreground text-xs">
                            {data.overdue_number} overdue installments
                        </p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
