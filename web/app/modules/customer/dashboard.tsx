import { useQuery } from "@tanstack/react-query";
import Dashboard from "~/features/dashboard/components";
import { getCustomerAnalytics } from "~/features/dashboard/services/customer";
import type { DashboardData } from "~/features/dashboard/components";

export default function CustomerDashboard() {
    const { data, isLoading } = useQuery({
        queryKey: ["customer-dashboard"],
        queryFn: getCustomerAnalytics,
    });

    if (isLoading) return <div>Loading...</div>;
    if (!data?.data) return null;

    return <Dashboard data={data.data} />;
}
