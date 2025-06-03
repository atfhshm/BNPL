import type { IPaymentPlan } from "./payment-plan";
import type { IPaginationResponse } from "./pagination";

export interface IInstallment {
    id: number;
    payment_plan: IPaymentPlan;
    created_at: string;
    updated_at: string;
    amount_currency: string;
    amount: string;
    due_date: string;
    paid_date: string | null;
    status: string;
}

export interface IPaginatedInstallmentResponse
    extends IPaginationResponse<IInstallment> {}
