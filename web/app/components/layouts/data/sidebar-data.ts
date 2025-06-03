import {
    IconHelp,
    IconLayoutDashboard,
    IconPackages,
    IconPalette,
    IconSettings,
    IconUserCog,
} from "@tabler/icons-react";
import { User2 } from "lucide-react";
import type { SidebarData } from "../types";

export const sidebarData: SidebarData = {
    navGroups: [
        {
            title: "General",
            items: [
                {
                    title: "Dashboard",
                    url: "/",
                    icon: IconLayoutDashboard,
                },
            ],
        },
        {
            title: "Payment Plans",
            items: [
                {
                    title: "Payment Plans",
                    url: "/customers/payment-plans",
                    icon: IconPackages,
                },
            ],
        },
        {
            title: "Installments",
            items: [
                {
                    title: "Installments",
                    url: "/customers/installments",
                    icon: User2,
                },
            ],
        },
    ],
};
