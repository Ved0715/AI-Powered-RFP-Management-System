import Link from "next/link";

export interface StatCardProps {
  title: string;
  value: number;
  icon: React.ElementType;
  trend?: string;
}

export function StatCard({ title, value, icon: Icon, trend }: StatCardProps) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="p-3 bg-blue-50 rounded-lg">
          <Icon className="h-6 w-6 text-blue-600" />
        </div>
        {trend && <span className="text-sm text-green-600">{trend}</span>}
      </div>
      <h3 className="text-slate-600 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-slate-900 mt-1">{value}</p>
    </div>
  );
}

export interface RecentListProps {
  title: string;
  items: any[];
  linkHref: string;
}

export function RecentList({ title, items, linkHref }: RecentListProps) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-slate-900">{title}</h2>
        <Link href={linkHref} className="text-blue-600 text-sm hover:underline">
          View All
        </Link>
      </div>
      <div className="space-y-3">
        {items.length === 0 ? (
          <p className="text-slate-500 text-sm">No items yet</p>
        ) : (
          items.map((item: any) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-3 hover:bg-slate-50 rounded-lg transition"
            >
              <div>
                <p className="font-medium text-slate-900">{item.title}</p>
                <p className="text-sm text-slate-500">{item.date}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}