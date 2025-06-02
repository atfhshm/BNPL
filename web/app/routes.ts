import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/root.tsx"),
    route("/sign-in", "modules/auth/sign-in/index.tsx"),
    route("/sign-up", "modules/auth/sign-up/index.tsx"),
] satisfies RouteConfig;
