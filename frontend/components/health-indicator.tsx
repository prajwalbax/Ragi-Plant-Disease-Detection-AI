"use client";

import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";
import { cn } from "@/lib/utils";

export function HealthIndicator() {
  const [online, setOnline] = useState(false);

  useEffect(() => {
    let active = true;

    const poll = async () => {
      const health = await checkHealth();
      if (active) {
        setOnline(health.status === "running");
      }
    };

    void poll();
    const interval = window.setInterval(poll, 6000);

    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  return (
    <div
      className={cn(
        "flex items-center gap-2 rounded-full border px-3 py-2 text-sm backdrop-blur-xl",
        online
          ? "border-primary/30 bg-primary/10 text-primary"
          : "border-red-400/30 bg-red-500/10 text-red-200",
      )}
    >
      <span className={cn("h-2.5 w-2.5 rounded-full", online ? "bg-primary" : "bg-red-400")} />
      {online ? "Backend Running" : "Backend Offline"}
    </div>
  );
}
