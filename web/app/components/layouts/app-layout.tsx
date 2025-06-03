import Cookies from "js-cookie";
import { Outlet } from "react-router";
import { AppSidebar } from "~/components/layouts/app-sidebar";
import SkipToMain from "~/components/skip-to-main";
import { SidebarProvider } from "~/components/ui/sidebar";
import { SearchProvider } from "~/hooks/use-search";
import { cn } from "~/lib/utils";

export default function AppLayout() {
    const defaultOpen = Cookies.get("sidebar_state") !== "false";

    return (
        <SidebarProvider defaultOpen={defaultOpen}>
            <SearchProvider>
                <SkipToMain />
                <AppSidebar />
                <div
                    id="content"
                    className={cn(
                        "ml-auto w-full max-w-full",
                        "peer-data-[state=collapsed]:w-[calc(100%-var(--sidebar-width-icon)-1rem)]",
                        "peer-data-[state=expanded]:w-[calc(100%-var(--sidebar-width))]",
                        "sm:transition-[width] sm:duration-200 sm:ease-linear",
                        "flex h-svh flex-col",
                        "group-data-[scroll-locked=1]/body:h-full",
                        "has-[main.fixed-main]:group-data-[scroll-locked=1]/body:h-svh"
                    )}
                >
                    <Outlet />
                </div>
            </SearchProvider>
        </SidebarProvider>
    );
}
