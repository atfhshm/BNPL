import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";

interface DateAnalytics {
    paid_date: string;
    paid_number: number;
    paid_amount: number;
}

interface OverviewProps {
    data: DateAnalytics[];
}

export function Overview({ data }: OverviewProps) {
    const chartData = data.map((item) => ({
        name: new Date(item.paid_date).toLocaleDateString("en-US", {
            month: "short",
            year: "numeric",
        }),
        total: item.paid_amount,
    }));

    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData}>
                <XAxis
                    dataKey="name"
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <YAxis
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `$${value}`}
                />
                <Bar
                    dataKey="total"
                    fill="currentColor"
                    radius={[4, 4, 0, 0]}
                    className="fill-primary"
                />
            </BarChart>
        </ResponsiveContainer>
    );
}
