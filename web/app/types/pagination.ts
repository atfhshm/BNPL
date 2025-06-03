export interface IPaginationResponse<T> {
    count: number;
    page_size: number;
    page_number: number;
    total_pages: number;
    next: string | null;
    previous: string | null;
    results: T[];
}
