import { Header } from "~/components/layouts/header";
import { Main } from "~/components/layouts/main";
import { Search } from "~/components/search";
import { ThemeSwitch } from "~/components/theme-switcher";
import React from "react";
import { useQuery } from "@tanstack/react-query";
import PaymentDataTable from "~/features/payment-plans/components/payments/payment-data-table";
import { getCustomerPaymentPlans } from "~/features/payment-plans/services/customer";
import { useUserStore } from "~/stores/user-store";

export default function CustomerPaymentPlans() {
    const [page, setPage] = React.useState(1);
    const { user } = useUserStore();

    const { data, isLoading } = useQuery({
        queryKey: ["customer-payment-plans", page],
        queryFn: () => getCustomerPaymentPlans(page, 10),
        keepPreviousData: true,
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
                {isLoading && <div>Loading...</div>}
                {!isLoading && data && (
                    <PaymentDataTable
                        data={data.results}
                        page={page}
                        pageCount={data.total_pages}
                        onPageChange={setPage}
                        isMerchant={false}
                        onDelete={() => {}}
                        onCreate={() => {}}
                    />
                )}
            </Main>
        </>
    );
}
