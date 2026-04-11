import { cn } from "@/lib/utils";

interface SectionLabelProps {
  children: React.ReactNode;
  className?: string;
}

export function SectionLabel({ children, className }: SectionLabelProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-3 py-1 text-xs font-semibold uppercase tracking-wider text-primary bg-primary-light rounded-full",
        className
      )}
    >
      {children}
    </span>
  );
}
