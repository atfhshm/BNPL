import type { To } from "react-router";
import type { ElementType } from "react";

interface BaseNavItem {
    title: string;
    badge?: string;
    icon?: ElementType;
}

type NavLink = BaseNavItem & {
    url: To;
    items?: never;
};

type NavCollapsible = BaseNavItem & {
    items: (BaseNavItem & { url: To })[];
    url?: never;
};

type NavItem = NavCollapsible | NavLink;

interface NavGroup {
    title: string;
    items: NavItem[];
}

interface SidebarData {
    navGroups: NavGroup[];
}

export type { SidebarData, NavGroup, NavItem, NavCollapsible, NavLink };
