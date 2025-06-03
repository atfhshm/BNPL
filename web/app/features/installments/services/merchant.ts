import { AuthAPI } from "~/lib/api";
import type {
    IPaginatedInstallmentResponse,
    IInstallment,
} from "~/types/installment";

export async function getMerchantInstallments(
    page = 1,
    pageSize = 10
): Promise<IPaginatedInstallmentResponse> {
    const { data } = await AuthAPI.get(
        `/api/v1/merchants/installments/?page=${page}&page_size=${pageSize}`
    );
    return data;
}

export async function payInstallment(id: number): Promise<IInstallment> {
    const { data } = await AuthAPI.patch(
        `/api/v1/merchants/installments/${id}/`,
        { status: "paid" }
    );
    return data;
}
