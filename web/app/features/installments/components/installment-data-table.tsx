import React from "react";
import {
    useReactTable,
    getCoreRowModel,
    flexRender,
} from "@tanstack/react-table";
import { installmentColumns } from "./installment-columns";
import type { IInstallment } from "~/types/installment";
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
import { Loader2 } from "lucide-react";

function StatusBadge({ status }: { status: string }) {
    let color = "";
    let label = status;
    switch (status) {
        case "active":
            color = "bg-primary/10 text-primary border-primary";
            label = "Active";
            break;
        case "paid":
            color = "bg-green-100 text-green-800 border-green-300";
            label = "Paid";
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

interface InstallmentDataTableProps {
    data: IInstallment[];
    page: number;
    pageCount: number;
    onPageChange: (page: number) => void;
    isCustomer: boolean;
    onPay: (installment: IInstallment) => void;
    payingId?: number | null;
}

export default function InstallmentDataTable({
    data,
    page,
    pageCount,
    onPageChange,
    isCustomer,
    onPay,
    payingId,
}: InstallmentDataTableProps) {
    const columns = React.useMemo(() => installmentColumns, []);
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    });

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Installments</CardTitle>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableCaption>A list of all installments.</TableCaption>
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
                                    No installments found.
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
                                            isCustomer &&
                                            row.original.status !== "paid"
                                        ) {
                                            return (
                                                <TableCell key={cell.id}>
                                                    <Button
                                                        className="bg-green-600 hover:bg-green-700 text-white font-semibold rounded px-3 py-1 flex items-center gap-2"
                                                        disabled={
                                                            payingId ===
                                                            row.original.id
                                                        }
                                                        onClick={() =>
                                                            onPay(row.original)
                                                        }
                                                    >
                                                        {payingId ===
                                                        row.original.id ? (
                                                            <Loader2 className="animate-spin w-4 h-4" />
                                                        ) : null}
                                                        Pay
                                                    </Button>
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
