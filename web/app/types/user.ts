import type { IUser } from "./auth";
import type { IPaginationResponse } from "./pagination";

export interface IPaginatedUserResponse extends IPaginationResponse<IUser> {}
