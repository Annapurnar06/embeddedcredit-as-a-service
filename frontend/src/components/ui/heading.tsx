import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface HeadingProps {
  children: ReactNode;
  className?: string;
  as?: "h1" | "h2" | "h3" | "h4";
  size?: "xl" | "2xl" | "3xl" | "4xl" | "5xl";
}

const sizeStyles = {
  xl: "text-xl lg:text-2xl",
  "2xl": "text-2xl lg:text-3xl",
  "3xl": "text-3xl lg:text-4xl",
  "4xl": "text-4xl lg:text-5xl",
  "5xl": "text-5xl lg:text-6xl",
};

export function Heading({
  children,
  className,
  as: Tag = "h2",
  size = "3xl",
}: HeadingProps) {
  return (
    <Tag
      className={cn(
        "font-bold tracking-tight text-foreground",
        sizeStyles[size],
        className
      )}
    >
      {children}
    </Tag>
  );
}
