import { Header } from "~/components/layouts/header";
import { Main } from "~/components/layouts/main";
import { Search } from "~/components/search";
import { ThemeSwitch } from "~/components/theme-switcher";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "~/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import StatCards from "./stat-cards";
import { Overview } from "./overview";
import { UpcomingInstallments } from "./upcoming-installments";

export interface DashboardData {
    numerical_analytics: {
        total_number: number;
        total_amount: string;
        paid_number: number;
        paid_amount: string;
        pending_number: number;
        pending_amount: string;
        overdue_number: number;
        overdue_amount: string;
    };
    date_analytics: Array<{
        paid_date: string;
        paid_number: number;
        paid_amount: number;
    }>;
    upcoming_installments: Array<{
        id: number;
        payment_plan: {
            id: number;
            customer: {
                id: number;
                first_name: string;
                last_name: string;
                email: string;
            };
            name: string;
        };
        amount: string;
        amount_currency: string;
        due_date: string;
        status: string;
    }>;
}

interface DashboardProps {
    data: DashboardData;
}

export default function Dashboard({ data }: DashboardProps) {
    return (
        <>
            <Header>
                <div className="ml-auto flex items-center space-x-4">
                    <Search />
                    <ThemeSwitch />
                </div>
            </Header>
            {/* ===== Main ===== */}
            <Main>
                <div className="mb-2 flex items-center justify-between space-y-2">
                    <h1 className="text-2xl font-bold tracking-tight">
                        Dashboard
                    </h1>
                </div>
                <Tabs
                    orientation="vertical"
                    defaultValue="overview"
                    className="space-y-4"
                >
                    <div className="w-full overflow-x-auto pb-2">
                        <TabsList>
                            <TabsTrigger value="overview">Overview</TabsTrigger>
                        </TabsList>
                    </div>
                    <TabsContent value="overview" className="space-y-4">
                        <StatCards data={data.numerical_analytics} />
                        <div className="grid grid-cols-1 gap-4 lg:grid-cols-7">
                            <Card className="col-span-1 lg:col-span-4">
                                <CardHeader>
                                    <CardTitle>Overview</CardTitle>
                                </CardHeader>
                                <CardContent className="pl-2">
                                    <Overview data={data.date_analytics} />
                                </CardContent>
                            </Card>
                            <Card className="col-span-1 lg:col-span-3">
                                <CardHeader>
                                    <CardTitle>Upcoming Installments</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <UpcomingInstallments
                                        data={data.upcoming_installments}
                                    />
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>
                </Tabs>
            </Main>
        </>
    );
}
