import { createColumnHelper } from "@tanstack/react-table";
import type { IInstallment } from "~/types/installment";

const columnHelper = createColumnHelper<IInstallment>();

export const installmentColumns = [
    columnHelper.accessor("id", {
        header: "ID",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor((row) => row.payment_plan.name, {
        id: "payment_plan",
        header: "Plan Name",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("amount", {
        header: "Amount",
        cell: (info) =>
            `${info.getValue()} ${info.row.original.amount_currency}`,
    }),
    columnHelper.accessor("due_date", {
        header: "Due Date",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor("paid_date", {
        header: "Paid Date",
        cell: (info) =>
            info.getValue()
                ? new Date(info.getValue() as string).toLocaleDateString()
                : "-",
    }),
    columnHelper.accessor("status", {
        header: "Status",
        cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("created_at", {
        header: "Created",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor("updated_at", {
        header: "Updated",
        cell: (info) => new Date(info.getValue()).toLocaleDateString(),
    }),
    // Actions column for customer table only (pay)
    columnHelper.display({
        id: "actions",
        header: "Actions",
        cell: () => null, // Will be replaced in the table for customer actions
    }),
];
