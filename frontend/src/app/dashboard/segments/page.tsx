"use client";

import { useState, useMemo } from "react";
import { SEGMENT_CATEGORIES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SegmentDetail } from "@/components/dashboard/segment-detail";
import { Grid3X3, ChevronRight } from "lucide-react";

type CategoryKey = keyof typeof SEGMENT_CATEGORIES;

const CATEGORY_KEYS = Object.keys(SEGMENT_CATEGORIES) as CategoryKey[];

const allSegments = CATEGORY_KEYS.flatMap((cat) =>
  SEGMENT_CATEGORIES[cat].map((seg) => ({ ...seg, category: cat }))
);

export default function SegmentsPage() {
  const [activeCategory, setActiveCategory] = useState<"All" | CategoryKey>(
    "All"
  );
  const [expandedSegment, setExpandedSegment] = useState<string | null>(null);

  const filteredSegments = useMemo(() => {
    if (activeCategory === "All") return allSegments;
    return allSegments.filter((s) => s.category === activeCategory);
  }, [activeCategory]);

  const handleCardClick = (segmentId: string) => {
    setExpandedSegment((prev) => (prev === segmentId ? null : segmentId));
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <Grid3X3 className="h-7 w-7 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">
            Segment Explorer
          </h1>
        </div>
        <p className="text-sm text-muted-foreground">
          38 borrower segments with custom scoring, products, and monitoring
        </p>
      </div>

      {/* Category filter tabs */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => {
            setActiveCategory("All");
            setExpandedSegment(null);
          }}
          className={cn(
            "px-4 py-2 text-sm font-medium rounded-lg transition-colors",
            activeCategory === "All"
              ? "bg-primary text-primary-foreground"
              : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
          )}
        >
          All ({allSegments.length})
        </button>
        {CATEGORY_KEYS.map((cat) => (
          <button
            key={cat}
            onClick={() => {
              setActiveCategory(cat);
              setExpandedSegment(null);
            }}
            className={cn(
              "px-4 py-2 text-sm font-medium rounded-lg transition-colors",
              activeCategory === cat
                ? "bg-primary text-primary-foreground"
                : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
            )}
          >
            {cat} ({SEGMENT_CATEGORIES[cat].length})
          </button>
        ))}
      </div>

      {/* Segment grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filteredSegments.map((seg) => {
          const isExpanded = expandedSegment === seg.id;

          return (
            <div
              key={seg.id}
              className={cn(
                isExpanded &&
                  "col-span-1 sm:col-span-2 lg:col-span-3 xl:col-span-4"
              )}
            >
              <Card
                hover={!isExpanded}
                padding="none"
                className={cn(
                  "cursor-pointer",
                  isExpanded && "border-primary/30"
                )}
              >
                <div
                  className="flex items-center gap-4 p-4"
                  onClick={() => handleCardClick(seg.id)}
                >
                  {/* Icon */}
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-muted text-2xl shrink-0">
                    {seg.icon}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-semibold text-foreground truncate">
                      {seg.name}
                    </h3>
                    <p className="text-xs text-muted-foreground mt-0.5 truncate">
                      {seg.product}
                    </p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <Badge variant="primary" className="text-[10px]">
                        ₹{seg.ticket}
                      </Badge>
                      <Badge variant="outline" className="text-[10px]">
                        {seg.category}
                      </Badge>
                    </div>
                  </div>

                  {/* Chevron */}
                  <ChevronRight
                    className={cn(
                      "h-4 w-4 text-muted-foreground shrink-0 transition-transform",
                      isExpanded && "rotate-90"
                    )}
                  />
                </div>

                {/* Expanded detail */}
                {isExpanded && (
                  <div className="px-4 pb-4">
                    <SegmentDetail
                      segmentId={seg.id}
                      segmentName={seg.name}
                      product={seg.product}
                      ticket={seg.ticket}
                      onClose={() => setExpandedSegment(null)}
                    />
                  </div>
                )}
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );
}
