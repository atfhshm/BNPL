import { AuthAPI } from "~/lib/api";
import type { DashboardData } from "../components";
import { UserType } from "~/types/auth";

/**
 * Fetch dashboard analytics for the current user type.
 * - CUSTOMER: /api/v1/customers/installments/analytics/
 * - MERCHANT: /api/v1/merchants/installments/analytics/
 */
export async function getDashboardAnalytics(
    userType: UserType
): Promise<DashboardData> {
    let url = "/api/v1/installments/analytics/";
    if (userType === UserType.CUSTOMER) {
        url = "/api/v1/customers/installments/analytics/";
    } else if (userType === UserType.MERCHANT) {
        url = "/api/v1/merchants/installments/analytics/";
    }
    const { data } = await AuthAPI.get(url);
    return data;
}
