import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { isAuthenticated, removeTokens } from "~/lib/api";
import type { IUser } from "~/types/auth";

interface UserState {
    user: IUser | null;
    setUser: (user: IUser) => void;
    clearUser: () => void;
    isAuthenticated: () => boolean;
    logOut: () => void;
}

export const useUserStore = create<UserState>()(
    persist(
        (set) => ({
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
        }),
        {
            name: "user-storage",
            storage: createJSONStorage(() => localStorage),
            partialize: (state) => ({ user: state.user }), // Only persist the user data
        }
    )
);
