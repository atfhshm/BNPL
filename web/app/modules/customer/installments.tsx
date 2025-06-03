import { Header } from "~/components/layouts/header";
import { Main } from "~/components/layouts/main";
import { Search } from "~/components/search";
import { ThemeSwitch } from "~/components/theme-switcher";
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import InstallmentDataTable from "~/features/installments/components/installment-data-table";
import {
    getCustomerInstallments,
    payInstallment,
} from "~/features/installments/services/customer";
import { toast } from "sonner";

export default function CustomerInstallments() {
    const [page, setPage] = React.useState(1);
    const [payingId, setPayingId] = React.useState<number | null>(null);
    const queryClient = useQueryClient();
    const { data, isLoading } = useQuery({
        queryKey: ["customer-installments", page],
        queryFn: () => getCustomerInstallments(page, 10),
        placeholderData: (prev) => prev,
    });

    const payMutation = useMutation({
        mutationFn: (id: number) => payInstallment(id),
        onMutate: (id: number) => setPayingId(id),
        onSettled: () => setPayingId(null),
        onSuccess: () => {
            toast.success("Installment paid successfully");
            queryClient.invalidateQueries({
                queryKey: ["customer-installments"],
            });
        },
        onError: (error: any) => {
            toast.error(
                error?.response?.data?.detail || "Failed to pay installment"
            );
        },
    });

    function handlePay(installment: any) {
        payMutation.mutate(installment.id);
    }

    return (
        <>
            <Header>
                <div className="ml-auto flex items-center space-x-4">
                    <Search />
                    <ThemeSwitch />
                </div>
            </Header>
            <Main>
                <div className="mb-2 flex items-center justify-between space-y-2">
                    <h1 className="text-2xl font-bold tracking-tight">
                        Installments
                    </h1>
                </div>
                {isLoading && <div>Loading...</div>}
                {!isLoading && data && (
                    <InstallmentDataTable
                        key={page}
                        data={data.results}
                        page={page}
                        pageCount={data.total_pages}
                        onPageChange={setPage}
                        isCustomer={true}
                        onPay={handlePay}
                        payingId={payingId}
                    />
                )}
            </Main>
        </>
    );
}
