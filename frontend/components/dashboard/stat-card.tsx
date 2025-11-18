interface StatCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'accent' | 'default';
}

export function StatCard({ title, value, icon, color }: StatCardProps) {
  const colorClasses = {
    primary: 'bg-primary/10 text-primary border-primary/20',
    secondary: 'bg-secondary/10 text-secondary border-secondary/20',
    accent: 'bg-accent/10 text-accent border-accent/20',
    default: 'bg-gray-100 text-gray-600 border-gray-200',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground font-medium mb-1">
            {title}
          </p>
          <p className="text-3xl font-bold">{value}</p>
        </div>
        <div
          className={`p-4 rounded-full border-2 ${colorClasses[color]}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}
