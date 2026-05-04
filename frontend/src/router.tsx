import { createRoute, createRouter, createRootRoute, Outlet } from "@tanstack/react-router";
import Dashboard from "./pages/Dashboard.tsx";
import MachineDetail from "./pages/MachineDetail.tsx";

const rootRoute = createRootRoute({
  component: () => <Outlet />,
});

const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: Dashboard
});

const machineRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/machines/$machineId',
    component: MachineDetail
});

const routeTree = rootRoute.addChildren([
    indexRoute,
    machineRoute
]);

export const router = createRouter({ routeTree });

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router
    }
}

