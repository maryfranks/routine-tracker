import { Link } from "@tanstack/react-router";
import { FlaskConical } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useAction, useClock } from "@/hooks/use-routine";
import { api } from "@/services/api";
import { cn } from "@/lib/utils";

export function AppHeader() {
  const clock = useClock();
  const advance = useAction(api.advanceClock);
  const resetClock = useAction(() => api.resetClock(), "Back to the live clock");
  const demo = useAction(() => api.loadDemoData(), "Demo data loaded");
  const empty = useAction(() => api.resetToEmpty(), "All data cleared");
  const now = clock.data ? new Date(clock.data.now) : null;

  const navCls = "rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground";
  return (
    <header className="border-b bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center gap-4 px-4 py-3">
        <Link to="/" className="font-display text-2xl leading-none">Routine</Link>
        <nav className="flex items-center gap-1">
          <Link to="/" className={navCls} activeOptions={{ exact: true }} activeProps={{ className: "bg-muted text-foreground" }}>Views</Link>
          <Link to="/history" className={navCls} activeProps={{ className: "bg-muted text-foreground" }}>History</Link>
        </nav>
        <div className="ml-auto flex items-center gap-2">
          {now && (
            <span className={cn("hidden rounded-full px-2.5 py-1 text-xs sm:inline", clock.data?.simulated ? "bg-warning text-warning-foreground" : "text-muted-foreground")}>
              {clock.data?.simulated && "Simulated · "}
              {now.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric", year: "numeric" })}
            </span>
          )}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" aria-label="Developer controls"><FlaskConical className="size-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel className="text-xs text-muted-foreground">Simulate time</DropdownMenuLabel>
              <DropdownMenuItem onSelect={() => advance.mutate("day")}>Advance 1 day</DropdownMenuItem>
              <DropdownMenuItem onSelect={() => advance.mutate("week")}>Advance 1 week</DropdownMenuItem>
              <DropdownMenuItem onSelect={() => advance.mutate("month")}>Advance 1 month</DropdownMenuItem>
              <DropdownMenuItem disabled={!clock.data?.simulated} onSelect={() => resetClock.mutate(undefined)}>Reset to live clock</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuLabel className="text-xs text-muted-foreground">Data</DropdownMenuLabel>
              <DropdownMenuItem onSelect={() => demo.mutate(undefined)}>Load demo data</DropdownMenuItem>
              <DropdownMenuItem className="text-destructive" onSelect={() => empty.mutate(undefined)}>Reset to empty</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
