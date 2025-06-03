import React from "react";

export default function Loader() {
    return (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-background/60">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-primary" />
        </div>
    );
}
