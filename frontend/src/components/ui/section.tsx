import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface SectionProps {
  children: ReactNode;
  className?: string;
  id?: string;
  background?: "white" | "gray" | "dark" | "primary";
}

const bgStyles = {
  white: "bg-white",
  gray: "bg-surface-raised",
  dark: "bg-secondary text-secondary-foreground",
  primary: "bg-primary text-primary-foreground",
};

export function Section({
  children,
  className,
  id,
  background = "white",
}: SectionProps) {
  return (
    <section
      id={id}
      className={cn("py-20 lg:py-28", bgStyles[background], className)}
    >
      {children}
    </section>
  );
}
