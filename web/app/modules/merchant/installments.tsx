import { Header } from "~/components/layouts/header";
import { Main } from "~/components/layouts/main";
import { Search } from "~/components/search";
import { ThemeSwitch } from "~/components/theme-switcher";
import React from "react";
import { useQuery } from "@tanstack/react-query";
import InstallmentDataTable from "~/features/installments/components/installment-data-table";
import { getMerchantInstallments } from "~/features/installments/services/merchant";

export default function MerchantInstallments() {
    const [page, setPage] = React.useState(1);
    const { data, isLoading } = useQuery({
        queryKey: ["merchant-installments", page],
        queryFn: () => getMerchantInstallments(page, 10),
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
                        Installments
                    </h1>
                </div>
                {isLoading && <div>Loading...</div>}
                {!isLoading && data && (
                    <InstallmentDataTable
                        data={data.results}
                        page={page}
                        pageCount={data.total_pages}
                        onPageChange={setPage}
                        isCustomer={false}
                        onPay={() => {}}
                    />
                )}
            </Main>
        </>
    );
}
