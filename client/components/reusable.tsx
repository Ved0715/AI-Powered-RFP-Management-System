import Link from "next/link";

export interface StatCardProps {
  title: string;
  value: number;
  icon: React.ElementType;
  trend?: string;
}

export function StatCard({ title, value, icon: Icon }: StatCardProps) {
  return (
    <div className="group bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
      <div className="flex items-center justify-between">
        <div className="p-4 bg-blue-50 rounded-xl group-hover:bg-blue-600 transition-colors duration-300">
          <Icon className="h-8 w-8 text-blue-600 group-hover:text-white transition-colors duration-300" />
        </div>
        <div className="text-right">
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
        </div>
      </div>
      <div>
        {/* if i need i will add description */}
      </div>
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