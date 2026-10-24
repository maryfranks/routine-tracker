import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { LayoutGrid, MoreHorizontal, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { ViewDialog } from "@/components/routine/ViewDialog";
import { TaskPanel } from "@/components/routine/TaskPanel";
import { EmptyState, ErrorState, ListSkeleton } from "@/components/routine/states";
import { useAction, useViews } from "@/hooks/use-routine";
import { api } from "@/services/api";
import { CADENCES } from "@/lib/periods";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/")({
  validateSearch: (s: Record<string, unknown>): { view?: string } => ({
    ...(typeof s["view"] === "string" ? { view: s["view"] } : {}),
  }),
  head: () => ({
    meta: [
      { title: "Your views — Routine" },
      { name: "description", content: "Daily, weekly and monthly routines with no overdue guilt." },
      { property: "og:title", content: "Your views — Routine" },
      { property: "og:description", content: "Daily, weekly and monthly routines with no overdue guilt." },
    ],
  }),
  component: Index,
});

function Index() {
  const { view: selectedId } = Route.useSearch();
  const navigate = useNavigate({ from: "/" });
  const views = useViews();
  const create = useAction(api.createView, "View created");

  const createAndOpen = async (v: Parameters<typeof api.createView>[0]) => {
    const made = await create.mutateAsync(v);
    navigate({ search: { view: made.id } });
  };

  if (views.isPending) return <div className="grid gap-8 md:grid-cols-[220px_1fr]"><ListSkeleton rows={4} /><ListSkeleton rows={5} /></div>;
  if (views.isError) return <ErrorState error={views.error} onRetry={() => views.refetch()} />;

  if (views.data.length === 0) {
    return (
      <EmptyState
        icon={<LayoutGrid className="size-8" />}
        title="Start with a single view"
        action={<ViewDialog onSubmit={createAndOpen} trigger={<Button size="lg"><Plus className="size-4" />Create your first view</Button>} />}
      >
        <p>A view groups tasks that share a rhythm — like <em>Health</em> every day, <em>Home</em> every week, or <em>Finances</em> every month.</p>
        <p className="mt-2">Tasks reset at the end of each period. Nothing piles up.</p>
      </EmptyState>
    );
  }

  const selected = views.data.find((v) => v.id === selectedId) ?? views.data[0]!;

  return (
    <div className="grid gap-8 md:grid-cols-[220px_1fr]">
      <aside className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs uppercase tracking-widest text-muted-foreground">Views</h2>
          <ViewDialog onSubmit={createAndOpen} trigger={<Button variant="ghost" size="icon" className="size-7" aria-label="New view"><Plus className="size-4" /></Button>} />
        </div>
        <ul className="space-y-1">
          {views.data.map((v) => (
            <li key={v.id}>
              <Link
                to="/"
                search={{ view: v.id }}
                className={cn(
                  "flex items-center justify-between rounded-md px-3 py-2 text-sm transition-colors",
                  v.id === selected.id ? "bg-accent text-accent-foreground" : "hover:bg-muted",
                )}
              >
                <span className="truncate">{v.name}</span>
                <span className="ml-2 shrink-0 text-xs text-muted-foreground">
                  {v.taskCount > 0 ? `${v.doneCount}/${v.taskCount}` : "—"} · {CADENCES.find((c) => c.value === v.cadence)?.label[0]}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </aside>

      <div className="relative">
        <div className="absolute right-0 top-0">
          <ViewActions id={selected.id} name={selected.name} cadence={selected.cadence} onDeleted={() => navigate({ search: {} })} />
        </div>
        <TaskPanel key={selected.id} view={selected} />
      </div>
    </div>
  );
}

function ViewActions({ id, name, cadence, onDeleted }: { id: string; name: string; cadence: Parameters<typeof api.createView>[0]["cadence"]; onDeleted: () => void }) {
  const update = useAction((v: Parameters<typeof api.updateView>[1]) => api.updateView(id, v), "View updated");
  const remove = useAction(() => api.deleteView(id), "View deleted");
  return (
    <AlertDialog>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon" aria-label="View options"><MoreHorizontal className="size-4" /></Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <ViewDialog
            initial={{ name, cadence }}
            onSubmit={(v) => update.mutateAsync(v)}
            trigger={<DropdownMenuItem onSelect={(e) => e.preventDefault()}>Edit view</DropdownMenuItem>}
          />
          <AlertDialogTrigger asChild>
            <DropdownMenuItem className="text-destructive">Delete view</DropdownMenuItem>
          </AlertDialogTrigger>
        </DropdownMenuContent>
      </DropdownMenu>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete "{name}"?</AlertDialogTitle>
          <AlertDialogDescription>This removes the view, its tasks, and their history. It can't be undone.</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            onClick={() => remove.mutateAsync(undefined).then(onDeleted, () => {})}
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
