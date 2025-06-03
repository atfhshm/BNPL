import {
    type RouteConfig,
    index,
    layout,
    prefix,
    route,
} from "@react-router/dev/routes";

export default [
    route("/sign-in", "features/auth/sign-in/index.tsx"),
    route("/sign-up", "features/auth/sign-up/index.tsx"),
    layout("./components/layouts/app-layout.tsx", [
        ...prefix("merchants", [
            index("modules/merchant/dashboard.tsx"),
            route("/payment-plans", "modules/merchant/payment-plans.tsx"),
            route("/installments", "modules/merchant/installments.tsx"),
        ]),
        ...prefix("customers", [
            index("modules/customer/dashboard.tsx"),
            route("/payment-plans", "modules/customer/payment-plans.tsx"),
            route("/installments", "modules/customer/installments.tsx"),
        ]),
    ]),
] satisfies RouteConfig;
