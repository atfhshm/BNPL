import type { AxiosResponse } from "axios";
import { AuthAPI } from "~/lib/api";
import type { DashboardData } from "../components";

export async function getMerchantAnalytics(): Promise<
    AxiosResponse<DashboardData>
> {
    return await AuthAPI.get("/api/v1/merchants/installments/analytics/");
}
