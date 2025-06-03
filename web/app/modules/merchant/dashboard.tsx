import { useQuery } from "@tanstack/react-query";
import Dashboard from "~/features/dashboard/components";
import { getDashboardAnalytics } from "~/features/dashboard/services/customer";
import { useUserStore } from "~/stores/user-store";

export default function MerchantDashboard() {
    const { user } = useUserStore();
    const { data, isPending } = useQuery({
        queryKey: ["dashboard", user?.user_type],
        queryFn: () => getDashboardAnalytics(user!.user_type),
        enabled: !!user,
    });

    if (isPending) return <div>Loading...</div>;
    if (!data) return null;

    return <Dashboard data={data} />;
}
