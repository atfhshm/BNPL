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

export function getSidebarData(userType: "merchant" | "customer"): SidebarData {
    const prefix = userType === "merchant" ? "/merchants" : "/customers";
    return {
        navGroups: [
            {
                title: "General",
                items: [
                    {
                        title: "Dashboard",
                        url: `${prefix}`,
                        icon: IconLayoutDashboard,
                    },
                ],
            },
            {
                title: "Payment Plans",
                items: [
                    {
                        title: "Payment Plans",
                        url: `${prefix}/payment-plans`,
                        icon: IconPackages,
                    },
                ],
            },
            {
                title: "Installments",
                items: [
                    {
                        title: "Installments",
                        url: `${prefix}/installments`,
                        icon: User2,
                    },
                ],
            },
        ],
    };
}
