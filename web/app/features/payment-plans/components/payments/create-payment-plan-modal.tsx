import React from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "~/components/ui/dialog";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { useInfiniteQuery } from "@tanstack/react-query";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "~/components/ui/select";
import type { IUser } from "~/types/auth";
import type { IPaginationResponse } from "~/types/pagination";
import { AuthAPI } from "~/lib/api";
import { useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { handleValidationErrors } from "~/lib/utils";

interface CreatePaymentPlanModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onCreate: (data: {
        customerId: number;
        name: string;
        amount: string;
        no_of_installments: number;
        start_date: string;
    }) => void;
    isLoading?: boolean;
}

export function CreatePaymentPlanModal({
    open,
    onOpenChange,
    onCreate,
    isLoading,
}: CreatePaymentPlanModalProps) {
    const [customerId, setCustomerId] = React.useState<number | null>(null);
    const [name, setName] = React.useState("");
    const [amount, setAmount] = React.useState("");
    const [noOfInstallments, setNoOfInstallments] = React.useState("");
    const [startDate, setStartDate] = React.useState("");
    const [error, setError] = React.useState<string | null>(null);

    // Infinite query for customers
    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        isLoading: isCustomersLoading,
    } = useInfiniteQuery<IPaginationResponse<IUser>>({
        queryKey: ["customers"],
        queryFn: async ({ pageParam = 1 }) => {
            const { data } = await AuthAPI.get(
                `/api/v1/customers/?page_number=${pageParam}&page_size=100`
            );
            return data;
        },
        getNextPageParam: (lastPage) => {
            if (lastPage.page_number < lastPage.total_pages) {
                return lastPage.page_number + 1;
            }
            return undefined;
        },
        initialPageParam: 1,
    });

    const customers = data?.pages.flatMap((page) => page.results) ?? [];

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setError(null);
        if (customerId && name && amount && noOfInstallments && startDate) {
            onCreate({
                customerId,
                name,
                amount,
                no_of_installments: Number(noOfInstallments),
                start_date: startDate,
            });
        }
    }

    // Error handling for mutation (to be used in parent)
    // Example usage in parent:
    // const createMutation = useMutation({
    //   mutationFn: createPaymentPlan,
    //   onError: (error) => handleCreateError(error),
    // });
    function handleCreateError(error: unknown) {
        if (error instanceof AxiosError) {
            if (error.response?.status === 400) {
                handleValidationErrors(error.response.data);
            } else {
                toast.error(error.response?.data.detail || "An error occurred");
            }
        } else {
            toast.error((error as Error).message);
        }
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Create Payment Plan</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block mb-1">Customer</label>
                        <Select
                            value={customerId?.toString() ?? ""}
                            onValueChange={(v) => setCustomerId(Number(v))}
                        >
                            <SelectTrigger>
                                <SelectValue
                                    placeholder={
                                        isCustomersLoading
                                            ? "Loading..."
                                            : "Select customer"
                                    }
                                />
                            </SelectTrigger>
                            <SelectContent
                                onScroll={(e) => {
                                    const el = e.currentTarget;
                                    if (
                                        el.scrollTop + el.clientHeight >=
                                            el.scrollHeight - 10 &&
                                        hasNextPage &&
                                        !isFetchingNextPage
                                    ) {
                                        fetchNextPage();
                                    }
                                }}
                            >
                                {customers.map((c) => (
                                    <SelectItem
                                        key={c.id}
                                        value={c.id.toString()}
                                    >
                                        {c.first_name} {c.last_name} ({c.email})
                                    </SelectItem>
                                ))}
                                {isFetchingNextPage && (
                                    <div className="p-2 text-center text-xs">
                                        Loading more...
                                    </div>
                                )}
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label className="block mb-1">Name</label>
                        <Input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label className="block mb-1">Amount</label>
                        <Input
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            required
                            type="number"
                            min="0"
                            step="0.01"
                        />
                    </div>
                    <div>
                        <label className="block mb-1">
                            Number of Installments
                        </label>
                        <Input
                            value={noOfInstallments}
                            onChange={(e) =>
                                setNoOfInstallments(e.target.value)
                            }
                            required
                            type="number"
                            min="1"
                            step="1"
                        />
                    </div>
                    <div>
                        <label className="block mb-1">Start Date</label>
                        <Input
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            required
                            type="date"
                        />
                    </div>
                    {error && (
                        <div className="text-destructive text-sm">{error}</div>
                    )}
                    <div className="flex justify-end gap-2">
                        <Button
                            type="button"
                            variant="secondary"
                            onClick={() => onOpenChange(false)}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            disabled={
                                isLoading ||
                                !customerId ||
                                !name ||
                                !amount ||
                                !noOfInstallments ||
                                !startDate
                            }
                        >
                            {isLoading ? "Creating..." : "Create"}
                        </Button>
                    </div>
                </form>
            </DialogContent>
        </Dialog>
    );
}
