import React from "react";
import {
    AlertDialog,
    AlertDialogContent,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogFooter,
    AlertDialogCancel,
    AlertDialogAction,
} from "~/components/ui/alert-dialog";

interface DeletePaymentPlanModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onDelete: () => void;
    isLoading?: boolean;
    planName?: string;
}

export function DeletePaymentPlanModal({
    open,
    onOpenChange,
    onDelete,
    isLoading,
    planName,
}: DeletePaymentPlanModalProps) {
    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Delete Payment Plan</AlertDialogTitle>
                </AlertDialogHeader>
                <div>
                    Are you sure you want to delete the payment plan{" "}
                    <b>{planName}</b>? This action cannot be undone.
                </div>
                <AlertDialogFooter>
                    <AlertDialogCancel disabled={isLoading}>
                        Cancel
                    </AlertDialogCancel>
                    <AlertDialogAction
                        onClick={onDelete}
                        disabled={isLoading}
                        className="bg-destructive text-destructive-foreground"
                    >
                        {isLoading ? "Deleting..." : "Delete"}
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
}
