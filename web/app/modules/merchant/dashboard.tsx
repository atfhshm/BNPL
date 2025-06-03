import { useQuery } from "@tanstack/react-query";
import Dashboard from "~/features/dashboard/components";
import { getMerchantAnalytics } from "~/features/dashboard/services/merchant";

export default function MerchantDashboard() {
    const { data, isLoading } = useQuery({
        queryKey: ["merchant-dashboard"],
        queryFn: getMerchantAnalytics,
    });

    if (isLoading) return <div>Loading...</div>;
    if (!data?.data) return null;

    return <Dashboard data={data.data} />;
}
