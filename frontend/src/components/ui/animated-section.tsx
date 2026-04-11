"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface AnimatedSectionProps {
  children: ReactNode;
  className?: string;
  id?: string;
  delay?: number;
  direction?: "up" | "left" | "right" | "none";
}

const directionVariants = {
  up: { hidden: { opacity: 0, y: 30 }, visible: { opacity: 1, y: 0 } },
  left: { hidden: { opacity: 0, x: -30 }, visible: { opacity: 1, x: 0 } },
  right: { hidden: { opacity: 0, x: 30 }, visible: { opacity: 1, x: 0 } },
  none: { hidden: { opacity: 0 }, visible: { opacity: 1 } },
};

export function AnimatedSection({
  children,
  className,
  id,
  delay = 0,
  direction = "up",
}: AnimatedSectionProps) {
  return (
    <motion.div
      id={id}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
      variants={directionVariants[direction]}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}
