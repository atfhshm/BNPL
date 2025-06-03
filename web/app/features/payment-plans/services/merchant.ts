import { AuthAPI } from "~/lib/api";
import type { IPaginatedPaymentPlanResponse } from "~/types/payment-plan";

export async function getMerchantPaymentPlans(
    page = 1,
    pageSize = 10
): Promise<IPaginatedPaymentPlanResponse> {
    const { data } = await AuthAPI.get(
        `/api/v1/merchants/payment-plans/?page=${page}&page_size=${pageSize}`
    );
    return data;
}

export async function deletePaymentPlan(id: number) {
    return AuthAPI.delete(`/api/v1/merchants/payment-plans/${id}/`);
}

export async function createPaymentPlan({
    customerId,
    name,
    amount,
    no_of_installments,
    start_date,
}: {
    customerId: number;
    name: string;
    amount: string;
    no_of_installments: number;
    start_date: string;
}) {
    return AuthAPI.post(`/api/v1/merchants/payment-plans/`, {
        customer: customerId,
        name,
        total_amount: amount,
        no_of_installments,
        start_date,
    });
}
