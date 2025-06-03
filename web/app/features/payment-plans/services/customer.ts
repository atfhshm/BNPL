import { AuthAPI } from "~/lib/api";
import type { IPaginatedPaymentPlanResponse } from "~/types/payment-plan";

export async function getCustomerPaymentPlans(
    page = 1,
    pageSize = 10
): Promise<IPaginatedPaymentPlanResponse> {
    const { data } = await AuthAPI.get(
        `/api/v1/customers/payment-plans/?page=${page}&page_size=${pageSize}`
    );
    return data;
}
