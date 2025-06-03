import React from "react";
import {
    useQuery,
    useMutation,
    useQueryClient,
    keepPreviousData,
} from "@tanstack/react-query";
import PaymentDataTable from "~/features/payment-plans/components/payments/payment-data-table";
import {
    getMerchantPaymentPlans,
    deletePaymentPlan,
    createPaymentPlan,
} from "~/features/payment-plans/services/merchant";
import { CreatePaymentPlanModal } from "~/features/payment-plans/components/payments/create-payment-plan-modal";
import { DeletePaymentPlanModal } from "~/features/payment-plans/components/payments/delete-payment-plan-modal";
import { useUserStore } from "~/stores/user-store";
import type { IPaginatedPaymentPlanResponse } from "~/types/payment-plan";
import Loader from "~/components/ui/loader";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { handleValidationErrors } from "~/lib/utils";
import { Header } from "~/components/layouts/header";
import { Main } from "~/components/layouts/main";
import { Search } from "~/components/search";
import { ThemeSwitch } from "~/components/theme-switcher";

export default function MerchantPaymentPlans() {
    const [page, setPage] = React.useState(1);
    const [createOpen, setCreateOpen] = React.useState(false);
    const [deleteOpen, setDeleteOpen] = React.useState(false);
    const [selectedPlan, setSelectedPlan] = React.useState<any>(null);
    const queryClient = useQueryClient();
    const { user } = useUserStore();

    const { data, isPending } = useQuery<IPaginatedPaymentPlanResponse>({
        queryKey: ["merchant-payment-plans", page],
        queryFn: () => getMerchantPaymentPlans(page, 10),
        placeholderData: keepPreviousData,
        enabled: !!user && user.user_type === "merchant",
    });

    const createMutation = useMutation({
        mutationFn: createPaymentPlan,
        onSuccess: () => {
            setCreateOpen(false);
            queryClient.invalidateQueries({
                queryKey: ["merchant-payment-plans"],
            });
        },
    });

    const deleteMutation = useMutation({
        mutationFn: (id: number) => deletePaymentPlan(id),
        onSuccess: () => {
            setDeleteOpen(false);
            setSelectedPlan(null);
            queryClient.invalidateQueries({
                queryKey: ["merchant-payment-plans"],
            });
        },
        onError: (error) => {
            if (error instanceof AxiosError && error.response?.status === 400) {
                handleValidationErrors(error.response.data);
            } else if (error instanceof AxiosError) {
                toast.error(error.response?.data.detail || "An error occurred");
            } else {
                toast.error((error as Error).message);
            }
        },
    });

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
                        Payment Plans
                    </h1>
                </div>
                {isPending && <Loader />}
                {!isPending && data && (
                    <>
                        <PaymentDataTable
                            data={data.results}
                            page={page}
                            pageSize={10}
                            pageCount={data.total_pages}
                            onPageChange={setPage}
                            isMerchant={user?.user_type === "merchant"}
                            onDelete={(plan) => {
                                setSelectedPlan(plan);
                                setDeleteOpen(true);
                            }}
                            onCreate={() => setCreateOpen(true)}
                        />
                        <CreatePaymentPlanModal
                            open={createOpen}
                            onOpenChange={setCreateOpen}
                            onCreate={(input) => createMutation.mutate(input)}
                            isLoading={createMutation.isPending}
                        />
                        <DeletePaymentPlanModal
                            open={deleteOpen}
                            onOpenChange={setDeleteOpen}
                            onDelete={() =>
                                selectedPlan &&
                                deleteMutation.mutate(selectedPlan.id)
                            }
                            isLoading={deleteMutation.isPending}
                            planName={selectedPlan?.name}
                        />
                    </>
                )}
            </Main>
        </>
    );
}
