import { createColumnHelper } from "@tanstack/react-table";
import type { IPaymentPlan } from "~/types/payment-plan";

const columnHelper = createColumnHelper<IPaymentPlan>();

export const paymentPlanColumns = [
    columnHelper.accessor("id", {
        header: "ID",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("name", {
        header: "Name",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("status", {
        header: "Status",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor(
        (row) => `${row.customer.first_name} ${row.customer.last_name}`,
        {
            id: "customer",
            header: "Customer",
            cell: (info) => info.getValue(),
        }
    ),
    columnHelper.accessor(
        (row) => `${row.merchant.first_name} ${row.merchant.last_name}`,
        {
            id: "merchant",
            header: "Merchant",
            cell: (info) => info.getValue(),
        }
    ),
    columnHelper.accessor("total_amount", {
        header: "Total Amount",
        cell: (info) =>
            `${info.getValue()} ${info.row.original.total_amount_currency}`,
    }),
    columnHelper.accessor("total_collected_amount", {
        header: "Collected Amount",
        cell: (info) =>
            `${info.getValue()} ${
                info.row.original.total_collected_amount_currency
            }`,
    }),
    columnHelper.accessor("no_of_installments", {
        header: "# Installments",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("no_of_paid_installments", {
        header: "# Paid",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("start_date", {
        header: "Start Date",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor("created_at", {
        header: "Created",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor("updated_at", {
        header: "Updated",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.display({
        id: "actions",
        header: "Actions",
        cell: () => null, // Will be replaced in the table with action buttons
    }),
];
