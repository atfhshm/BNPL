import { create } from "zustand";
import { isAuthenticated, removeTokens } from "~/lib/api";
import type { IUser } from "~/types/auth";

interface UserState {
    user: IUser | null;
    setUser: (user: IUser) => void;
    clearUser: () => void;
    isAuthenticated: () => boolean;
    logOut: () => void;
}

export const useUserStore = create<UserState>((set) => ({
    user: null,
    setUser: (user: IUser) => set({ user }),
    clearUser: () => set({ user: null }),
    isAuthenticated: () => {
        return isAuthenticated();
    },
    logOut: () => {
        removeTokens();
        set({ user: null });
    },
}));