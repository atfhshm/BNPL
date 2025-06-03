import type { IUser } from "./auth";
import type { IPaginationResponse } from "./pagination";

export interface IPaymentPlan {
    id: number;
    customer: IUser;
    merchant: IUser;
    no_of_paid_installments: number;
    created_at: string;
    updated_at: string;
    name: string;
    status: string;
    no_of_installments: number;
    total_amount_currency: string;
    total_amount: string;
    total_collected_amount_currency: string;
    total_collected_amount: string;
    start_date: string;
}

export interface IPaginatedPaymentPlanResponse
    extends IPaginationResponse<IPaymentPlan> {}
