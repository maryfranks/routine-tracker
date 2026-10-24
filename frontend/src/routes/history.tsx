import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { Check, History, Minus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState, ErrorState, ListSkeleton } from "@/components/routine/states";
import { useHistory } from "@/hooks/use-routine";
import { periodLabel } from "@/lib/periods";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/history")({
  head: () => ({
    meta: [
      { title: "History — Routine" },
      { name: "description", content: "Browse past periods and what got done in each." },
      { property: "og:title", content: "History — Routine" },
      { property: "og:description", content: "Browse past periods and what got done in each." },
    ],
  }),
  component: HistoryPage,
});

const PAGE = 10;

function HistoryPage() {
  const history = useHistory();
  const [viewId, setViewId] = useState<string | null>(null);
  const [shown, setShown] = useState(PAGE);

  if (history.isPending) return <ListSkeleton rows={6} />;
  if (history.isError) return <ErrorState error={history.error} onRetry={() => history.refetch()} />;

  if (history.data.length === 0) {
    return (
      <EmptyState icon={<History className="size-8" />} title="Nothing to look back on yet" action={<Button asChild><Link to="/">Create a view</Link></Button>}>
        History fills in as periods end. Create a view and add a few tasks to get started.
      </EmptyState>
    );
  }

  const current = history.data.find((h) => h.view.id === viewId) ?? history.data[0]!;
  const periods = current.periods.slice(0, shown);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-5xl">History</h1>
        <p className="mt-1 text-sm text-muted-foreground">Finished periods only. The current period lives on the Views page.</p>
      </div>
      <div className="flex flex-wrap gap-2" role="tablist">
        {history.data.map((h) => (
          <button
            key={h.view.id}
            role="tab"
            aria-selected={h.view.id === current.view.id}
            onClick={() => { setViewId(h.view.id); setShown(PAGE); }}
            className={cn(
              "rounded-full border px-3 py-1 text-sm transition-colors",
              h.view.id === current.view.id ? "border-primary bg-accent text-accent-foreground" : "hover:bg-muted",
            )}
          >
            {h.view.name}
          </button>
        ))}
      </div>

      {periods.length === 0 ? (
        <EmptyState icon={<History className="size-7" />} title="No finished periods">
          {current.view.name} hasn't completed a full {current.view.cadence.replace("ly", "").replace("dai", "day")} with tasks yet. Try advancing time from the developer menu.
        </EmptyState>
      ) : (
        <ol className="space-y-3">
          {periods.map((p) => {
            const done = p.tasks.filter((t) => t.done).length;
            return (
              <li key={p.key} className="rounded-lg border bg-card p-4">
                <div className="mb-3 flex items-baseline justify-between gap-2">
                  <h2 className="font-medium">{periodLabel(new Date(p.start), current.view.cadence)}</h2>
                  <span className="text-xs text-muted-foreground">{done} completed · {p.tasks.length - done} not completed</span>
                </div>
                <ul className="flex flex-wrap gap-2">
                  {p.tasks.map((t) => (
                    <li
                      key={t.id}
                      className={cn(
                        "inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs",
                        t.done ? "bg-accent text-accent-foreground" : "bg-muted text-muted-foreground",
                      )}
                    >
                      {t.done ? <Check className="size-3" /> : <Minus className="size-3" />}
                      {t.title}
                    </li>
                  ))}
                </ul>
              </li>
            );
          })}
        </ol>
      )}
      {current.periods.length > shown && (
        <div className="text-center">
          <Button variant="outline" onClick={() => setShown((s) => s + PAGE)}>Show earlier periods</Button>
        </div>
      )}
    </div>
  );
}
