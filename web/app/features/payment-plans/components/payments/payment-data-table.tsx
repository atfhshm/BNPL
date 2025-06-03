import React from "react";
import {
    useReactTable,
    getCoreRowModel,
    flexRender,
} from "@tanstack/react-table";
import { paymentPlanColumns } from "./payment-plan-columns";
import type { IPaymentPlan } from "~/types/payment-plan";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    TableCaption,
} from "~/components/ui/table";
import { Button } from "~/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "~/components/ui/card";
import { Badge } from "~/components/ui/badge";

function StatusBadge({ status }: { status: string }) {
    let color = "";
    let label = status;
    switch (status) {
        case "active":
            color = "bg-primary/10 text-primary border-primary";
            label = "Active";
            break;
        case "completed":
            color = "bg-green-100 text-green-800 border-green-300";
            label = "Completed";
            break;
        case "cancelled":
            color = "bg-muted text-muted-foreground border-muted-foreground/30";
            label = "Cancelled";
            break;
        case "overdue":
            color = "bg-destructive/10 text-destructive border-destructive";
            label = "Overdue";
            break;
        default:
            color = "bg-muted text-muted-foreground border-muted-foreground/30";
            label = status;
    }
    return (
        <Badge className={`border ${color} font-medium px-2 py-1 rounded`}>
            {label}
        </Badge>
    );
}

interface PaymentDataTableProps {
    data: IPaymentPlan[];
    page: number;
    pageSize: number;
    pageCount: number;
    onPageChange: (page: number) => void;
    isMerchant: boolean;
    onDelete: (plan: IPaymentPlan) => void;
    onCreate: () => void;
}

export default function PaymentDataTable({
    data,
    page,
    pageCount,
    onPageChange,
    isMerchant,
    onDelete,
    onCreate,
}: PaymentDataTableProps) {
    const columns = React.useMemo(() => paymentPlanColumns, []);
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    });

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Payment Plans</CardTitle>
                {isMerchant && (
                    <Button onClick={onCreate} variant="default" size="sm">
                        + New Payment Plan
                    </Button>
                )}
            </CardHeader>
            <CardContent>
                <Table>
                    <TableCaption>A list of all payment plans.</TableCaption>
                    <TableHeader>
                        {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow
                                key={headerGroup.id}
                                className="bg-muted/40"
                            >
                                {headerGroup.headers.map((header) => (
                                    <TableHead
                                        key={header.id}
                                        className="uppercase font-bold text-xs tracking-wider text-muted-foreground py-3 px-2 border-b border-muted"
                                    >
                                        {flexRender(
                                            header.column.columnDef.header,
                                            header.getContext()
                                        )}
                                    </TableHead>
                                ))}
                            </TableRow>
                        ))}
                    </TableHeader>
                    <TableBody>
                        {data.length === 0 ? (
                            <TableRow>
                                <TableCell
                                    colSpan={columns.length}
                                    className="text-center text-muted-foreground"
                                >
                                    No payment plans found.
                                </TableCell>
                            </TableRow>
                        ) : (
                            table.getRowModel().rows.map((row) => (
                                <TableRow
                                    key={row.id}
                                    className="transition-colors hover:bg-accent/40 group"
                                >
                                    {row.getVisibleCells().map((cell) => {
                                        if (cell.column.id === "status") {
                                            return (
                                                <TableCell key={cell.id}>
                                                    <StatusBadge
                                                        status={
                                                            cell.getValue() as string
                                                        }
                                                    />
                                                </TableCell>
                                            );
                                        }
                                        if (
                                            cell.column.id === "actions" &&
                                            isMerchant
                                        ) {
                                            return (
                                                <TableCell key={cell.id}>
                                                    <div className="flex gap-2">
                                                        <Button
                                                            variant="destructive"
                                                            size="sm"
                                                            onClick={() =>
                                                                onDelete(
                                                                    row.original
                                                                )
                                                            }
                                                        >
                                                            Delete
                                                        </Button>
                                                    </div>
                                                </TableCell>
                                            );
                                        }
                                        return (
                                            <TableCell key={cell.id}>
                                                {flexRender(
                                                    cell.column.columnDef.cell,
                                                    cell.getContext()
                                                )}
                                            </TableCell>
                                        );
                                    })}
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
                <div className="flex justify-end gap-2 mt-4">
                    <Button
                        disabled={page <= 1}
                        onClick={() => onPageChange(page - 1)}
                        size="sm"
                        variant="outline"
                    >
                        Previous
                    </Button>
                    <span className="self-center text-sm text-muted-foreground">
                        Page {page} of {pageCount}
                    </span>
                    <Button
                        disabled={page >= pageCount}
                        onClick={() => onPageChange(page + 1)}
                        size="sm"
                        variant="outline"
                    >
                        Next
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
